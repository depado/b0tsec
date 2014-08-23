#!/home/depado/3.3/bin/python3.3
# -*- coding: utf8 -*-

# External Libs
import irc.bot

# Internal Libs
# TODO: Using requests instead of urllib
import pickle
import sys
import random
import urllib.request
import urllib.parse
import time
from datetime import datetime

from constants import *
from functions import *

def pdump(datasource, filename):
    pickle.dump(datasource, open('pickles/{}'.format(filename), 'wb'))

def pload(filename):
    try:
        return pickle.load(open('pickles/{}'.format(filename), 'rb'))
    except (FileNotFoundError, OSError) as error:
        return {}


class BotModeration(irc.bot.SingleServerIRCBot):

    def __init__(self):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], botname, botname)

        # Network related attributes
        # TODO: Replace this with requests (those lines won't be needed)
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Content-Type', 'application/json;charset=utf-8')]
        
        # Command related attributes
        self.rindex = 1
        self.rbulet = random.randint(1, 6)
        self.basic  = basics
        self.extra  = extra

        # Stored attributes
        self.buglist   = pload('buglist.p')
        self.deathlist = pload('deathlist.p')
        self.ctf       = pload('ctf.p')
        self.idle      = pload('idle.p')
        self.afk       = pload('afk.p')

        print("Running.")

    def on_welcome(self, serv, ev):
        with open('ircpwd') as pwd:
            connection_string = "identify {}".format(pwd.read())
            serv.privmsg("NickServ", connection_string)
        serv.join(chan)

    def on_kick(self, serv, ev):
        serv.join(chan)

    def on_pubmsg(self, serv, ev):
        command      = ev.arguments[0].split(" ")[0]
        command_args = ev.arguments[0].split(" ")[1:] if len(ev.arguments[0].split(" ")) > 1 else []
        author       = ev.source.nick

        # Away from keyboard handler
        if author in self.afk.keys():
            del self.afk[author]
            serv.privmsg(chan, "{} is back.".format(author))
            pdump(self.afk, "afk.p")

        # Idle time handler
        self.idle[author] = datetime.now()
        pdump(self.idle, "idle.p")

        # Avoid single checks for message that doesn't start with an activated command
        if command in activated_commands:
            if command == "!afk":
                if len(command_args) > 0:
                    message = " ".join(command_args)
                    self.afk[author] = message
                    serv.privmsg(chan, "{} is afk : {}".format(author, message))
                else:
                    self.afk[author] = "Away"
                    serv.privmsg(chan, "{} is afk.".format(author))
                pdump(self.afk, 'afk.p')

            elif command == "!afklist":
                if len(self.afk) > 0:
                    for key in self.afk.keys():
                        serv.privmsg(chan, "{author} : {message}".format(author=key, message=self.afk[key]))
                else:
                    serv.privmsg(chan, "No one is afk right now.")

            # Bug handler
            elif command == "!bug":
                if len(command_args) > 0:
                    if command_args[0] in ['add', 'list']:
                        if command_args[0] == 'add':
                            if len(command_args) > 1: 
                                message = " ".join(command_args[1:])
                                if author in self.buglist.keys():
                                    self.buglist[author].append(message)
                                else:
                                    self.buglist[author] = [message]

                                serv.privmsg(chan, "Bug registered.")
                                pdump(self.buglist, "buglist.p")
                            else:
                                serv.privmsg(chan, "Describe your bug or request.")
                        if command_args[0] == 'list':
                            for user, bugs in self.buglist.items():
                                serv.privmsg(chan, "{} :".format(user))
                                for bug in bugs:
                                    serv.privmsg(chan, bug)
                    else:
                        serv.privmsg(author, "Invalid argument. (add | list)")    
                else:
                    serv.privmsg(author, "This command takes an argument. (add | list)")

            elif command in self.basic.keys():
                serv.privmsg(chan, "{} {}".format(author, self.basic[command]))

            elif command in self.extra.keys():
                serv.privmsg(chan, "{}".format(self.extra[command]))

            elif command == "!beer":
                if len(command_args) > 0:
                    message = " ".join(command_args)
                    serv.privmsg(chan, "Beer tonight {} ?".format(message))
                else:
                    serv.privmsg(chan, "{} is going to drink a beer.".format(author))

            elif command == "!femops":
                serv.privmsg(chan, "{}".format(manifesto[random.randint(0, len(manifesto))]))

            elif command == "!eightball":
                serv.privmsg(chan, "{}".format(eightball_list[random.randint(0, len(eightball_list))]))

            elif command == "!roulette":

                def on_death():
                    if author in self.deathlist.keys():
                        self.deathlist[author] += 1
                        serv.privmsg(chan, "*BANG* {} is gay and dead ! (Total : {} deaths.)".format(author, self.deathlist[author]))
                    else:
                        self.deathlist[author] = 1
                        serv.privmsg(chan, "*BANG* {} is gay and dead ! (First death)".format(author))

                    if self.deathlist[author] in roulette_achievements.keys():
                        serv.privmsg(chan, "{} earned an achievement : {}".format(author, roulette_achievements[self.deathlist[author]]))
                    pickle.dump(self.deathlist, open("deathlist.p", "wb"))

                if len(command_args) > 0:
                    if command_args[0] in ["--cheat", "-c"]:
                        on_death()
                        self.rbulet = random.randint(1, 6)
                        self.rindex = 1

                    if command_args[0] in ["--list", "-l"]:
                        for user in self.deathlist.keys():
                            if self.deathlist[user] == 1:
                                serv.privmsg(chan, "{} died 1 time.".format(user))
                            serv.privmsg(chan, "{} died {} times.".format(user, self.deathlist[user]))
                else:
                    if self.rindex == self.rbulet:
                        on_death()
                        self.rbulet = random.randint(1,6)
                        self.rindex = 1
                    else:
                        serv.privmsg(chan, "*click*")
                        self.rindex += 1

            elif command == "!export":
                with open("server_bot.py") as f:
                    text = f.read()
                url = 'http://pastebin.com/api/api_post.php'
                values = {
                            "api_dev_key": "204d1dd6578cbba12ad45536dfcdcc04",
                            "api_paste_code": text,
                            "api_paste_private": 1,
                            "api_paste_name ": "Dat N0sec Bot",
                            "api_paste_expire_date ": "10M",
                            "api_paste_format": "python",
                            "api_user_key ": "",
                            "api_option": "paste",
                         }
                data = urllib.parse.urlencode(values).encode('utf-8')
                request = urllib.request.Request(url, data)
                try:
                    response = self.opener.open(request)
                    serv.privmsg(author, "This is my code : {}".format(response.read().decode("utf-8")))
                except Exception as e:
                    serv.privmsg(author, "Couldn't paste myself.")

            elif command == "!dirtylinks":
                if len(command_args) > 0:
                    if command_args[0] in ['-r', '--random']:
                        serv.privmsg(chan, links[random.randint(0, len(links))])
                else:
                    serv.privmsg(chan, "List of dirty links of #n0sec")
                    for link in links:
                        serv.privmsg(chan, link)

            elif command == "!sentence":
                url = "http://translate.google.com/translate_tts?tl=fr&q="
                x = '%20'.join(command_args)
                url = url+x
                short = shorten(url)
                if short:
                    serv.privmsg(chan, "Synthese Vocale : {}".format(short))

            elif command == "!shorten":
                if len(command_args) > 0:
                    url = command_args[0]
                    short = shorten(url)
                    if short:
                        serv.privmsg(chan, "{}".format(short))
                else:
                    serv.privmsg(author, "This command requires an argument.")

            elif command == "!gay":
                if not command_args:
                    serv.privmsg(chan, "{} is gay !".format(author))
                elif len(command_args) == 1:
                    serv.privmsg(chan, "{} is gay !".format(command_args[0]))
                else:
                    serv.privmsg(chan, "{} are gay !".format(" ".join(command_args)))

            elif command == "!fap":
                if not command_args:
                    serv.privmsg(chan, "{} is going to fap.".format(author))
                elif len(command_args) == 1:
                    if command_args[0].lower() == author.lower():
                        serv.privmsg(chan, "{} is going to fap.".format(author))
                    else:
                        serv.privmsg(chan, "{} is fapping {}".format(author, command_args[0]))
                elif len(command_args) == 2:
                    serv.privmsg(chan, "{} is fapping {} and {} with both hands".format(author, command_args[0], command_args[1]))
                else:
                    serv.privmsg(chan, "{}, you don't have more than two hands, you bitch !".format(author))

            elif command == "!idle":
                if not command_args:
                    serv.privmsg(author, "This command requires an argument.")
                elif len(command_args) == 1:
                    if self.idle.get(command_args[0], None) is not None:
                        idle_time = self.idle[command_args[0]]
                        serv.privmsg(chan, "{} has been idle for {}".format(command_args[0],
                                                                            str(datetime.now() - idle_time)[:-7]))
                    else:
                        serv.privmsg(chan, "Never saw {} or didn't registered his/her last message.".format(command_args[0]))

            elif command == "!nifle":
                if author == "Fataloror":
                    serv.privmsg(chan, "Fataloror frappe toute la room d'un coup de nichons !")

            elif command in ["!strpn", "!strapon"]:
                if not command_args:
                    if random.random() < 0.2:
                        serv.privmsg(chan, "{} uses a strapon on the whole room. BAM STRAPON !".format(author))
                    else:
                        serv.privmsg(chan, "{} attempt to use a strapon failed. Fumble.".format(author))
                else:
                    if random.random() < 0.5:
                        serv.privmsg(chan, "{} uses a strapon on {}. Critical Hit ! BAM STRAPON !".format(author, command_args[0]))
                    else:
                        serv.privmsg(chan, "{}'s attempt to use a strapon on {} failed. Fumble.".format(author, command_args[0]))


if __name__ == "__main__":
    BotModeration().start()

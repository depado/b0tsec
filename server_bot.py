#!/home/depado/3.3/bin/python3.3
# -*- coding: utf8 -*-

# External Libs
import irc.bot

# Internal Libs
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
    pickle.dump(datasource, open(filename, "wb"))

def pload(filename):
    try:
        return pickle.load(open(filename, 'rb'))
    except (FileNotFoundError, OSError) as error:
        return {}


class BotModeration(irc.bot.SingleServerIRCBot):

    def __init__(self):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], botname, botname)

        self.rindex = 1
        self.rbulet = random.randint(1, 6)
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Content-Type', 'application/json;charset=utf-8')]
        self.basic = basics
        self.extra = extra

        self.buglist   = pload('buglist.p')
        self.deathlist = pload('deathlist.p')
        self.ctf       = pload('ctf.p')
        self.idle      = pload('idle.p')
        self.afk       = pload('afk.p')

    def on_welcome(self, serv, ev):
        with open('ircpwd') as pwd:
            connection_string = "identify {}".format(pwd.read())
            serv.privmsg("NickServ", connection_string)
        serv.join(chan)

    def on_kick(self, serv, ev):
        serv.join(chan)

    def on_pubmsg(self, serv, ev):
        argmessage = ev.arguments[0].split(" ")
        command = argmessage[0]
        auteur = ev.source.nick

        if auteur in self.afk.keys():
            del self.afk[auteur]
            serv.privmsg(chan, "{} is back.".format(auteur))
            pickle.dump(self.afk, open("afk.p", "wb"))

        self.idle[auteur] = datetime.now()
        pickle.dump(self.idle, open("idle.p", "wb"))

        if command == "!bug":
            if len(argmessage) > 1:
                message = " ".join(argmessage[1:])
                basicauteur = auteur
                x = 0
                while auteur in self.buglist.keys():
                    auteur = basicauteur+str(x)
                    x += 1
                self.buglist[auteur] = message
                serv.privmsg(chan, "Bug registered.")
                pickle.dump(self.buglist, open("buglist.p", "wb"))
            else:
                serv.privmsg(chan, "Describe your bug, bitch.")

        if command == "!buglist":
            for auteur in self.buglist.keys():
                serv.privmsg(chan, "{} : {}".format(auteur, self.buglist[auteur]))

        if command in self.basic.keys():
            serv.privmsg(chan, "{} {}".format(auteur, self.basic[command]))

        elif command in self.extra.keys():
            serv.privmsg(chan, "{}".format(self.extra[command]))

        if command == "!beer":
            if len(argmessage) > 1:
                message = " ".join(argmessage[1:])
                serv.privmsg(chan, "Beer tonight {} ?".format(message))
            else:
                serv.privmsg(chan, "{} is going to drink a beer.".format(auteur))

        if command == "!femops":
            serv.privmsg(chan, "{}".format(manifesto[random.randint(0, len(manifesto))]))

        if command == "!eightball":
            serv.privmsg(chan, "{}".format(eightball_list[random.randint(0, len(eightball_list))]))

        if command == "!roulette":

            def on_death():
                if auteur in self.deathlist.keys():
                    self.deathlist[auteur] += 1
                    serv.privmsg(chan, "*BANG* {} is gay and dead ! (Total : {} deaths.)".format(auteur, self.deathlist[auteur]))
                else:
                    self.deathlist[auteur] = 1
                    serv.privmsg(chan, "*BANG* {} is gay and dead ! (First death)".format(auteur))

                if self.deathlist[auteur] in roulette_achievements.keys():
                    serv.privmsg(chan, "{} earned an achievement : {}".format(auteur, roulette_achievements[self.deathlist[auteur]]))
                pickle.dump(self.deathlist, open("deathlist.p", "wb"))

            if len(argmessage) > 1:
                if argmessage[1] == "--cheat" or argmessage[1] == "-c":
                    on_death()
                    self.rbulet = random.randint(1, 6)
                    self.rindex = 1

                if argmessage[1] == "--list" or argmessage[1] == "-l":
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

        if command == "!export":
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
                serv.privmsg(auteur, "This is my code : {}".format(response.read().decode("utf-8")))
            except Exception as e:
                serv.privmsg(auteur, "Couldn't paste myself. Running on a shitty connection sorry.")

        if command == "!dirtylinks":
            if len(argmessage) > 1:
                if argmessage[1] == "random":
                    serv.privmsg(chan, links[random.randint(0, len(links))])
            else:
                serv.privmsg(chan, "List of dirty links of #n0sec")
                for link in links:
                    serv.privmsg(chan, link)

        if command == "!sentence":
            url = "http://translate.google.com/translate_tts?tl=fr&q="
            x = '%20'.join(argmessage[1:])
            url = url+x
            short = shorten(url)
            if short:
                serv.privmsg(chan, "Synthese Vocale : {}".format(short))

        if command == "!afk":
            if len(argmessage) > 1:
                message = " ".join(argmessage[1:])
                self.afk[auteur] = message
                serv.privmsg(chan, "{} is afk : {}".format(auteur, message))
            else:
                self.afk[auteur] = "Away (no message provided)"
                serv.privmsg(chan, "{} is afk.".format(auteur))
            pdump(self.afk, 'afk.p')

        if command == "!afklist":
            if len(self.afk) > 0:
                for key in self.afk.keys():
                    serv.privmsg(chan, "{auteur} : {message}".format(auteur=key, message=self.afk[key]))
            else:
                serv.privmsg(chan, "No one is afk right now.")

        if command == "!shorten":
            if len(argmessage) < 2:
                serv.privmsg(auteur, "This command requires an argument.")
            else:
                url = argmessage[1]
                short = shorten(url)
                if short:
                    serv.privmsg(chan, "{}".format(short))

        if command == "!ctf":
            if len(argmessage) < 2:
                serv.privmsg(auteur, "This command requires an argument.")
            else:
                if argmessage[1] == "list":
                    for user in self.ctf.keys():
                        serv.privmsg(chan, "{} : {}".format(user, self.ctf[user]))

                elif argmessage[1] == "stop":
                    serv.privmsg(chan, "{} stopped working on the ctf : {}.".format(auteur, self.ctf[auteur]))
                    del self.ctf[auteur]
                    pickle.dump(self.ctf, open("ctf.p", "wb"))

                else:
                    current = " ".join(argmessage[1:])
                    self.ctf[auteur] = current
                    serv.privmsg(chan, "{} is now working on the ctf : {}".format(auteur, self.ctf[auteur]))
                    pickle.dump(self.ctf, open("ctf.p", "wb"))

        if command == "!gay":
            if len(argmessage) < 2:
                serv.privmsg(chan, "{} is gay !".format(auteur))
            elif len(argmessage) == 2:
                serv.privmsg(chan, "{} is gay !".format(argmessage[1]))
            else:
                serv.privmsg(chan, "{} are gay !".format(" ".join(argmessage[1:])))

        if command == "!fap":
            if len(argmessage) < 2:
                serv.privmsg(chan, "{} is going to fap.".format(auteur))
            elif len(argmessage) == 2:
                if argmessage[1].lower() == auteur.lower():
                    serv.privmsg(chan, "{} is going to fap.".format(auteur))
                else:
                    serv.privmsg(chan, "{} is fapping {}".format(auteur, argmessage[1]))
            elif len(argmessage) == 3:
                serv.privmsg(chan, "{} is fapping {} and {} with both hands".format(auteur, argmessage[1], argmessage[2]))
            else:
                serv.privmsg(chan, "{}, you don't have more than two hands, you bitch !".format(auteur))

        if command == "!idle":
            if len(argmessage) < 2:
                serv.privmsg(auteur, "This command requires an argument.")
            elif len(argmessage) == 2:
                if self.idle.get(argmessage[1], None) is not None:
                    idle_time = self.idle[argmessage[1]]
                    serv.privmsg(chan, "{} has been idle for {}".format(argmessage[1],
                                                                        str(datetime.now() - idle_time)[:-7]))
                else:
                    serv.privmsg(chan, "Never saw {} or didn't registered his/her last message.".format(argmessage[1]))

        if command == "!nifle":
            if auteur == "Fataloror":
                serv.privmsg(chan, "Fataloror frappe toute la room d'un coup de nichons !")
            else:
                serv.privmsg(chan, "YOU GOT NO BOOBIES YOU CAN'T DO THAT !")

        if command in ["!strpn", "!strapon"]:
            if len(argmessage) < 2:
                if random.random() < 0.2:
                    serv.privmsg(chan, "{} uses a strapon on the whole room. BAM STRAPON !".format(auteur))
                else:
                    serv.privmsg(chan, "{} attempt to use a strapon failed. Critical Failure.".format(auteur))
            else:
                if random.random() < 0.5:
                    serv.privmsg(chan, "{} uses a strapon on {}. Critical Hit ! BAM STRAPON !".format(auteur, argmessage[1]))
                else:
                    serv.privmsg(chan, "{} attempt to use a strapon on {} failed. Critical Failure.".format(auteur, argmessage[1]))


if __name__ == "__main__":
    BotModeration().start()

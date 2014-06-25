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


class BotModeration(irc.bot.SingleServerIRCBot):
    def __init__(self):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], botname, botname)

        self.rindex = 1
        self.rbulet = random.randint(1, 6)
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Content-Type', 'application/json;charset=utf-8')]
        self.basic = basics
        self.extra = extra

        try:
            self.buglist = pickle.load(open("buglist.p", "rb"))
        except (FileNotFoundError, OSError) as error:
            print(error)
            self.buglist = {}

        try:
            self.deathlist = pickle.load(open("deathlist.p", "rb"))
        except (FileNotFoundError, OSError) as error:
            print(error)
            self.deathlist = {}

        try:
            self.ctf = pickle.load(open("ctf.p", "rb"))
        except (FileNotFoundError, OSError) as error:
            print(error)
            self.ctf = {}

        try:
            self.idle = pickle.load(open("idle.p", "rb"))
        except (FileNotFoundError, OSError) as error:
            print(error)
            self.idle = {}

    def on_welcome(self, serv, ev):
        serv.privmsg("NickServ", "identify tvjhnqn4764")
        serv.join(chan)

        @periodic_task(60)
        def tasked():
            data = urllib.request.urlopen('https://tools.intrepid-linux.info/bbs/json').read().decode("utf-8")
            thread_dict = json.loads(data)
            try:
                saved_dict = pickle.load(open("thread_dict.p", "rb"))
                if thread_dict['thread_number'] != saved_dict['thread_number']:
                    diff = thread_dict['thread_number']-saved_dict['thread_number']
                    if diff > 1:
                        message = "{} New Threads on the BBS".format(diff)
                    else:
                        message = "One New Thread on the BBS : {}".format(thread_dict['threads'][str(thread_dict['thread_number'])]['url'])
                    serv.privmsg(chan, message)
                    pickle.dump(thread_dict, open("thread_dict.p", "wb"))

                if thread_dict['comment_number'] != saved_dict['comment_number']:
                    for new_id in thread_dict['threads'].keys():
                        for saved_id in saved_dict['threads'].keys():
                            if new_id == saved_id:
                                unique_id = new_id
                                diff = thread_dict['threads'][unique_id]['comments'] - saved_dict['threads'][unique_id]['comments']
                                if diff == 1:
                                    m_bit = "One New Comment"
                                elif diff > 1:
                                    m_bit = "{} New Comments".format(diff)
                                else:
                                    continue
                                serv.privmsg(chan, "{} on Thread {}".format(m_bit, thread_dict['threads'][unique_id]['url']))
                    pickle.dump(thread_dict, open("thread_dict.p", "wb"))
            except FileNotFoundError:
                pickle.dump(thread_dict, open("thread_dict.p", "wb"))
        tasked()

    def on_kick(self, serv, ev):
        serv.join(chan)

    def on_pubmsg(self, serv, ev):
        argmessage = ev.arguments[0].split(" ")
        command = argmessage[0]
        auteur = ev.source.nick

        if auteur in afk.keys():
            del afk[auteur]
            serv.privmsg(chan, "{} is back.".format(auteur))
            pickle.dump(afk, open("afk.p", "wb"))

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

        if command == "!dumpbug":
            if auteur == "Depado":
                self.buglist = {}
                pickle.dump(self.buglist, open("buglist.p", "wb"))
                serv.privmsg(chan, "Dumped all the bugs :)")
            else:
                serv.privmsg(chan, "You're not my master.")

        if command == "!help":
            serv.privmsg(auteur, "[optionnal argument] <needed argument>")
            serv.privmsg(auteur, "!beer [someone]; !drug ; !nom ; !smoke ; !coffee")
            serv.privmsg(auteur, "!afk [message] ; !afklist ; !back")
            serv.privmsg(auteur, "!export ; !dirtylinks ['random'] ; !femops")
            serv.privmsg(auteur, "!eightball [question] ; !roulette ; !sentence <your sentence>")

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

        if command == "!reload":
            if auteur == "Depado":
                serv.privmsg(auteur, "{} wants me to reload myself. Be right back.".format(auteur))
                sys.exit(2)
            else:
                serv.privmsg(auteur, "You're not my master.")

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
                afk[auteur] = message
                serv.privmsg(chan, "{} is afk : {}".format(auteur, message))
            else:
                afk[auteur] = "Is away"
                serv.privmsg(chan, "{} is afk.".format(auteur))
            pickle.dump(afk, open("afk.p", "wb"))

        if command == "!afklist":
            if len(afk) > 0:
                for key in afk.keys():
                    serv.privmsg(chan, "{auteur} : {message}".format(auteur=key, message=afk[key]))
            else:
                serv.privmsg(chan, "No one is afk right now.")

        if command == "!up":
            if len(argmessage) < 2:
                serv.privmsg(chan, "This command requires an argument.")
            else:
                try:
                    host = argmessage[1]
                    request = urllib.request.Request("http://www.downforeveryoneorjustme.com/{}".format(host))
                    response = self.opener.open(request)
                    if "It's just you" in response.read().decode('utf-8'):
                        serv.privmsg(chan, "Host {} is Up.".format(host))
                    else:
                        serv.privmsg(chan, "Host {} is Down".format(host))
                except Exception as e:
                    serv.privmsg(chan, "Stop playing with my encoding, bitch !")

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
                    serv.privmsg(chan, "INCEPTION ! END OF THE WORLD IN 3...")
                    time.sleep(1)
                    serv.privmsg(chan, "2...")
                    time.sleep(1)
                    serv.privmsg(chan, "1...")
                    time.sleep(1)
                    serv.privmsg(chan, "Just kidding. {} is gay. And so is tanael.".format(auteur))
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

if __name__ == "__main__":
    BotModeration().start()

#!/usr/bin/env python
# -*- coding: utf8 -*-

server = "irc.freenode.net"
port = 6667
botname = "b0tsec"
chan = "#n0sec"

try:
    with open("manifesto.txt") as f:
        manifesto = f.readlines()
    manifesto = [word.strip() for word in manifesto]
except Exception as e:
    print(e)

roulette_achievements = {
                          5:"It's ok to cry",
                          10:"Depressive Player",
                          15:"Mad Russian Roulette Player",
                          20:"Suicide is sometimes a Solution",
                          25:"Are you coding in PHP ?",
                          30:"Forced to use Windows",
                          35:"Done with Life"
                        }
eightball_list = [
                   "It is certain",
                   "It is decidedly so",
                   "Without a doubt",
                   "Yes definitely",
                   "You may rely on it",
                   "As I see it yes",
                   "Most likely",
                   "Outlook good",
                   "Yes",
                   "Signs point to yes",
                   "Reply hazy try again",
                   "Ask again later",
                   "Better not tell you now",
                   "Cannot predict now",
                   "Concentrate and ask again",
                   "Don't count on it",
                   "My reply is no",
                   "My sources say no",
                   "Outlook not so good",
                   "Very doubtful"
                 ]
links = [
          "http://www.hai2u.com/", 
          "http://www.specialfriedrice.net/",
          "http://www.meatspin.cc/"
        ]

trolls = [
           "Python is better than perl.",
           "Do you accept Jesus Christ as your savior and lord ?",
         ]

basics = {
           "!nom":"is going to eat.",
           "!smoke":"is going to smoke.",
           "!drug":"is going to smoke a big joint.",
           "!coffee":"is going to drink a coffee",
           "!bifle":"saute en l'air dans un mouvement circulaire, son sexe biflant toute la room.",
         }

extra = {
          "!flip":"(╯°□°）╯︵ ┻━┻",
          "!chill":"┬─┬﻿ ノ( ゜-゜ノ",
          "!flipyou":"(╯°□°）╯︵ /(.□ . \)",
          "!dunno":"¯\(°_o)/¯",
        }


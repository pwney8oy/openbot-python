#!/usr/bin/env python
# -*- coding: utf-8 -*- 
############################################################################
#    Copyright (C) 2005-206 by RebelCoders.org community                   #
#                           Authors: LuX(luciano.ferraro@gmail.com)        #
#                                                                          #
#                                                                          #
#    This program is free software; you can redistribute it and/or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################
import os
import sys
import time
import urllib

class Core:
    def __init__(self):
        self.help_message = """Usage: updater.py [OPTIONS]
OPTIONS:
       --ignore-conf    don't update conf files (conf/).
       --help           print this message."""
        self.ignore_conf = False

    def openurl(self, url):
        urlopen = urllib.urlopen("http://openbot-python.googlecode.com/svn/trunk/" + url)
        file = url.split("/")[-1]
        if os.path.exists(file):
            os.remove(file)
        filesaver = open(file, "w")
        filesaver.write(urlopen.read())
        filesaver.close()
        time.sleep(0.005)

    def mkdir(self, path):
        if not os.path.exists(path):
            print "- Creating %s directory..."% (path)
            os.mkdir(path)
        os.chdir(path)

    def read_argv(self):
        if len(sys.argv) > 0:
            for argv in sys.argv:
                if argv == "--ignore-conf":
                    self.ignore_conf = True
                elif argv == "--help":
                    print self.help_message
                    sys.exit()

    def start_update(self):
        print "- Downloading openbot core..."
        for url in ("openbot.py", "openbot.tac", "channels.py", "conf.py"):
            self.openurl(url)
        self.mkdir("library")
        ####
        print "- Downloading Libraries..."
        for url in ("feedparser.py", "utils.py", "__init__.py"):
            self.openurl("library/" + url)
        ####
        os.chdir("..")
        if not self.ignore_conf:
            self.mkdir("conf")
            print "- Downloading conf files...."
            for url in ("openbot.commands", "openbot.join", "openbot.manual", 
            "openbot.modes", "openbot.owner.commands", "openbot.owner.manual"):
                self.openurl("conf/" + url)
            os.chdir("..")
        ####
        self.mkdir("plugins")
        print "- Downloading plugins..."
        for url in ("base.py", "google.py", "news.py", "logs.py", "peak.py", 
        "quote.py", "private_identifier.py", "syscmd.py", "seen.py", "weather.py"):
            self.openurl("plugins/" + url)
        ####
        self.mkdir("core_plugin")
        self.openurl("plugins/core_plugin/confparser.py")
        self.openurl("plugins/core_plugin/welcome_message.py")
        ####
        os.chdir("..")
        self.mkdir("conf_reader")
        for url in ("_commands.py", "join.py", "manual.py", "modes.py"):
            self.openurl("plugins/conf_reader/" + url)
        ####
        os.chdir("../..")
        self.mkdir("data")
        ####
        print "- Installation finished, run openbot.py with Python for use it (`python openbot.py`"

core = Core()
core.read_argv()
core.start_update()

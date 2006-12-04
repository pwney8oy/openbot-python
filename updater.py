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

help_message = """Usage: updater.py [OPTION]
OPTIONS:
       --ignore-conf    don't update conf files (conf/).
       --help           print this message."""
ignore_conf = False

def openurl(url):
    urlopen = urllib.urlopen("http://openbot-python.googlecode.com/svn/trunk/" + url)
    file = url.split("/")[-1]
    if os.path.exists(file):
        os.remove(file)
    filesaver = open(file, "w")
    filesaver.write(urlopen.read())
    filesaver.close()
    time.sleep(0.005)

def mkdir(path):
    if not os.path.exists(path):
        print "- Creating %s directory..."% (path)
        os.mkdir(path)
    os.chdir(path)

if len(sys.argv) > 0:
    for argv in sys.argv:
        if argv == "--ignore-conf":
            ignore_conf = True
        elif argv == "--help":
            print help_message
            sys.exit()

print "- Downloading openbot core..."
openurl("openbot.py")
openurl("openbot.tac")
openurl("channels.py")
openurl("conf.py")

mkdir("library")
print "- Downloading Libraries..."
openurl("library/feedparser.py")
openurl("library/utils.py")

os.chdir("..")

if not ignore_conf:
    mkdir("conf")
    print "- Downloading conf files...."
    openurl("conf/openbot.commands")
    openurl("conf/openbot.join")
    openurl("conf/openbot.manual")
    openurl("conf/openbot.modes")
    openurl("conf/openbot.owner.commands")
    openurl("conf/openbot.owner.manual")

os.chdir("..")

mkdir("plugins")
print "- Downloading plugins..."
openurl("plugins/base.py")
openurl("plugins/google.py")
openurl("plugins/news.py")
openurl("plugins/logs.py")
openurl("plugins/peak.py")
openurl("plugins/quote.py")
openurl("plugins/private_identifier.py")
openurl("plugins/syscmd.py")
openurl("plugins/seen.py")

mkdir("core_plugin")
openurl("plugins/core_plugin/confparser.py")
openurl("plugins/core_plugin/welcome_message.py")

os.chdir("..")
mkdir("conf_reader")
openurl("plugins/conf_reader/_commands.py")
openurl("plugins/conf_reader/join.py")
openurl("plugins/conf_reader/manual.py")
openurl("plugins/conf_reader/modes.py")

os.chdir("../..")
mkdir("data")

print "- Installation finished, run openbot.py with Python for use it"

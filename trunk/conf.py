#!/usr/bin/env python
# -*- coding: utf-8 -*- 
############################################################################
#    Copyright (C) 2005-2007                                               #
#                           Ferraro Luciano (aka lux)                      #
#                            email : luciano.ferraro@gmail.com             #
#                            website : http://ferraro.wordpress.org/       #
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
" Configure the Bot "
import os
import sys
from library import utils
from library.utils import messages as send
import random
send = utils.messages()

class Config:
    """
    Se è la prima volta che lo si avvia:
    Chiede tutti i dati all'utente
    Altrimenti:
    Prende i dati dal file conf/openbot.main"""
    def __init__(self):
        self.variables = ["host", "port", "verbose", "logs", "botnick", "password", 
        "ns_password", "chans"]
        if os.path.exists("conf"):
            # Se esiste la dir conf/
            self.confdir = "conf/"
            self.maindir = ""
        else:
            send.error("Error: conf/ and ~/conf doesn't exists\n")
            sys.exit()
        self.values = None
        if __name__ != "__main__":
            self.values_conf()
    def values_conf(self, force=False):
        new = False
        if not os.path.exists(self.confdir+"openbot.main"):
            # Se e' la prima volta che si avvia il bot
            self.edit_or_create_conf()
            new = True
        self.values = self.open_conf()
        if force:
            self.edit_or_create_conf()
        return new
    def open_conf(self):
        values = {}
        for conf in utils._conf_parser(self.confdir+"openbot.main"):
            if len(conf) != 2:
                continue
            value = conf[1]
            conf = conf[0]
            if conf in self.variables:
                if conf in ("verbose", "logs", "port"):
                    value = int(value)
                values[conf] = value
                setattr(self, "_" + conf, value)
                if conf == "botnick":
                   self.firstbotnick = value
            else:
                send.warning(conf + ": UNKNOW VARIABLE")
        return values
    def edit_or_create_conf(self):
        values = {"host":"irc.freenode.org", "port":6667, "logs":1, "verbose":1, 
        "botnick":"oBot"+str(random.randrange(0, 9999)), "password":"", 
        "ns_password":"", "chans":""}
        if self.values != None:
            values = self.values
            send.system("Editing the conf file")
        # Chiede tutti i dati necessari
        self._host, condition = utils._get_input("NetWork ["+values["host"]+"]: ", 
        "len(a) <= 4")
        if condition:
            self._host = values["host"]
        self._port, condition = utils._get_input("Port ["+str(values["port"])+"]: ", 
        "(len(a) >= 2) and (a != '') and (int(a) != 0)")
        if not condition:
            self._port = values["port"]
        else:
            self._port = int(self._port)
        self._verbose, condition = utils._get_input(
        "Verbose (0/1)["+str(values["verbose"])+"]: ", "a")
        if not condition:
            self._verbose = values["verbose"]
        else:
            if values["verbose"]:
                self._verbose = 0
            else:
                self._verbose = 1
        self._logs, condition = utils._get_input(
        "Logs (0/1)["+str(values["logs"])+"]: ", "a")
        if not condition:
            self._logs = values["logs"]
        else:
            if values["logs"]:
                self._logs = 0
            else:
                self._logs = 1
        self._botnick, condition = utils._get_input(
        "Bot's nick ["+values["botnick"]+"]: ", "a == ''")
        if condition:
            self._botnick = values["botnick"]
        self.firstbotnick = self._botnick
        self._ns_password, condition = utils._get_input(
        "NickServe Password ["+values["ns_password"]+"]: ", "a == ''")
        if condition:
            self._ns_password = values["ns_password"]
        self._password = ""
        while self._password == "":
            self._password, condition = utils._get_input(
            "Bot identify Password ["+values["password"]+"]: ", "a == ''")
            if (self._password != values["password"]) and condition:
                self._password = values["password"]
        self._chans, condition = utils._get_input(
        "Channels to join ["+values["chans"]+"]: ", "a == ''")
        if condition:
            self._chans = values["chans"]
        for conf_arg in self.variables:
            utils._add_conf(self.confdir+"openbot.main", str(conf_arg), 
            str(getattr(self, "_" + conf_arg)))
    if __name__ != "__main__":
        try:
            variables = ("host", "port", "verbose", "logs", "botnick", 
            "password", "ns_password", "chans")
            for var in variables:
                utils.create_property(var)
        except: # Se si e' sollevata un'eccezione
            send.error(confdir+"openbot.main isn't a valid config file")
            sys.exit()

if __name__ == "__main__":
    core = Config()
    help_message = """Usage: conf.py [OPTIONS]
OPTIONS:
       --configure      create the config file (conf/openbot.main).
       --edit-conf      edit the config file (conf/openbot.main).
       --help           print this message."""
    if len(sys.argv) > 0:
        for argv in sys.argv:
            quit = True
            if argv == "--configure":
                if not core.values_conf():
                    send.system("The file conf exists, if you wanna edit it use " \
                    "--edit-conf.\n")
            elif argv == "--edit-conf":
                if os.path.exists("conf/openbot.main"):
                    core.values_conf(True)
            elif argv == "--help":
                print help_message
            else:
                print help_message
                quit = False
            if quit:
                sys.exit()
    else:
        print help_message

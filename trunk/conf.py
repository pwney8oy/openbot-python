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
" Configure the Bot "
import os
import sys
from library import utils
from library.utils import messages as send
import random

class Config:
    """
    Se è la prima volta che lo si avvia:
    Chiede tutti i dati all'utente
    Altrimenti:
    Prende i dati dal file conf/openbot.main"""
    def __init__(self):
        self.variables = ("host", "port", "verbose", "logs", "botnick", "password", 
        "ns_password", "chans")
        if os.path.exists("conf"):
            # Se esiste la dir conf/
            self.confdir = "conf/"
            self.maindir = ""
        else:
            send.error("Error: conf/ and ~/conf doesn't exists\n")
            sys.exit()
        if not os.path.exists(self.confdir+"openbot.main"):
            # Se e' la prima volta che si avvia il bot
            self.new_conf()
        else:
            # Se il file di conf gia' esiste
            self.open_conf()
    def open_conf(self):
        for conf in utils._conf_parser(self.confdir+"openbot.main"):
            if len(conf) != 2:
                continue
            value = conf[1]
            conf = conf[0]
            if conf in self.variables:
                if conf in ("verbose", "logs", "port"):
                    value = int(value)
                setattr(self, "_" + conf, value)
                if conf == "botnick":
                    self.firstbotnick = value
            else:
                send.warning(conf + ": UNKNOW VARIABLE")
    def new_conf(self):
        # Chiede tutti i dati necessari
        self._host, condition = utils._get_input("NetWork [irc.freenode.org]: ", 
        "len(a) <= 4")
        if condition:
            self._host = "irc.freenode.org"
        self._port, condition = utils._get_input("Port [6667]: ", 
        "(len(a) >= 2) and (a != '') and (int(a) != 0)")
        if not condition:
            self._port = 6667
        else:
            self._port = int(self._port)
        self._verbose, condition = utils._get_input("Verbose (0/1)[1]: ", "a")
        if not condition:
            self._verbose = 1
        else:
            self._verbose = 0
        self._logs, condition = utils._get_input("Logs (0/1)[1]: ", "a")
        if not condition:
            self._logs = 1
        else:
            self._logs = 0
        random_nick = "oBot"+str(random.randrange(0, 9999))
        self._botnick, condition = utils._get_input(
        "Bot's nick ["+random_nick+"]: ", "a == ''")
        if condition:
            self._botnick = random_nick
        self.firstbotnick = self._botnick
        self._ns_password, b = utils._get_input(
        "NickServe Password [blank for none]: ")
        self._password = ""
        while self._password == "":
            self._password, b = utils._get_input("Bot identify Password: ")
        self._chans, b = utils._get_input("Channels to join [blank for none]: ")
        for conf_arg in self.variables:
            utils._add_conf(self.confdir+"openbot.main", str(conf_arg), 
            str(getattr(self, "_" + conf_arg)))
    try:
        variables = ("host", "port", "verbose", "logs", "botnick", 
        "password", "ns_password", "chans")
        for var in variables:
            utils.create_property(var)
    except: # Se si e' sollevata un'eccezione
        send.error(confdir+"openbot.main isn't a valid config file")
        sys.exit()

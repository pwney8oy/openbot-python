#!/usr/bin/env python
# -*- coding: utf-8 -*- 
############################################################################
#    Copyright (C) 2005-206 by RebelCoders.org community                   #
#                           Authors: LuX(lux@rebelcoders.org)              #
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
import utils
import random

class Config:
    """
    Se è la prima volta che lo si avvia:
    Chiede tutti i dati all'utente
    Altrimenti:
    Prende i dati dal file conf/openbot.main"""
    #TODO: RISCRIVERE PARZIALMENTE
    #TODO: USARE library.utils._add_conf
    if os.path.exists("conf"):
        # Se esiste la dir conf/
        confdir = "conf/"
        maindir = ""
    else:
        print " -!ERROR!- conf/ and ~/conf don't exists\n"
        sys.exit()
    if not os.path.exists(confdir+"openbot.main"):
        # Se e' la prima volta che si avvia il bot
        # Chiede tutti i dati necessari
        _host = raw_input(str("NetWork [irc.freenode.org]: "))
        if len(_host) <= 5:
            _host = "irc.freenode.org"
        _port = raw_input(str("Port [6667]: "))
        if len(str(_port)) <= 2:
            _port = 6667
        _verbose = raw_input(str("Verbose (0/1)[1]: "))
        if _verbose != "0":
            _verbose = 1
        else:
            _verbose = 0
        _logs = raw_input(str("Logs (0/1)[1]: "))
        if _logs != "0":
            _logs = 1
        else:
            _logs = 0
        random_nick = "oBot"+str(random.randrange(0, 9999))
        _botnick = firstbotnick = raw_input(str(
            "Bot's nick [%s]: "%(random_nick)))
        if _botnick == "":
            _botnick = firstbotnick = random_nick
        _ns_password = raw_input(str(
            "NickServe Password (blank for none): "))
        _password = ""
        while _password == "":
            _password = raw_input(str("Bot identify Password: "))
        _chans = raw_input(str(
            "Channels to join [#rebelcode,#rebeltest]: "))
        if _chans == "":
            _chans = "#rebelcode,#rebeltest"
        saveconf = open(confdir+"openbot.main", "w")
        newconf = str("host=%s\nport=%s\nverbose=%s\nlogs=%s" \
                      "\nbotnick=%s\npassword=%s\nns_password=%s" \
                      "\nchans=%s"%(_host, _port, _verbose,
                                     _logs, _botnick,
                                     _password, _ns_password,
                                     _chans))
        saveconf.write(newconf)
        saveconf.close()
    else: # Se il file di conf gia' esiste
        openconf = open(confdir+"openbot.main", "r") # Apre il file di conf
        for conf in openconf.readlines():
            # Prende tutti i dati dal file di conf
            conf = conf.strip("\n").split("=", 1)
            value = conf[1]
            conf = conf[0]
            if (conf == "host") and (value != ""):
                _host = value
            elif (conf == "port") and (value != ""):
                _port = int(value)
            elif (conf == "verbose") and ((value == "0") or (value == "1")):
                _verbose = int(value)
            elif (conf == "logs") and ((value == "0") or (value == "1")):
                _logs = int(value)
            elif (conf == "botnick") and (value != ""):
                _botnick = firstbotnick = value
            elif conf == "password":
                _password = value
            elif conf == "ns_password":
                if value == None:
                    _ns_password = None
                else:
                    _ns_password = value
            elif (conf == "chans") and (value != ""):
                _chans = value
        openconf.close()
    try:
        variables = ("host", "port", "verbose", "logs", "botnick",
                     "password", "ns_password", "chans")
        for var in variables:
            utils.create_property(var)
    except: # Se si e' sollevata un'eccezione
        print confdir+"openbot.main isn't a valid config file"
        sys.exit()

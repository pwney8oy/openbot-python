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
" Modes conf reader Plugin "
class Modes:
    " Load Modes conf file "
    def __init__(self, core):
        self.core = core
        self.core.call("privmsg", self._on_privmsg)
        self.modes_conf = self.core.startdir+"conf/openbot.modes"

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        nick = user.split("!")[0]
        fromowners = self.core.irc.channels.is_identified(nick)
        if (fromowners) and (os.path.exists(self.modes_conf)):
            # Se il padrone ha scritto qualcosa
            # Carica il file di configurazione dei modi
            conf = open(self.modes_conf, "r")
            rows_number = 0
            # Avvia un ciclo che legge ogni riga nel file di conf
            for cfg in conf.readlines():
                rows_number += 1
                cfg = cfg.strip().split("=", 1)
                try:
                    error = False
                    cfg_out = cfg[1]
                    cfg = cfg[0]
                except:
                    error = True
                    self.core.add2log("-!ERROR!- %s: Line %s"%(
                        self.modes_conf, str(rownumber)))
                    continue
                if message[:len(cfg)] == cfg:
                    cfg_out = self.core.confparser(cfg_out, nick, "", channel,
                                                   message, cfg).strip()
                    set = cfg_out[0]
                    if set == "+":
                        set = True
                    elif set == "-":
                        set = False
                    else:
                        self.core.add2log("-!ERROR!- %s: Line %s"%(
                            self.modes_conf, str(rownumber)))
                        continue
                    user = cfg_out.split()
                    if len(user) > 1:
                        user = user[1]
                    else:
                        user = None
                    self.core.irc.mode(channel, set, cfg_out[1:], user=user)

def main(core):
    " Start the Plugin and load all the needed modules "
    modes = Modes(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os"]

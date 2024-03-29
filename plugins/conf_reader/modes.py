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
        user = user.split("!")[0]
        fromowners = self.core.irc.channels.is_identified(user)
        if (fromowners) and (os.path.exists(self.modes_conf)):
            # Se il padrone ha scritto qualcosa
            # Carica il file di configurazione dei modi
            conf = library.utils._conf_parser(self.modes_conf)
            rows_number = 0
            # Avvia un ciclo che legge ogni riga nel file di conf
            for cfg in conf:
                rows_number += 1
                cfg[0] = cfg[0].strip()
                cfg[1] = cfg[1].strip()
                # Parzialmente incluso in utils._conf_parser
                #try:
                #    error = False
                #    cfg_out = cfg[1]
                #    cfg = cfg[0]
                #except:
                #    error = True
                #    self.core.add2log("-!ERROR!- %s: Line %s"%(
                #        self.modes_conf, str(rownumber)))
                #    continue
                if message.split()[0] == cfg[0]:
                    cfg[1] = self.core.confparser(cfg[1], user, channel,
                                                   message).strip()
                    set = cfg[1][0]
                    if set == "+":
                        set = True
                    elif set == "-":
                        set = False
                    else:
                        self.core.add2log("-!ERROR!- %s: Line %s"%(
                            self.modes_conf, str(rownumber)))
                        continue
                    user = cfg[1].split()
                    if len(user) > 1:
                        user = user[1]
                    else:
                        user = None
                    self.core.irc.mode(channel, set, cfg[1][1:], user=user)

def main(core):
    " Start the Plugin and load all the needed modules "
    modes = Modes(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os", "library", "library.utils"]

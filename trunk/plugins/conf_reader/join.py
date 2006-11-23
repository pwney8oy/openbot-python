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
" Join conf reader Plugin "
class Core:
    " Load join conf file "
    def __init__(self, core):
        self.core = core
        self.core.call("userJoined", self._on_userJoined)
        self.join_conf = self.core.startdir + "conf/openbot.join"

    def _on_userJoined(self, user, channel):
        """Called when I see another user joining a channel.
        """
        print user
        if os.path.exists(self.join_conf):
            # Carica il file di configurazione
            conf = open(self.join_conf, "r")
            finshed = False
            rows_number = 0
            # Legge il file di conf e avvia il ciclo per ogni linea
            for cfg in conf.readlines():
                if not finshed:
                    rows_number += 1
                    if cfg.find("=") == -1:
                        self.core.add2log("-!ERROR!- %s: Line %s"%(
                            self.join_conf, str(rows_number)))
                        continue
                    """Poichè all'apertura di un file le \n
                    nel file si trasformano in \\n, vengono 
                    ritrasformate in \n, stessa cosa con \r
                    """
                    dictionary = {"\\n":"\n", "\\r":"\r", "\\001":"\001"}
                    scfg = self.core._replacer(dictionary, cfg)
                    scfg = scfg.split("=", 1)
                    cfg = scfg[0]
                    # Avvia il confparser
                    cfg = self.core.confparser(cfg, user, channel)
                    scfg = scfg[1]
                    scfg = self.core.confparser(scfg, user, channel)
                    # Se la linea corrente combacia con il user corrente
                    # oppure
                    # Se la linea corrente è .all.
                    if cfg.lower() in (user.lower(), ".all."):
                        finshed = True
                        for xint in scfg.split("\n"):
                            self.core.irc.sendLine(xint)

def main(core):
    " Start the Plugin and load all the needed modules "
    Core(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os"]

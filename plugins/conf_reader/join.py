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
        if os.path.exists(self.join_conf):
            concluted = False
            rows_number = 0
            # Legge il file di conf e avvia il ciclo per ogni linea
            for cfg in library.utils._conf_parser(self.join_conf):
                if not concluted:
                    rows_number += 1
                    # Incluso in utils._conf_parser
                    #if cfg.find("=") == -1:
                    #    self.core.add2log("-!ERROR!- %s: Line %s"%(
                    #        self.join_conf, str(rows_number)))
                    #    continue
                    """Poichè all'apertura di un file le \n
                    nel file si trasformano in \\n, vengono 
                    ritrasformate in \n, stessa cosa con \r
                    """
                    dictionary = {"\\n":"\n", "\\r":"\r", "\\001":"\001"}
                    cfg[1] = self.core._replacer(dictionary, cfg[1])
                    cfg[1] = self.core.confparser(cfg[1], user, channel)
                    cfg[0] = self.core._replacer(dictionary, cfg[0])
                    cfg[0] = self.core.confparser(cfg[0], user, channel)
                    # Se la linea corrente combacia con il user corrente
                    # oppure
                    # Se la linea corrente è .all.
                    if cfg[0].lower() in (user.lower(), ".all."):
                        concluted = True
                        for xint in cfg[1].split("\n"):
                            self.core.irc.sendLine(xint)

def main(core):
    " Start the Plugin and load all the needed modules "
    Core(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os", "library", "library.utils"]

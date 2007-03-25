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
" Manual conf reader Plugin "
class Manual:
    " Load all manual conf files "
    def __init__(self, core):
        self.core = core
        self.core.call("privmsg", self._on_privmsg)
        self.manual_conf = self.core.startdir+"conf/openbot.manual"
        self.owner_manual_conf = self.core.startdir+"conf/openbot.owner.manual"

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        user = user.split("!")[0]
        def manualdef(owner=False):
            " Carica il file di configurazione "
            # Se il user della persona che ha inviato il messaggio e' l'owner
            #  carica openbot.owner.manual
            if owner:
                try:
                    conf = library.utils._conf_parser(self.owner_manual_conf)
                except IOError, (errno, strerror):
                    error = "I/O error %s(%s): %s" % (self.owner_manual_conf, 
                                                      errno, strerror)
                    self.core.add2log(error)
                    return error
            # Altrimenti carica openbot.manual
            else:
                try:
                    conf = library.utils._conf_parser(self.manual_conf)
                except IOError, (errno, strerror):
                    error = "I/O error %s(%s): %s" % (self.manual_conf,
                                                      errno, strerror)
                    self.core.add2log(error)
                    return error
            # Avvia un ciclo che legge tutte le righe nel file di conf
            for cfg in conf:
                # Parserizza il conf
                cfg[0] = cfg[0].strip()
                cfg[0] = self.core.confparser(cfg[0], user, channel, message)
                cfg[1] = cfg[1].strip()
                cfg[1] = self.core.confparser(cfg[1], user, channel, message)
                nmsg = message.split()[0]
                # Se l'user e' uguale a quello di adesso
                if nmsg.lower() == cfg[0].lower():
                    dictionary = {"\\n":"\n", "\\r":"\r", "\\001":"\001"}
                    cfg[1] = self.core._replacer(dictionary, cfg[1])
                    # Invia al server ogni riga scritta nel file di conf
                    for splitted in cfg[1].splitlines():
                        self.core.irc.sendLine(splitted)
        fromowners = self.core.channels.is_identified(user)
        # Se il file conf/openbot.manual esiste vedi la def manual
        if os.path.exists(self.manual_conf):
            manualdef()
        # Se il file conf/openbot.owner.manual esiste
        #  e il messaggio e' stato inviato dall'owner vedi manual()
        if (fromowners) and (os.path.exists(self.owner_manual_conf)):
            manualdef(True)

def main(core):
    " Start the Plugin and load all the needed modules "
    Manual(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os", "time", "library", "library.utils"]

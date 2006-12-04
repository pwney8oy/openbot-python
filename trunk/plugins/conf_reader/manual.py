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
                    conf = open(self.owner_manual_conf, "r")
                except IOError, (errno, strerror):
                    error = "I/O error %s(%s): %s" % (self.owner_manual_conf, 
                                                      errno, strerror)
                    self.core.add2log(error)
                    return error
            # Altrimenti carica openbot.manual
            else:
                try:
                    conf = open(self.manual_conf, "r")
                except IOError, (errno, strerror):
                    error = "I/O error %s(%s): %s" % (self.manual_conf,
                                                      errno, strerror)
                    self.core.add2log(error)
                    return error
            # Avvia un ciclo che legge tutte le righe nel file di conf
            for cfg in conf.readlines():
                # Se la riga inizia con # la ignora e passa a quella dopo
                if cfg[0] == "#":
                    continue
                # Parserizza il conf
                cfg = self.core.confparser(cfg.strip(), user, channel)
                cfg = cfg.strip().split("=", 1)
                cfg_out = cfg[1]
                nmsg = message.split()[0]
                # Se il user e' uguale a quello di adesso
                if nmsg.lower() == cfg[0].lower():
                    dictionary = {"\\n":"\n", "\\r":"\r", "\\001":"\001"}
                    cfg_out = self.core._replacer(dictionary, cfg_out)
                    while True:
                        # Vedi xmsg
                        excfgt = cfg_out
                        cfg_out = xmsg(cfg_out, message)
                        if excfgt == cfg_out:
                            break
                    # Invia al server ogni riga scritta nel file di conf
                    for splitted in cfg_out.splitlines():
                        self.core.irc.sendLine(splitted)
        def xmsg(cfg_out, msg):
            """ Se nel file di conf si trova per esempio
            .message.[0:11]
            Lo cambia con le stringhe da 0 a 11 del messaggio inviato """
            if ".message.[" not in cfg_out:
                return cfg_out
            xmessage = cfg_out.split(".message.[", 1)[1].split(
                "].", 1)[0].split(":", 1)
            xmstart = int(xmessage[0])
            if xmessage[1] != "":
                xmend = int(xmessage[1])
            else:
                xmend = len(msg)
            msg = msg[xmstart:xmend]
            if ".message.[" in msg:
                msg = "infinite loop protection"
            cfg_out = cfg_out.replace(".message.[%s:%s]."%(xmessage[0],
                                                           xmessage[1]), msg)
            return cfg_out
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
__call__ = ["os", "time", "google"]

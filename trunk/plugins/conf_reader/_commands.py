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
" Commands conf reader Plugin "
class Core:
    " Load commands conf file "
    def __init__(self, core):
        self.core = core
        self.core.call("privmsg", self._on_privmsg)
        self.commands = 0
        self.commandsnick = []

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        nick = user.split("!")[0]
        fromowners = self.core.channels.is_identified(nick)
        if nick != self.core.conf.botnick:
            if (os.path.exists("conf/openbot.commands")) and (
                message.startswith("!commands")):
                canstart = False
                if self.commands < 3:
                    canstart = True
                    if nick in self.commandsnick:
                        canstart = False
                # Carica il file di configurazione
                if canstart:
                    thread.start_new(self._commands, (fromowners,nick, channel))
                else:
                    self.core.privmsg(nick, "Too many commands Requests")

    def _commands(self, owner, nick, chan):
        """Invia i comandi
        """
        self.commandsnick.append(nick)
        self.commands += 1
        conf = open(self.core.startdir + "conf/openbot.commands", "r")
        for cfg in conf.readlines():
            cfg_out = self.core.confparser(cfg.strip(), nick, chan=chan)
            self.core.privmsg(nick, cfg_out)
        if owner:
            conf = open(self.core.startdir + "conf/openbot.owner.commands", "r")
            for cfg in conf.readlines():
                cfg_out = self.core.confparser(cfg.strip(), nick, chan=chan)
                self.core.privmsg(nick, cfg_out)
        self.commands -= 1
        del self.commandsnick[self.commandsnick.index(nick)]

def main(core):
    " Start the Plugin and load all the needed modules "
    Core(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os", "thread"]

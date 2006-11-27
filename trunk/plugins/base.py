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
" The base  "
class Core:
    " Base answer "
    def __init__(self, core):
        " Plug to the irclib "
        self.core = core
        self.core.call("privmsg", self._on_privmsg)

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        user = user.split("!")[0]
        fromowners = self.core.channels.is_identified(user)
        if fromowners:
            # If the !quit has requested the bot disconnect with the date reason
            if message.startswith("!quit"):
                try:
                    reason = message.lstrip("!quit ")
                except:
                    reason = ""
                self.core.quit(reason)
            elif message.startswith("!join "):
                self.core.irc.join(message.lstrip("!join ").replace(" ", ""))
            elif message.startswith("!part "):
                self.core.irc.leave(message.lstrip("!part ").replace(" ", ""))
            elif message.startswith("!nick "):
                self.core.irc.setuser(message.lstrip("!nick "))
            elif message.startswith("!send "):
                send_to = message.split()
                if len(send_to) < 3:
                    self.core.privmsg(user, "Usage: !send [to] [message]")
                    return
                message = ' '.join(send_to[2:])
                self.core.privmsg(send_to[1], message)

def main(core):
    " Start the plugin "
    Core(core)

__functions__ = [main]
__revision__ = 0

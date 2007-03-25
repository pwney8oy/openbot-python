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
" The Private Message Identifier  "
class Core:
    """Wait a private message with identify: password
    """
    def __init__(self, core):
        self.core = core
        self.core.call("privmsg", self._on_privmsg)

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        user = user.split("!")[0]
        fromowners = self.core.channels.is_identified(user)
        if (not fromowners) and (message.startswith("identify: ")):
            password = message.lstrip("identify: ")
            if password == self.core.conf.password:
                self.core.channels.set_mode(channel, user, "i")
                message = "'%s' momentarily added to the owners's list" % (user)
                self.core.privmsg(user, message)

def main(core):
    " Start the plugin "
    Core(core)

__functions__ = [main]
__revision__ = 0

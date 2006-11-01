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
" SyS and Py commands plugin "
class Core:
    """You can use this plugin for exec a SyS Command, e.g. exec> uname -a
    Or a Python Command, e.g. py> print 'Hi all!!'
    The plugin works only for the owners
    """
    def __init__(self, core):
        self.core = core
        self.interpreter = code.InteractiveInterpreter()
        self.core.call("privmsg", self._on_privmsg)

    def runcode(self, codestring):
        """Run a Python code
        """
        self.output = StringIO.StringIO()
        sys.stdout, sys.stderr = self.output, self.output
        self.interpreter.runcode(codestring)
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
        return self.output.getvalue()

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        nick = user.split("!")[0]
        fromowners = self.core.channels.is_identified(nick)
        if fromowners:
            command = ""
            if message[:6] == "exec> ":
                command = commands.getoutput(message[6:])
            elif message[:4] == "py> ":
                command = self.runcode(message[4:])
            if command != "":
                for splitted_command in str(command).split("\n"):
                    self.core.privmsg(channel, splitted_command)

def main(core):
    " Start the Plugin and load all the needed modules "
    Core(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["sys", "code", "commands", "StringIO"]

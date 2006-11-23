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
" Logs plugin "
class Core:
    " Plugin for the logging "
    def __init__(self, core):
        self.core = core
        self.core.add2log = self.add2log
        for i in ["connectionLost", "signedOn", "userJoined", "kickedFrom",
                  "userKicked", "modeChanged", "nickChanged", "userRenamed",
                  "userLeft", "privmsg", "userQuit", "action"]:
            self.core.call(i, getattr(self, "_on_" + i))

    def add2log(self, log, chan="general"):
        " Function for add anything to the logs "
        ntime = time.strftime("%H:%M:%S")
        log = "%s:%s %s"% (ntime, chan, log)
        self.last_log = log
        # Se la modalita' verbose e' abilitata
        if self.core.conf.verbose:
            print log
        # Se la modalita' log e' disabilitata chiude la funzione
        if not self.core.conf.logs:
            return
        startdir = self.core.startdir
        utils.chdir("data/", startdir)
        today = time.strftime("%d-%m-%Y")
        utils.chdir("logs/", startdir + "data/")
        utils.chdir(chan + "/", startdir + "data/logs/")
        utils.write2file(log + "\n", "%s_%s" % (chan, today))
        os.chdir(startdir)

    def _on_connectionLost(self, reason):
        """Start when you get disconnected from the IRC Server
        """
        self.add2log((" Quit, Reason: %s" % (reason)).strip())

    def _on_signedOn(self):
        """Called after sucessfully signing on to the server.
        """
        port = str(self.core.conf.port)
        self.add2log((" Succerfull connected to %s:%s\n" % (
            self.core.conf.host, port)).strip())

    def _on_kickedFrom(self, channel, kicker, message):
        """Called when I am kicked from a channel.
        """
        self.add2log((" The Bot has kicked by %s: %s\n" % (
            kicker.split("!")[0], message)).strip(), channel)

    def _on_userKicked(self, kickee, channel, kicker, message):
        """Called when I observe someone else being kicked from a channel.
        """
        self.add2log((" %s has kicked %s: %s\n" % (
            kicker.split("!")[0], kickee.split("!")[0], message)).strip(),
                    channel)

    def _on_modeChanged(self, user, channel, set, modes, args):
        """Called when a channel's modes are changed
        """
        for mode in modes:
            if set:
                mode = "+" + mode
            else:
                mode = "-" + mode
            try:
                mode += " to " + args[0]
            except:
                pass
            self.add2log((" %s set: %s\n" % (user, mode)).strip(), channel)

    def _on_nickChanged(self, user):
        """Called when my user has been changed.
        """
        self.add2log((" You are now known as %s\n" % (user)).strip())

    def _on_userRenamed(self, oldname, newname):
        """A user changed their name from oldname to newname.
        """
        self.add2log((" %s is now known as %s\n" % (oldname, newname)).strip())

    def _on_userLeft(self, channel):
        """Called when I see another user leaving a channel.
        """
        self.add2log((" %s has part %s\n" % (
            user, host, channel)).strip(), channel)

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        user = user.split("!")[0]
        if channel == self.core.conf.botnick:
            channel = "private"
        self.add2log(("%s said: %s" % (user, message)).strip(), channel)

    def _on_userQuit(self, user, quitMessage):
        """Called when I see another user disconnect from the network.
        """
        self.add2log(("%s has quit (%s)" % (user, quitMessage)).strip())

    def _on_joined(self, channel):
        """Called when I finish joining a channel.
        """
        self.add2log(("You joined %s" % (channel)).strip(), channel)

    def _on_userJoined(self, user, channel):
        """Called when I see another user joining a channel.
        """
        self.add2log(("%s has joined %s" % (user, channel)).strip(), channel)

    def _on_action(self, user, channel, data):
        """Called when I see a user perform an ACTION on a channel.
        """
        user = user.split("!")[0]
        self.add2log(("%s did: %s" % (user, data)).strip(), channel)

def main(core):
    " Start the Plugin and load all the needed modules "
    Core(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os", "sys", "time", "utils"]

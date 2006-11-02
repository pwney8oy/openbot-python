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
" Bot core "
import os
import sys

from UserDict import UserDict
try:
    from twisted.words.protocols import irc
except:
    print """
WARNING: loading old twisted irc protocol
         some plugins, like google, could not work"""
    from twisted.protocols import irc
from twisted.internet import reactor, protocol
sys.path.append('library')
import utils
from channels import Channels
from conf import Config

__version__ = "0.1a"
__delay__ = 1.5

class Core(irc.IRCClient):
    versionName = "OpenBot"
    versionNum = __version__
    versionEnv = "http://projects.rebelcoders.org/"
    lineRate = __delay__

    def __init__(self, factory):
        self.nickname = factory.conf.botnick

    def connectionMade(self):
        self.handler_box = {}
        self.factory.call = self.call
        self.factory.irc = self
        self.factory.quit = self.disconnect
        self.channels = self.factory.channels
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def call(self, event, function):
        if getattr(self, event) != None:
            if self.handler_box.has_key(event):
                self.handler_box[event].append(function)
            else:
                self.handler_box[event] = [function]

    def connect(self, event, args=None):
        if self.handler_box.has_key(event):
            for function in self.handler_box[event]:
                if args != None:
                    function(*args)
                else:
                    function()

    def disconnect(self, reason="Requested"):
        """Start when you get disconnected from the IRC Server
        """
        self.factory.disconnection = True
        self.quit(reason)

    def privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        self.connect("privmsg", (user, channel, message))

    def joined(self, channel):
        """Called when I finish joining a channel.

        channel has the starting character (# or &) intact.
        """
        self.channels.add_channel(channel)
        self.connect("joined", (channel))

    def left(self, channel):
        """Called when I have left a channel.

        channel has the starting character (# or &) intact.
        """
        self.connect("left", (channel))

    def noticed(self, user, channel, message):
        """Called when I have a notice from a user to me or a channel.

        By default, this is equivalent to IRCClient.privmsg, but if your
        client makes any automated replies, you must override this!
        From the RFC::

            The difference between NOTICE and PRIVMSG is that
            automatic replies MUST NEVER be sent in response to a
            NOTICE message. [...] The object of this rule is to avoid
            loops between clients automatically sending something in
            response to something it received.
        """
        self.connect("noticed", (user, channel, message))

    def modeChanged(self, user, channel, set, modes, args):
        """Called when a channel's modes are changed

        @type user: C{str}
        @param user: The user and hostmask which instigated this change.

        @type channel: C{str}
        @param channel: The channel for which the modes are changing.

        @type set: C{bool} or C{int}
        @param set: true if the mode is being added, false if it is being
        removed.

        @type modes: C{str}
        @param modes: The mode or modes which are being changed.

        @type args: C{tuple}
        @param args: Any additional information required for the mode
        change.
        """
        try:
            changed_to = args[0]
            nick = user.split("!")[0]
            for mode in modes:
                args = (channel, changed_to, mode)
                if set:
                    self.channels.set_mode(*args)
                else:
                    self.channels.clear_mode(*args)
        except:
            pass
        self.connect("modeChanged", (user, channel, set, modes, args))

    def pong(self, user, secs):
        """Called with the results of a CTCP PING query.
        """
        self.connect("pong", (user, secs))

    def signedOn(self):
        """Called after sucessfully signing on to the server.
        """
        ##
        self.factory.start()
        ##
        if self.factory.conf.ns_password != None:
            self.msg("NickServ", "identify " + self.factory.conf.ns_password)
        self.join(self.factory.conf.chans)
        self.connect("signedOn")

    def kickedFrom(self, channel, kicker, message):
        """Called when I am kicked from a channel.
        """
        self.connect("kickedFrom", (channel, kicker, message))

    def nickChanged(self, nick):
        """Called when my nick has been changed.
        """
        self.factory.conf.botnick = nick
        print nick
        self.connect("nickChanged", (nick))

    ### Things I observe other people doing in a channel.

    def userJoined(self, user, channel):
        """Called when I see another user joining a channel.
        """
        self.channels.add_user(channel, user.split("!")[0])
        self.connect("userJoined", (user, channel))

    def userLeft(self, user, channel):
        """Called when I see another user leaving a channel.
        """
        self.channels.remove_user(channel, user.split("!")[0])
        self.connect("userLeft", (user, channel))

    def userQuit(self, user, quitMessage):
        """Called when I see another user disconnect from the network.
        """
        self.channels.remove_user(".all.", user.split("!")[0])
        self.connect("userQuit", (user, quitMessage))

    def userKicked(self, kickee, channel, kicker, message):
        """Called when I observe someone else being kicked from a channel.
        """
        self.channels.remove_user(channel, kickee.split("!")[0])
        self.connect("userKicked", (kickee, channel, kicker, message))

    def action(self, user, channel, data):
        """Called when I see a user perform an ACTION on a channel.
        """
        self.connect("action", (user, channel, data))

    def topicUpdated(self, user, channel, newTopic):
        """In channel, user changed the topic to newTopic.

        Also called when first joining a channel.
        """
        self.connect("topicUpdated", (user, channel, newTopic))

    def userRenamed(self, oldname, newname):
        """An user changed his name from oldname to newname.
        """
        self.channels.change_nick(oldname, newname)
        self.connect("userRenamed", (oldname, newname))

    def irc_RPL_NAMREPLY(self, prefix, params):
        """Collect usernames from this channel.
        """
        channel = params[2]
        for name in params[3].split():
            # Remove operator, half-operator and voice prefixes
            if name[0] in ("@", "%", "+"):
                mode = name[0].replace("@", "o").replace("%", "h").replace("+",
                                                                           "v")
                name = name[1:]
                self.channels.set_mode(channel, name, mode)
            self.channels.add_user(channel, name)

    ### Information from the server.

    def receivedMOTD(self, motd):
        """I received a message-of-the-day banner from the server.

        motd is a list of strings, where each string was sent as a seperate
        message from the server. To display, you might want to use::

            string.join(motd, '\\n')

        to get a nicely formatted string.
        """
        self.connect("receivedMOTD", (motd))


class OpenBot(protocol.ClientFactory):
    " Start the bot, load the config file, start the plugins, etc."
    protocol = Core

    def __init__(self):
        self.conf = Config()
        self.channels = Channels()
        self.delay = __delay__
        self.version = __version__
        self.ENCODING = "utf-8"
        self._replacer, self._endreplacer = utils._replacer, utils._endreplacer
        self.chan = []
        self.startdir = os.getcwd()+"/"
        self.disconnection = False
        self.connect()
        os.chdir(self.startdir)

    def buildProtocol(self, addr):
        protocol = self.protocol(self)
        protocol.factory = self
        return protocol

    def privmsg(self, channel, message):
        self.add2log("The Bot say: %s" % (message), channel)
        self.irc.msg(channel, message)

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        if not self.disconnection:
            connector.connect()
        else:
            reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()

    def connect(self):
        """ Connect to the IRC Server
        """
        reactor.connectTCP(self.conf.host, self.conf.port, self)
        reactor.run()

    def start(self):
        " Load all plugins and give to it global variables "
        utils.load_plugins(self.startdir, self)

if __name__ == "__main__":
    OpenBot()

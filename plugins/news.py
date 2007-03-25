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
" The news Plugin  "
class Core:
    " Get the last news "
    def __init__(self, core):
        self.core = core
        self.core.call("privmsg", self._on_privmsg)

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        def call(url, name):
            name += " :: "
            if require:
                result = utils.get_one_rss(url, require-1, name, feedparser)
            else:
                result = utils.get_rss(url, name, feedparser)
            result = result.encode("utf-8")
            if len(result) > 433:
                result = result[:430] + "..."
            self.core.privmsg(channel, result)
        message = message.split()
        RSS = {"slashdot":"http://rss.slashdot.org/Slashdot/slashdot",
               "ziobudda":"http://www.ziobudda.net/headlines/ziobudda.xml", 
               "distrowatch":"http://distrowatch.com/news/dwd.xml",
               "gp2x":"http://www.gp32x.com/board/index.php?act=rssout&id=3",
               "games":"http://happypenguin.org/html/news.rdf",
               "games2":"http://www.linux-gamers.net/backend.php",
               "osnews":"http://osnews.com/files/recent.rdf"}
        if len(message) > 2:
            try:
                require = int(message[2])
            except ValueError:
                require = False
        else: require = False
        if (len(message) > 1) and (message[0].lower() == "!news"):
            message[1] = message[1].lower()
            if RSS.has_key(message[1]):
                call(RSS[message[1]], message[1])
            else:
                self.core.privmsg(channel, "Valid !news arguments are: %s" % (
                    ', '.join(RSS.keys())))
        else: return

def main(core):
    " Start the Plugin and load all the needed modules "
    Core(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["feedparser", "utils"]

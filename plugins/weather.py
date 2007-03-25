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
" The weathers news Plugin  "
class Core:
    " Get the last weathers news "
    def __init__(self, core):
        self.core = core
        self.core.call("privmsg", self._on_privmsg)

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        def call(url, name):
            url = "http://xml.weather.yahoo.com/forecastrss?p=" + url + "&u=f"
            name += " :: "
            result = utils.get_one_rss(url, 0, name, feedparser)
            result = result.encode("utf-8")
            dictionary = {"<b>":"", "</b>":"", "<br />":"", "\n":""}
            for ranged in range(0, 50):
                string = "<img src=\"http://us.i1.yimg.com/us.yimg.com/i/us/we/52/%s.gif\" />"%ranged
                dictionary[string] = ""
            result = utils._replacer(dictionary, result).split("<a href")[0]
            if len(result) > 433:
                result = result[:430] + "..."
            self.core.privmsg(channel, result)
        message = message.split()
        RSS = {"roma":"ITXX0067", "milano":"ITXX0090", "napoli":"ITXX0052",
               "palermo":"ITXX0055", "aosta":"ITXX0103", "catania":"ITXX0017",
               "reggiocalabria":"ITXX0097", "genova":"ITXX0031", 
               "amsterdam":"NLXX0002", "parigi":"FRXX0076", "madrid":"SPXX0050", 
               "perugia":"ITXX0136", "potenza":"ITXX0139", "l'aquila":"ITXX0105", 
               "bari":"ITXX0003", "bologna":"ITXX0006", "cagliari":"ITXX0010", 
               "torino":"ITXX0081"}
        if (len(message) > 1) and (message[0].lower() == "!weather"):
            message[1] = message[1].lower()
            if RSS.has_key(message[1]):
                call(RSS[message[1]], message[1])
            else:
                self.core.privmsg(channel, "Valid !weather arguments are: %s" % (
                    ', '.join(RSS.keys())))
        else: return

def main(core):
    " Start the Plugin and load all the needed modules "
    Core(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["feedparser", "utils"]

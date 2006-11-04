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
" Quote Plugin "

class Core:
    """ Fun plugin for quote
    !quote MSG for add a quote
    !rquote for get a random quote
    !gquote NUM for get a quote
    !dquote NUM for delete a quote"""
    def __init__(self, core):
        self.core = core
        self.core.call("privmsg", self._on_privmsg)
        self.quote_file = self.core.startdir+"data/quote"

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        nick = user.split("!")[0]
        fromowners = self.core.channels.is_identified(nick)
        # Se è stato inserito !quit il bot si disconnette con il motivo dato
        # Se non è stato dato un motivo userà quello di default: Requested
        message = message.split()
        if message[0] == "!quote":
            # Add a quote message in data/quote
            try:
                quote = ' '.join(message[1:])
            except:
                return
            if not os.path.exists(self.quote_file):
                open_quote = open(self.quote_file, "w")
                open_quote.close()
            open_quote = open(self.quote_file, "a")
            open_quote.write(quote+"\n")
            open_quote.close()
        elif message[0] in ("!rquote", "!gquote", "!dquote"):
            if os.path.exists(self.quote_file):
                open_quote = open(self.quote_file, "r")
            get_quote = open_quote.readlines()
            if (message[0] == "!rquote") and (len(get_quote) > 0):
                # Return a random quote from data/quote
                get_quote = get_quote[random.randrange(0, len(get_quote))]
                open_quote.close()
            elif (message[0] == "!dquote") and (fromowners):
                # Delete a quote from data/quote, only for the owner
                try:
                    quote_num = int(message[1])
                except ValueError:
                    quote_num = 0
                if len(get_quote) < quote_num:
                    return
                quote = get_quote[:quote_num]
                if len(get_quote) != quote_num:
                    quote += get_quote[quote_num+1:]
                open_quote.close()
                save_quote = open(self.quote_file, "w")
                save_quote.write(' '.join(quote))
                save_quote.close()
                return
            elif message[0] == "!gquote":
                # Return a quote from data/quote
                try:
                    get_quote = get_quote[int(message[1].strip().split()[0])]
                except:
                    return
                open_quote.close()
            if (get_quote != "") and (type(get_quote) == type("")):
                self.core.privmsg(channel, get_quote.strip())

def main(core):
    " Start the Plugin and load all the needed modules "
    Core(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os", "random"]

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
" Google Plugin"
class Core:
    " Check a word on google "
    def __init__(self, core):
        self.core = core
        self.core.call("userLeft", self._on_userLeft)
        self.core.call("privmsg", self._on_privmsg)

    def make_seen_string(self, user, channel):
        full_date = time.strftime("%d/%m/%Y")
        full_time = time.strftime("%H:%M")
        return "%s %s %s %s\n"%(channel, user, full_date, full_time)

    def append_to_config(self, user, channel):
        string = self.make_seen_string(user, channel)
        utils.write2file(string, "seen")

    def parse_file(self, user):
        read = utils.open_file("seen", True)
        if not read:
            return ""
        else:
            result = ""
            for line in read:
                if line.split()[1] != user:
                    result += line
            return result

    def seen_system(self, user, channel):
        startdir = self.core.startdir
        utils.chdir("data/", startdir)
        parsed_file = self.parse_file(user)
        if parsed_file != "":
            os.remove("seen")
        utils.write2file(parsed_file, "seen")
        self.append_to_config(user, channel)
        os.chdir(startdir)

    def search(self, user):
        read = utils.open_file("seen", True)
        if not read:
            return ""
        else:
            result = ""
            for line in read:
                line = line.split()
                if line[1] == user:
                    result = "I saw %s in %s on %s at %s"%(user, line[0],
                                                           line[2], line[3])
            return result

    def _on_userLeft(self, user, channel):
        """Called when I see another user leaving a channel.
        """
        self.seen_system(user, channel)

    def _on_privmsg(self, user, channel, message):
        """Called when I have a message from a user to me or a channel.
        """
        user = user.split("!")[0]
        if message.startswith("!seen"):
            seen_user = message.split()[1]
            user_channels = self.core.channels.get_users_channels(seen_user)
            if seen_user == user:
                result = "I'm Mandrake, and who are you?"
            elif seen_user == self.core.conf.botnick:
                result = "Don't joke me dude..."
            elif len(user_channels) != 0:
                result = "%s is online (%s)"%(seen_user,
                                              ', '.join(user_channels))
            else:
                startdir = self.core.startdir
                utils.chdir("data/", startdir)
                result = self.search(seen_user)
                if result == "":
                    result = "I never saw %s..."%seen_user
                os.chdir(startdir)
            self.core.privmsg(channel, result)

def main(core):
    " Start the Plugin and load all the needed modules "
    Core(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os", "time", "utils"]

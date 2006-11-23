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
" Peak Plugin"
class Core:
    " Peak all chan "
    def __init__(self, core):
        self.core = core
        self.core.call("userJoined", self._on_userJoined)

    def _on_userJoined(self, user, channel):
        """Called when I see another user joining a channel.
        If there is a new peak save it
        """
        nick = user.split("!")[0]
        peakdir = self.core.startdir+"data/peak"
        lastpeak = 0
        usersnumber = 0
        if self.core.channels.is_in(channel):
            users = self.core.channels.users(channel)
            usersnumber = len(users)
            if self.core.conf.botnick not in users:
                usersnumber += 1
        if not os.path.exists(self.core.startdir+"data/"):
            os.mkdir(self.core.startdir+"data/")
        # Se il file di peak gia' esiste
        if os.path.exists(peakdir):
            # Apre il file di peak (data/peak)
            try:
                opendata = open(peakdir, "r")
                # Avvia un ciclo che legge il file di peak
                # Se il canale corrente e' gia' stato inserito:
                #  inserisce l'ultimo peak in lastpeak
                for line in opendata.readlines():
                    line = line.strip().split("=")
                    if line[0] == channel:
                        lastpeak = line[1]
                opendata.close()
            except IOError, (errno, strerror):
                lastpeak = 0
        # Se il numero di utenti al momento e' piu' grande del penultimo peak
        if int(lastpeak) < usersnumber:
            # Carica il file
            newpeak = ""
            new = True
            if os.path.exists(peakdir):
                opendata = open(peakdir, "r")
                # Avvia un ciclo che legge il file di peak
                # Se il canale corrente e' gia' stato inserito:
                #  scrive nella var newpeak il canale=ultimopeak
                # Altrimenti se non e' questo canale lo riscrive in newpeak
                for line in opendata.readlines():
                    xchan = line.split("=")[0].strip()
                    if xchan == channel:
                        new = False
                        newpeak += "%s=%s\n"% (xchan, str(usersnumber))
                    else:
                        newpeak += line
                opendata.close()
            # Se il canale non e' gia' stato inserito nel peak
            if new:
                newpeak += "%s=%s\n"% (channel, str(usersnumber))
            # Se il canale non e' gia' stato inserito nel peak
            if newpeak != "":
                # Scrive da 0 il file peak
                savedata = open(peakdir, "w")
                savedata.write(newpeak)
                savedata.close()
            # Informa in chan del nuovo peak
            peak_message = "New peak of %s users, thank to %s" % (
                str(usersnumber), nick)
            self.core.add2log(peak_message, channel)
            self.core.privmsg(channel, peak_message)

def main(core):
    " Start the Plugin and load all the needed modules "
    Core(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os"]

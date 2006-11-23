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
" ConfParser Plugin "
class ConfParser:
    " Plugin for the parsing of the confing files "
    def __init__(self, core):
        self.core = core
        self.core.confparser = self.confparser
        self.uptime = time.time()

    def chan_stats(self, stat):
        stat.sort()
        return ", ".join(stat), self.core._endreplacer(stat), len(stat)

    def confparser(self, cfg_out, nick, chan="", msg="", host=""):
        " The base confparser function "
        # .from. viene cambiato con il nick della persona che e' entrata in chan
        #   oppure con il nick della persona che ha scritto il messaggio
        # .botnick. viene cambiato col nick del bot
        # .chan. viene cambiato col chan corrente
        # .hours. .minutes. .seconds. ecc.
        # .uptime_hours/minutes/secondes.
        #   viene cambiato con il tempo passato dall'avvio del Bot
        hms = time.strftime("%H.%M.%S").split(".")
        dmy = time.strftime("%d.%m.%y").split(".")
        owners = ' '.join(self.core.channels.identified())
        uptime = time.localtime(time.time()-self.uptime)
        uptime = (str(uptime[3]-1), str(uptime[4]), str(uptime[5]))
        dictionary = {".from.":nick, ".botnick.":self.core.conf.botnick,
                      ".chan.":chan, ".hours.":hms[0], ".seconds.":hms[2],
                      ".minutes.":hms[1], ".day.":dmy[0], ".month.":dmy[1],
                      ".year.":dmy[2], ".owner.":owners,
                      ".uptime_hours.":uptime[0], ".uptime_minutes.":uptime[1],
                      ".uptime_seconds.":uptime[2]}
        cfg_out = self.core._replacer(dictionary, cfg_out)
        peakdir = self.core.startdir+"data/peak"
        if os.path.exists(peakdir):
            try:
                opendata = open(peakdir, "r")
                lastpeak = ""
                for line in opendata.readlines():
                    line = line.strip().split("=")
                    if line[0] == chan:
                        lastpeak = line[1]
                opendata.close()
                if lastpeak == "":
                    lastpeak = "No peak found for %s"% (chan)
                # .peak. lo cambia col peak del chan corrente
                cfg_out = cfg_out.replace(".peak.", str(lastpeak))
            except IOError, (errno, strerror):
                self.core.add2log("I/O error %s(%s): %s" % (peakdir, errno, 
                                                            strerror), chan)
        if self.core.channels.is_in(chan):
            chans = self.core.channels
            users, users_, users_number = self.chan_stats(chans.users(chan))
            opers, opers_, opers_number = self.chan_stats(chans.opers(chan))
            halfop, halfop_, halfop_number = self.chan_stats(chans.halfop(chan))
            voiced, voiced_, voiced_number = self.chan_stats(chans.voiced(chan))
            dictionary = {".users.":users, ".users_.":users_, ".opers.":opers, 
                          ".users_number.":users_number, ".opers_.":opers_,
                          ".opers_number.":opers_number, ".halfop.":halfop,
                          ".halfop_.":halfop_, ".halfop_number.":halfop_number,
                          ".voiced.":voiced, ".voiced_.":voiced_,
                          ".voiced_number.":voiced_number}
            cfg_out = self.core._replacer(dictionary, cfg_out)
        return cfg_out

def main(core):
    " Start the Plugin and load all the needed modules "
    ConfParser(core)

__functions__ = [main]
__revision__ = 0
__call__ = ["os", "time"]

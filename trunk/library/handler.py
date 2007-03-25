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
"""
 *** Still not used in OpenBot ***
"""
from utils import messages as send
send = send()
base = {}

class add:
    def __init__(self):
        send.system("PHandler's add class is loading...")
    def init(self, name, receiver):
        if base.has_key(name):
            warning("%s was handled before, replacing it" % name)
        base[name] = receiver

class remove:
    def __init__(self):
        send.system("PHandler's remove class is loading...")
    def init(self, name):
        if base.has_key(name):
            base.remove(name)
            return 1
        else:
            warning("%s isn't in the handler's list" % name)
            return 0

class call:
    def __init__(self):
        send.system("PHandler's call class is loading...")
    def init(self, name, *datas):
        if base.has_key(name):
            base[name](*datas)
            return 1
        else:
            warning("%s isn't in the handler's list" % name)
            return 0

class Core:
    add = add().init
    remove = remove().init
    call = call().init
    def __init__(self):
        send.system("PHandler succerfull loaded")

#if __name__ == "__main__":
def test(message):
    print message
core = Core()

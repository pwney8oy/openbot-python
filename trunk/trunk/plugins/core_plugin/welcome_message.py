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
" Welcome Message Plugin "
class welcome_message:
    " Print the Welcome Message "
    def __init__(self, core):
        self.core = core
        print self.message()

    def message(self):
        " Return the Welcome Message "
        return """

                                        _|                    _|
  _|_|    _|_|_|      _|_|    _|_|_|    _|_|_|      _|_|    _|_|_|_|
_|    _|  _|    _|  _|_|_|_|  _|    _|  _|    _|  _|    _|    _|
_|    _|  _|    _|  _|%s    _|    _|  _|    _|  _|    _|    _|
  _|_|    _|_|_|      _|_|_|  _|    _|  _|_|_|      _|_|        _|_|
          _|
          _|


""" % (self.core.version)
def main(core):
    " Start the Plugin "
    welcome_message(core)

__functions__ = [main]
__revision__ = 0

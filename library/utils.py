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
" Bot utils "
import os
import sys

module = {}

class messages:
    def __init__(self):
        self.set_stdout(None)
    def set_stdout(self, stdout):
        self.stdout = stdout
    def normal(self, message):
        data = "[--] %s" % message
        if self.stdout != None:
            self.stdout(data)
            return
        print data
    def warning(self, message):
        data = "[Warning] %s" % message
        if self.stdout != None:
            self.stdout(data)
            return
        print "[Warning] %s" % message
    def error(self, message):
        data = "[ERROR] %s" % message
        if self.stdout != None:
            self.stdout(data)
            return
        print "[ERROR] %s" % message
    def system(self, message):
        data = "[**] %s" % message
        if self.stdout != None:
            self.stdout(data)
            return
        print "[**] %s" % message
send = messages()

def _add_conf(conf_file, *args):
    old_conf = ""
    if os.path.exists(conf_file):
        open_file = open(conf_file, "r")
        for line in open_file.readlines():
            line = line.split("=", len(args)-1)
            if args[0] != line[0]:
                old_conf += '='.join(line)
        open_file.close()
    open_file = open(conf_file, "w")
    open_file.write(old_conf + '='.join(args) + "\n")
    open_file.close()

def _conf_parser(conf_file, args_for_value=1):
    """
    conf_file = string with file to open
    [args_for_value] = int with numbers of max args for value (0 for no limit)
    """
    openconf = open(conf_file, "r") # Apre il file di conf
    conf_list = []
    for conf in openconf.readlines():
        # Se la linea e' commentata la ignora
        # Prende tutti i dati dal file di conf
        if (args_for_value) and (not conf.startswith("#")):
            conf_list.append(conf.strip("\n").split("=", args_for_value))
        elif (not args_for_value) and (not conf.startswith("#")):
            conf_list.append(conf.strip("\n").split("="))
    openconf.close()
    return conf_list

def _endreplacer(start_string, string2add="_"):
    """ Data lista di stringhe (start_string)
    Ad ogni stringa aggiunge string2add prima dell'ultima parola
    """
    end_string = []
    for string2edit in start_string:
        end_string.append(string2edit[:-2] + string2add + string2edit[-1])
    return ', '.join(end_string)

def _replacer(dictionary, string2edit):
    for to_replace in dictionary.keys():
        string2edit = string2edit.replace(str(to_replace),
                                          str(dictionary[to_replace]))
    return string2edit

def _get_input(answer, conditions=0, type="raw_input"):
    """
    Usage:
      _get_input ( answer , [conditions] , [type] )
    Example:
      _get_input ( "0 is 0?" , "a == 'yes'" )
        will return ['yes', True] or [userinput, False]
    Example2:
      _get_input ( "Your name?" )
        will return [userinput, False]
    """
    if type == "raw_input":
        userinput = a = raw_input(str(answer))
        try:
            if eval(conditions) not in [True, False]:
                conditions = False
            else:
                conditions = eval(conditions)
        except:
            conditions = False
        return [userinput, conditions]

def get_one_rss(url, number, rss_name, feedparser):
    rss = feedparser.parse(url)
    entry = rss.entries[number]
    result = rss_name
    try:
        result += "%s: %s" % (entry.title, entry.description)
    except:
        result += "%s: no description found" % (entry.title)
    return result

def get_rss(url, rss_name, feedparser):
    rss = feedparser.parse(url)
    entries = rss.entries[0:5]
    cont, result = 0, rss_name
    for entry in entries:
        cont += 1
        result += "%s (%s)" % (entry.title, cont)
        if cont != 5:
            result += " - "
    return result

def walk():
    " Walk the plugins directory, then set self.plugins with all .py files "
    global plugins
    for root, dirs, files in os.walk("plugins", topdown=False):
        for name in files:
            if name.split(".")[-1] == "py":
                plugins.append(root+"/"+name)
        for name in dirs:
            try:
                if name != ".svn":
                    os.chdir(name)
                    walk()
            except:
                pass
def chdir(directory, startdir):
    """ If the given directory don't exists:
    Create it
    After that:
    Enter it
    """
    os.chdir(startdir)
    if not os.path.exists(directory):
        os.mkdir(directory)
    os.chdir(directory)

def write2file(data, file):
    """ Date a string (data) and a file name (file)
    If the file don't exists create it
    Then write data in the file"""
    if not os.path.exists(file):
        read = open(file, "w")
        read.close()
    save = open(file, "a")
    save.write(data)
    save.close()

def open_file(file, read_lines=False):
    if os.path.exists(file):
        read = open(file, "r")
        if read_lines:
            result = read.readlines()
        else:
            result = read.read()
        read.close()
        return result
    else:
        return False

def _import_(library):
    """ Load a module
    If a plugin demands a module that is already loaded:
    Don't load it again
    Else:
    Load the module"""
    global module
    if library in module:
        return module[library]
    else:
        module[library] = __import__(library)
        return module[library]

def load_plugins(startdir, self):
    global plugins
    plugins = []
    walk()
    send.system("Loading Plugins...")
    for plugin in plugins:
        sys.path.append(startdir+os.path.split(plugin)[0])
        plugin_name = os.path.split(plugin)[1].replace(".py", "")
        send.set_stdout(sys.stdout.write)
        send.system("Plugin: " + plugin_name)
        plugin = __import__(plugin_name)
        try:
            for module in plugin.__call__:
                setattr(plugin, module, _import_(module))
        except:
            pass
        try:
            for function in plugin.__functions__:
                function(self)
            sys.stdout.write(" [OK]\n")
        except:
                sys.stdout.write(" [FAILED]\n")
        send.set_stdout(None)
    os.chdir(startdir)
 
def _create_get_property(property_name):
    def _property_get(self):
        return getattr(self, "_"+property_name)
    return _property_get
 
def _create_set_property(property_name):
    def _property_set (self, value):
        setattr(self, "_"+property_name, value)
    return _property_set
 
def create_property(property_name):
      locals = sys._getframe(1).f_locals
      locals[property_name] = property(
          _create_get_property(property_name),
          _create_set_property(property_name))

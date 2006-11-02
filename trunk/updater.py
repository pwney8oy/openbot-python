import os
import time
import urllib

def openurl(url):
    urlopen = urllib.urlopen("http://initd.org/svn/rebelcoders/OpenBot/" + url)
    file = url.split("/")[-1]
    if os.path.exists(file):
        os.remove(file)
    filesaver = open(file, "w")
    filesaver.write(urlopen.read())
    filesaver.close()
    time.sleep(0.005)

def mkdir(path):
    if not os.path.exists(path):
        print "- Creating %s directory..."% (path)
        os.mkdir(path)
    os.chdir(path)

print "- Downloading openbot core..."
openurl("openbot.py")
openurl("openbot.tac")
openurl("channels.py")
openurl("conf.py")


mkdir("library")

print "- Downloading Libraries..."
openurl("library/feedparser.py")
openurl("library/utils.py")


os.chdir("..")

mkdir("conf")

print "- Downloading conf files...."
openurl("conf/openbot.commands")
openurl("conf/openbot.join")
openurl("conf/openbot.manual")
openurl("conf/openbot.modes")
openurl("conf/openbot.owner.commands")
openurl("conf/openbot.owner.manual")


os.chdir("..")

mkdir("plugins")

print "- Downloading plugins..."
openurl("plugins/base.py")
openurl("plugins/google.py")
openurl("plugins/news.py")
openurl("plugins/logs.py")
openurl("plugins/peak.py")
openurl("plugins/quote.py")
openurl("plugins/private_identifier.py")
openurl("plugins/syscmd.py")
openurl("plugins/seen.py")

mkdir("core_plugin")
openurl("plugins/core_plugin/confparser.py")
openurl("plugins/core_plugin/welcome_message.py")

os.chdir("..")
mkdir("conf_reader")
openurl("plugins/conf_reader/_commands.py")
openurl("plugins/conf_reader/join.py")
openurl("plugins/conf_reader/manual.py")
openurl("plugins/conf_reader/modes.py")

os.chdir("../..")
mkdir("data")

print "- Installation finished, run openbot.py with Python for use it"

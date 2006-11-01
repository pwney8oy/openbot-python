from twisted.application import service
import openbot
application = service.Application('openbot')
openbot.OpenBot()

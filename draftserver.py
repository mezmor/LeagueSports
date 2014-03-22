import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LeagueSports.settings")

from django.contrib.sessions.models import Session
from drafter.models import ConnectionTicket
 

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        cookie = self.request.headers.get('cookie')
        split_cookie = cookie.split(';')
        sessionIndex = [index for index, data in enumerate(split_cookie) if "sessionid" in data]
        sessionid = split_cookie[sessionIndex[0]].split("=")[1]
        print sessionid
        print 'new connection'
      
    def on_message(self, message):
        data = message.split(":")
        print 'data received: %s' % data
        if len(data) < 2:
            return
        if data[0] == 'session':
            session = Session.objects.get(session_key=data[1])
            print "Session: " + str(session)
            self.write_message('Data Found!')
        if data[0] == 'ticket':
            ticket = ConnectionTicket.objects.get()
            print "Ticket: " + str(ticket)
 
    def on_close(self):
        print 'connection closed'
        
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
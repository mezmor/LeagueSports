import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LeagueSports.settings")

from django.contrib.sessions.models import Session
 

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
      
    def on_message(self, message):
        print 'message received: %s' % message
        if message.startswith('session'):
            data = message.split(":")
            print data
            session = Session.objects.get(session_key=data[1])
            print session.expire_date
            self.write_message('Data Found!')
 
    def on_close(self):
        print 'connection closed'
        
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
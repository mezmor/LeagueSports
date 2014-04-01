import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LeagueSports.settings")

from django.contrib.sessions.models import Session
from drafter.models import ConnectionTicket

from types import NoneType

connection_buffer = []
connections = {}
 
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        """
        To validate a connection we take the cookie's sessionid and query for its ConnectionTicket
        If there is no cookie, close the connection
        If there is no sessionid, close the connection
        If there is no session associated with the sessionid, close the connection
        If there is no ConnectionTicket, close the connection
        Otherwise delete the ConnectionTicket and add the connection the appropriate pool
        """
        # First get the session id from the cookie
        cookie = self.request.headers.get('cookie')
        if cookie is NoneType:
            self.close()
        split_cookie = cookie.split(';')
        sessionIndex = [index for index, data in enumerate(split_cookie) if "sessionid" in data]
        if len(sessionIndex) == 0:
            self.close()
        sessionid = split_cookie[sessionIndex[0]].split("=")[1]
        
        print "Getting sessionid: " + sessionid
        # Check if session id exists
        try:
            session = Session.objects.get(session_key=sessionid)
            print "Session get successful"
        except Session.DoesNotExist:
            print "Session get failed"
            self.close()
        
        print "Getting ticket"
        # Check if there is a ConnectionTicket with the associated sessionid, if not close
        try:
            ticket = ConnectionTicket.objects.get(user_sessionid=session.session_key)
            self.user = ticket.user # Keep a reference to the current user
            print "Ticket get successful"
        except ConnectionTicket.DoesNotExist:
            print "Ticket get failed"
            self.close()
            
        # Clear out the ticket and append this connection to the connection buffer
        ticket.delete()
        connection_buffer.append(self)
        
        print 'new connection'
      
    def on_message(self, message):
        data = message.split("::")
        print 'data received: %s' % data
        if len(data) < 2:
            return
        
        if data[0] == 'league':
            if self not in connection_buffer:
                return
            self.leagueid = data[1] # Keep a reference to the current leagueid
            try:
                connections[self.leagueid].append(self)
            except KeyError:
                connections[self.leagueid] = [self]
            connection_buffer.remove(self)
            print "Added connection to pool: " + str(connections)
            
            message = "join::" + str(self.user.username)
            for connection in connections[self.leagueid]:
                if connection is not self:
                    connection.write_message(message)
                self.write_message("join::"+str(connection.user.username))
        
        if data[0] == 'join':
            session = Session.objects.get(session_key=data[1])
            print "Session: " + str(session)
            self.write_message('Data Found!')
 
    def on_close(self):
        # Remove this connection from the connections pool
        message = "leave::" + str(self.user.username)
        for connection in connections[self.leagueid]:
            if connection is not self:
                connection.write_message(message)
        connections[self.leagueid].remove(self)
        print 'connection closed'
        
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    
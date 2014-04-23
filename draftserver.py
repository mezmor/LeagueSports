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
        If there is no sessionid in the cookie, close the connection
        If there is no session associated with the sessionid, close the connection
        If there is no ConnectionTicket, close the connection
        Otherwise delete the ConnectionTicket and add the connection the appropriate pool
        """
        # First get the session id from the cookie
        cookie = self.request.headers.get('cookie')
        if cookie is NoneType:
            self.close()
            
        # Check for sessionid in cookie
        cookie_dict = dict(item.split("=") for item in cookie.split(";"))
        if not "sessionid" in cookie_dict.keys():
            self.close()
        
        if cookie_dict.get("sessionid") is NoneType:
            print "ERROR sessionid not in cookie"
            print cookie_dict
            self.close()
        
        sessionid = cookie_dict.get("sessionid") # Sometimes Malfunctioning in Incognito mode
        
        # Check if session id exists
        print "Getting sessionid: " + sessionid
        try:
            session = Session.objects.get(session_key=sessionid)
            print "Session get successful"
        except Session.DoesNotExist:
            print "Session get failed"
            self.close()
        
        # Check if there is a ConnectionTicket with the associated sessionid, if not: close
        print "Getting ticket"
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
        # If we receive league data, the connection should be in the connection buffer
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
            
            # Notify all connections in the pool of the new connection
            # Notify the new connection of all the connections in the pool
            message = "join::" + str(self.user.username)
            for connection in connections[self.leagueid]:
                if connection is not self:
                    connection.write_message(message)
                self.write_message("join::"+str(connection.user.username))
        
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
    
from enum import Enum
from collections import deque
import constants
import actor
import command
import sessionmanager

class Session:

    def __init__(self, sock, addr, session_mgr ):
        self.id = ""
        self.sock = sock
        self.addr = addr
        self.session_mgr = session_mgr
        self.state = SessionState.UNAUTHENTICATED
        self.inbound_message_queue = deque()
        self.outbound_message_queue = deque()
        self.incoming_data = ""
        self.actor = actor.Actor()

    def send( self, data):
        try:
            #print( data )
            self.outbound_message_queue.append( data )
        except ConnectionResetError as cre : 
            # Need to inform session manager of error
            print(" ConnectionResetError" )
            self.session_mgr.handle_disconnect( self.sock )

    def handle_data( self, data ):
        # Add to the incoming data and then parse for complete messages
        encoded_data = data.decode("utf-8")
        #print( self.addr[0] + " > " + encoded_data )
        self.incoming_data = self.incoming_data + encoded_data
        self.process_data()

    def send_messages( self ):
        for msg in self.outbound_message_queue:
            try:
                terminated_msg = msg + constants.MESSAGE_TERMINATOR
                encoded_msg = terminated_msg.encode("utf-8")
                self.sock.send( encoded_msg )
            except Exception as ex:
                print("Error sending message ", ex ) 
        
        self.outbound_message_queue.clear()

    def process_data( self ):
        # Check incoming data for terminator
        while self.incoming_data.find( constants.MESSAGE_TERMINATOR ) > -1 :
            msgs = self.incoming_data.split( constants.MESSAGE_TERMINATOR, 1 )
            if len(msgs) == 0:
                continue

            if self.state == SessionState.UNAUTHENTICATED:
                # This better be a token
                parts = msgs[0].split(":")
                if len(parts) != 2 or parts[0] != "Token" :
                    continue
                # This is where we'd do some actual authentication
                self.id = parts[1]
                self.actor.id = self.id
                self.actor.pos_x = 2
                self.actor.pos_z = 2
                self.state = SessionState.READY
                self.incoming_data = ""
                self.outbound_message_queue.append( "SessionReady" )
                self.session_mgr.notify_others_of_arrival( self )                

            else :
                self.inbound_message_queue.append( command.Command(msgs[0], self ) )
                self.incoming_data = msgs[1]

class SessionState( Enum ):
    UNAUTHENTICATED = 1
    READY = 2
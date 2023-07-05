import select
import session
import constants
import time

class SessionManager:
    def __init__( self, server ):
        self.server = server
        self.session_table = dict()
        self.read_ready = []
        self.write_ready = []

    def create_session( self, sock, addr ) :
        sess = session.Session( sock, addr, self )
        return sess
    
    def handle_disconnect( self, sock ) :
        removedId = self.session_table[ sock ].id
        del self.session_table[ sock ]
        sock.close()
        msg = str( round(time.time() * 1000 ) ) + "|RemoveRemoteActor|id:" + removedId
        for s,sess in self.session_table.items() :
            sess.send( msg )

    def notify_others_of_arrival( self, session ) :
        msg = str( round(time.time() * 1000 ) ) + "|NewRemoteActor|" + session.actor.to_string()
        for s,sess in self.session_table.items() :
            if sess.id == session.id :
                continue
            sess.send( msg )


    # This method updates the sockets ready for reading and/or writing
    def select_sockets( self ):
        read_socks = [self.server]
        write_socks = []
        for k,v in self.session_table.items():
            read_socks.append( k )
            if len(v.outbound_message_queue) > 0:
                write_socks.append( k )
        
        read_ready, write_ready, error_ready = select.select( read_socks, write_socks, read_socks, 0 )
        self.read_ready = read_ready
        self.write_ready = write_ready

    def accept_read( self ):
        for s in self.read_ready:
            if s is self.server:
                # New connection
                conn, conn_addr = s.accept()
                conn.setblocking( 0 )
                #self.session_table[conn] = session.Session( conn, conn_addr )
                self.session_table[conn] = self.create_session( conn, conn_addr )

            else:
                # Socket with data to read?
                try:
                    data = s.recv( constants.READ_BUFFER_SIZE )
                    if data:
                        # Pass it to the session
                        self.session_table[s].handle_data( data )
                    else:
                        # Closed connection
                        del self.session_table[s]
                        s.close()
                except ConnectionResetError as cre:
                    self.handle_disconnect( s )

    def write_out( self ):
        for s in self.write_ready:
            self.session_table[s].send_messages()

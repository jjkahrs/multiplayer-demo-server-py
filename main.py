import socket
import map
import sessionmanager
import constants

server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

server.bind( ( constants.IP_ADDRESS, constants.PORT ) )
server.listen( constants.MAX_NUMBER_OF_CONNECTIONS )

session_mgr = sessionmanager.SessionManager( server )
map_server = map.Map( session_mgr )

print( "Listening on " + str(constants.PORT) )

while True:
    # select sockets with waiting data to read or clear buffers to write
    session_mgr.select_sockets()

    # accept connections and read inbound data
    session_mgr.accept_read()

    # update map state
    map_server.update_state()

    # send outbound messages
    session_mgr.write_out()


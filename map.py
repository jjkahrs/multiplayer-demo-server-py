import constants
import datetime
import vector
import time

class Map :
    def __init__( self, session_mgr ):
        self.tick = 0
        #self.tick_timer_start = datetime.datetime.now()
        self.tick_timer_start = round(time.time() * 1000)
        self.session_mgr = session_mgr
        self.last_timestamp = round(time.time() * 1000)

    def update_state( self ):
        # if the tick interval has passed, update the tick
        now = round(time.time() * 1000)
        
        if now - self.tick_timer_start >= constants.TICK_INTERVAL:
            self.tick_timer_start = round(time.time() * 1000)
            self.tick = self.tick + 1
            self.process_commands()
            self.physics_loop( now )
            self.last_timestamp = now

    def physics_loop( self, timestamp ):
        deltaTime = ( timestamp - self.last_timestamp ) / 1000.0
        header = str(timestamp) + "|WorldDelta|" + str(deltaTime) + "|"
        payload = "|"

        index = 0
        for s,sess in self.session_mgr.session_table.items():
            # Update all the session actors 
            heading_vector = vector.Vector( sess.actor.heading_x, sess.actor.heading_y, sess.actor.heading_z )
            position_vector = vector.Vector( sess.actor.pos_x, sess.actor.pos_y, sess.actor.pos_z )            
            velocity_vector = heading_vector.mul( ( sess.actor.speed * min( deltaTime, sess.actor.duration ) ) )
            translated_position = position_vector.add( velocity_vector )

            sess.actor.pos_x = translated_position.x
            sess.actor.pos_y = translated_position.y
            sess.actor.pos_z = translated_position.z

            sess_data = ""
            if index > 0:
                sess_data += "^"
            sess_data = sess_data + "sessionId:" + sess.id + "," + sess.actor.to_string()
            payload += sess_data

            index += 1

        # inform all sessions of new state
        for s,sess in self.session_mgr.session_table.items():
            sess.send( header + str(self.tick) + payload )



    def process_commands( self ):
        timestamp = round( time.time() * 1000 )
        for sock, sess in self.session_mgr.session_table.items():
            for cmd in sess.inbound_message_queue:
                #print("processing command: " + cmd.raw)
                if cmd.cmd == "ReqPlayerState":
                    player_state_str = str(timestamp) + "|PlayerState|" + cmd.session.actor.to_string()
                    cmd.session.send( player_state_str )

                elif cmd.cmd == "ReqWorldState":
                    world_state_str = str(timestamp) + "|WorldState|" + self.current_world_snapshot()
                    cmd.session.send( world_state_str )
                
                elif cmd.cmd == "PlayerInput":
                    key_val_pairs = cmd.payload.split(",")
                    for key_val_pair in key_val_pairs:
                        pair = key_val_pair.split(":")

                        if "headingX" == pair[0] :
                            cmd.session.actor.heading_x = float(pair[1])
                        elif "headingY" == pair[0] :
                            cmd.session.actor.heading_y = float(pair[1])
                        elif "headingZ" == pair[0] :
                            cmd.session.actor.heading_z = float(pair[1])
                        elif "duration" == pair[0] :
                            cmd.session.actor.duration = float(pair[1])
                        elif "facingX" == pair[0] :
                            cmd.session.actor.facing_x = float(pair[1])
                        elif "facingY" == pair[0] :
                            cmd.session.actor.facing_y = float(pair[1])
                        elif "facingZ" == pair[0] :
                            cmd.session.actor.facing_z = float(pair[1])
                        
                
            sess.inbound_message_queue.clear()

    def current_world_snapshot( self ):
        payload = ""
        count = 0
        for s,sess in self.session_mgr.session_table.items():
            if count > 0:
                payload += "^"
            payload = payload + sess.actor.to_string()
            count += 1
        return payload

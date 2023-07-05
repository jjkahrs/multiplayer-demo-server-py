
class Actor:
    def __init__(self):
        self.id = ""
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0
        self.heading_x = 0.0
        self.heading_y = 0.0
        self.heading_z = 0.0
        self.speed = 2.0
        self.duration = 0.0
        self.facing_x = 0.0
        self.facing_y = 0.0
        self.facing_z = 0.0

    def to_string( self ):
        return "sessionId:"+self.id + \
            ",posX:"+str(round(self.pos_x,3))+",posY:"+str(round(self.pos_y,3))+",posZ:"+str(round(self.pos_z,3))+ \
            ",headingX:"+str(round(self.heading_x,3))+",headingY:"+str(round(self.heading_y,3))+",headingZ:"+str(round(self.heading_z,3))+ \
            ",speed:"+str(round(self.speed,3)) + \
            ",facingX:"+str(round(self.facing_x,3))+",facingY:"+str(round(self.facing_y,3))+",facingZ:"+str(round(self.facing_z,3))
class Vector:
    def __init__(self, x, y, z) :
        self.x = x
        self.y = y
        self.z = z

    def add( self, vec ) :
        return Vector( self.x + vec.x, self.y + vec.y, self.z + vec.z )
    
    def mul( self, val ) :
        return Vector( self.x * val, self.y * val, self.z * val )
    
    def to_string( self ) :
        return str("("+str(self.x)+","+str(self.y)+","+str(self.z)+")")
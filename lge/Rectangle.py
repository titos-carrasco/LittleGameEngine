class Rectangle():
    def __init__( self, origin, size ):
        w, h = size
        assert w > 0 and h > 0, "'size' invalido"

        self.x, self.y = origin
        self.w, self.h = size

    def __repl__( self ):
        return "Rect( ( %f, %f ), ( %f, %f ) )" % ( self.x, self.y, self.w, self.h )

    def Copy( self ):
        return Rectangle( ( self.x, self.y ), ( self.w, self.h ) )

    def GetOrigin( self ):
        return self.x, self.y

    def GetSize( self ):
        return self.w, self.h

    def SetOrigin( self, origin ):
        self.x, self.y = origin

    def SetSize( self, size ):
        w, h = size
        assert w > 0 and h > 0, "'size' invalido"
        self.w, self.h = size

    def KeepInsideRectangle( self, rect ):
        x, y = self.x, self.y
        w, h = self.w, self.h
        rx, ry = rect.x, rect.y
        rw, rh = rect.w, rect.h

        if( w <= rw and h <= rh ):
            if( x < rx ): x = rx
            elif( x + w > rx + rw ): x = rx + rw - w
            if( y < ry ): y = ry
            elif( y + h > ry + rh ): y = ry + rh - h

        self.x, self.y =  x, y

    def CollidePoint( self, point ):
        x, y = self.origin
        w, h = self.w, self.h
        px, py = point
        return px >= x and px < x+w and py >= y and py < y+h

    def CollideRectangle( self, rect ):
        x1, y1 = self.x, self.y
        w1, h1 = self.w, self.h
        x2, y2 = rect.x, rect.y
        w2, h2 = rect.w, rect.h

        return not ( x2 >= x1 + w1 or x1 >= x2 + w2 or y2 >= y1 + h1 or y1 >= y2 + h2 )

    def GetCollideRectangle( self, rect ):
        x1, y1 = self.x, self.y
        w1, h1 = self.w, self.h
        x2, y2 = rect.x, rect.y
        w2, h2 = rect.w, rect.h

        if( x1 > x2 ):
            x = x1
            w = x2 + w2 - x1
        else:
            x = x2
            w = x1 + w1 - x2

        if( y1 > y2 ):
            y = y1
            h = y2 + h2 - y1
        else:
            y = y2
            h = y1 + h1 - y2
        return Rectangle( (x, y), (w, h) ) if w > 0 and h > 0 else None

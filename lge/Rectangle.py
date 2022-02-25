class Rectangle():
    def __init__( self, origin, size ):
        x, y = origin
        w, h = size
        assert w > 0 and h > 0, "'size' invalido"

        self.origin = x, y
        self.size = w, h

    def Copy( self ):
        return Rectangle( self.origin, self.size )

    def GetOrigin( self ):
        x, y = self.origin
        return x, y

    def GetSize( self ):
        w, h = self.size
        return w, h

    def SetOrigin( self, origin ):
        x, y = origin
        self.origin = x, y

    def SetSize( self, size ):
        w, h = size
        assert w > 0 and h > 0, "'size' invalido"
        self.size = w, h

    def CollidePoint( self, point ):
        x, y = self.origin
        w, h = self.size
        px, py = point
        return px >= x and px < x+w and py >= y and py < y+h

    def CollideRectangle( self, rect ):
        x1, y1 = self.origin
        w1, h1 = self.size
        x2, y2 = rect.origin
        w2, h2 = rect.size

        return not ( x2 >= x1 + w1 or x1 >= x2 + w2 or y2 >= y1 + h1 or y1 >= y2 + h2 )

    def GetCollideRectangle( self, rect ):
        x1, y1 = self.origin
        w1, h1 = self.size
        x2, y2 = rect.origin
        w2, h2 = rect.size

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

    def KeepInsideRectangle( self, rect ):
        x, y = self.origin
        w, h = self.size
        rx, ry = rect.origin
        rw, rh = rect.size

        if( w <= rw and h <= rh ):
            if( x < rx ): x = rx
            elif( x + w > rx + rw ): x = rx + rw - w
            if( y < ry ): y = ry
            elif( y + h > ry + rh ): y = ry + rh - h

        self.origin =  x, y
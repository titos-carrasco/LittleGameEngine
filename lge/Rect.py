class Rect():
    def __init__( self, origin, size ):
        x, y = origin
        self.origin = int(x), int(y)

        w, h = size
        if( w < 0 ): w = 0
        if( h < 0 ): h = 0
        self.size = int(w), int(h)

    def Copy( self ):
        return Rect( self.origin, self.size )

    def GetOrigin( self ):
        x, y = self.origin
        return x, y

    def GetSize( self ):
        w, h = self.size
        return w, h

    def SetOrigin( self, origin ):
        x, y = origin
        self.origin = int(x), int(y)

    def SetSize( self, size ):
        w, h = size
        if( w < 0 ): w = 0
        if( h < 0 ): h = 0
        self.size = int(w), int(h)

    def CollidePoint( self, point ):
        x, y = self.origin
        w, h = self.size
        px, py = int(point[0]), int(point[1])
        return px >= x and px < x+w and py >= y and py < y+h

    def CollideRect( self, rect ):
        x1, y1 = self.origin
        w1, h1 = self.size
        x2, y2 = rect.origin
        w2, h2 = rect.size

        if( x1 > x2 ):
            x = x1
            w = x2 + w2 - 1 - x1
        else:
            x = x2
            w = x1 + w1 - 1 - x2

        if( y1 > y2 ):
            y = y1
            h = y2 + h2 - 1 - y1
        else:
            y = y2
            h = y1 + h1 - 1 - y2
        return Rect( (x,y), (w,h) ) if w >= 0 and h >= 0 else None

    def KeepInsideRect( self, rect ):
        x, y = self.origin
        w, h = self.size
        rx, ry = rect.GetOrigin()
        rw, rh = rect.GetSize()

        if( w <= rw and h <= rh ):
            if( x < rx ): x = rx
            elif( x + w > rw ): x = rw - w
            if( y < ry ): y = ry
            elif( y + h > rh ): y = rh - h

        return x, y

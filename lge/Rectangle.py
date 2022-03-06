class Rectangle():
    def __init__( self, origin, size ):
        w, h = size
        assert w > 0 and h > 0, "'size' invalido"
        self._w, self._h = size
        self._x1, self._y1 = origin
        self._x2, self._y2 = self._x1 + w - 1, self._y1 + h - 1

    def __repr__( self ):
        return "Rectangle( ( %f, %f ), ( %f, %f ), ( %f, %f ) )" % ( self._x1, self._y1, self._x2, self._y2, self._w, self._h )

    def Copy( self ):
        return Rectangle( ( self._x1, self._y1 ), ( self._w, self._h ) )

    def GetPoints( self ):
        return self._x1, self._y1, self._x2, self._y2

    def GetSize( self ):
        return self._w, self._h

    def SetOrigin( self, x, y ):
        self._x1, self._y1 = x, y
        self._x2, self._y2 = self._x1 + self._w - 1, self._y1 + self._h - 1

    def SetSize( self, w, h ):
        assert w > 0 and h > 0, "'size' invalido"
        self._w, self._h = w, h
        self._x2, self._y2 = self._x1 + self._w - 1, self._y1 + self._h - 1

    def KeepInsideRectangle( self, rect ):
        if( self._w <= rect._w and self._h <= rect._h ):
            if( self._x1 < rect._x1 ): self._x1 = rect._x1
            elif( self._x2 > rect._x2): self._x1 = rect._x2 - self._w + 1

            if( self._y1 < rect._y1 ): self._y1 = rect._y1
            elif( self._y2 > rect._y2 ): self._y1 = rect._y2 - self._h + 1

            self._x2, self._y2 = self._x1 + self._w - 1, self._y1 + self._h - 1

    def CollidePoint( self, px, py ):
        return px >= self._x1 and \
               px <= self._x2 and \
               py >= self._y1 and \
               py <= self._y2

    def CollideRectangle( self, rect ):
        return rect._x1 <= self._x2 and \
               self._x1 <= rect._x2 and \
               rect._y1 <= self._y2 and \
               self._y1 <= rect._y2

    def GetCollideRectangle( self, rect ):
        x1, y1 = self._x1, self._y1
        w1, h1 = self._w, self._h
        x2, y2 = rect._x1, rect._y1
        w2, h2 = rect._w, rect._h

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

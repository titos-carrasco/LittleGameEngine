from lge.Rectangle import Rectangle


class Camera():
    def __init__( self, position, size ):
        self._rect = Rectangle( position, size )
        self._bounds = None

    def GetRectangle( self ):
        return self._rect.Copy()

    def GetPosition( self ):
        x1, y1, x2, y2 = self._rect.GetPoints()
        return x1, y1

    def GetSize( self ):
        return self._rect.GetSize()

    def GetBounds( self ):
        if( self._bounds  ): return self._bounds.Copy()
        else: return None

    def SetPosition( self, x, y ):
        self._rect.SetOrigin( x, y )
        if( self._bounds ):
            self._rect.KeepInsideRectangle( self._bounds )

    def SetBounds( self, bounds=None) :
        if( bounds ): self._bounds = bounds.Copy()
        else: self._bounds = None

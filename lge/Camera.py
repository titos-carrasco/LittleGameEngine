from lge.Rect import Rect


class Camera():
    def __init__( self, position, size ):
        self.rect = Rect( position, size )
        self.bounds = None

    def GetPosition( self ):
        return self.rect.GetOrigin()

    def GetSize( self ):
        return self.rect.GetSize()

    def SetBounds( self, bounds=None ):
        self.bounds = bounds.Copy()

    def GetBounds( self ):
        if( self.bounds is None ): return None
        else: return self.bounds.Copy()

    def SetPosition( self, position ):
        # no tiene limites
        if( self.bounds is None ):
            self.rect.SetOrigin( position )
            return

        # el posible origen
        cx, cy = position
        cx, cy = int(cx), int(cy)
        cw, ch = self.rect.GetSize()

        # debemos mantenerla dentro de los limites
        me = Rect( (cx,cy), (cw,ch) )
        cx, cy = me.KeepInsideRect( self.bounds )

        # la reposicionamos
        self.rect.SetOrigin( (cx,cy) )

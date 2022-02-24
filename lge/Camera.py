from lge.Rect import Rect


class Camera():
    def __init__( self, position, size ):
        self.rect = Rect( position, size )
        self.bounds = None

    def GetRect( self ):
        return self.rect.Copy()

    def GetPosition( self ):
        return self.rect.GetOrigin()

    def GetSize( self ):
        return self.rect.GetSize()

    def GetBounds( self ):
        if( self.bounds  ): return self.bounds.Copy()
        else: return None

    def SetPosition( self, position ):
        self.rect.SetOrigin( position )
        if( self.bounds ):
            self.rect.KeepInsideRect( self.bounds )

    def SetBounds( self, bounds=None) :
        if( bounds ): self.bounds = bounds.Copy()
        else: self.bounds = bounds

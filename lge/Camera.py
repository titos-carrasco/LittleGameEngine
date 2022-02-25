from lge.Rectangle import Rectangle


class Camera():
    def __init__( self, position, size ):
        self.rect = Rectangle( position, size )
        self.bounds = None

    def GetRectangle( self ):
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
            self.rect.KeepInsideRectangle( self.bounds )

    def SetBounds( self, bounds=None) :
        if( bounds ): self.bounds = bounds.Copy()
        else: self.bounds = bounds

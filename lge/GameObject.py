import uuid
from lge.Rectangle import Rectangle

class GameObject():
    def __init__( self, position, size, name=None ):
        self.rect = Rectangle( position, size )
        self.name = "__noname__-" + uuid.uuid4().hex if name is None else name
        self.tag = ""
        self.visible = True
        self.active = True
        self.colliders = []

    def GetRectangle( self ):
        return self.rect.Copy()

    def GetPosition( self ):
        return self.rect.GetOrigin()

    def GetSize( self ):
        return self.rect.GetSize()

    def GetName( self ):
        return self.name

    def GetTag( self ):
        return self.tag

    def IsVisible( self ):
        return self.visible

    def IsActive( self ):
        return self.active

    def SetPosition( self, position, bounds=None ):
        self.rect.SetOrigin( position )
        if( bounds ):
            self.rect.KeepInsideRectangle( bounds )

    def SetSize( self, size ):
        self.rect.SetSize( size )

    def SetTag( self, tag ):
        self.tag = tag

    def SetVisible( self, visible ):
        self.visible = visible

    def SetActive( self, active ):
        self.active = active

    def SetColliders( self, colliders=True ):
        if( colliders is True ):
            r = self.rect.Copy()
            r.SetOrigin( (0,0) )
            self.colliders = [ r ]
        elif( isinstance( colliders, list ) ):
            self.colliders = colliders
        else:
            self.colliders = []

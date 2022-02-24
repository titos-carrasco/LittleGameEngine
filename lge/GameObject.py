import uuid
from lge.Rect import Rect

class GameObject():
    def __init__( self, position, size, name=None ):
        self.rect = Rect( position, size )
        self.name = "__noname__-" + uuid.uuid4().hex if name is None else name
        self.tag = ""
        self.visible = True
        self.active = True
        self.use_collider = False

    def GetRect( self ):
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
            self.rect.KeepInsideRect( bounds )

    def SetSize( self, size ):
        self.rect.SetSize( size )

    def SetTag( self, tag ):
        self.tag = tag

    def SetVisible( self, visible ):
        self.visible = visible

    def SetActive( self, active ):
        self.active = active

    def SetColliders( self, enable ):
        self.use_collider = enable

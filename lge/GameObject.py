import uuid

from lge.Rect import Rect

class GameObject():
    def __init__( self, origin, size, name=None ):
        self.rect = Rect( origin, size )
        self.name = "noname-" + uuid.uuid4().hex if name is None else name
        self.tag = ""
        self.visible = True

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

    def SetPosition( self, origin ):
        self.rect.SetOrigin( origin )

    def SetSize( self, size ):
        self.rect.SetSize( size )

    def SetVisible( self, visible ):
        self.visible = visible

    def CollideGObject( self, gobj ):
        return self.rect.CollideRect( gobj.rect )

    def CollideRect( self, rect ):
        return self.rect.CollideRect( rect )

    def CollidePoint( self, point ):
        return self.rect.CollidePoint( point )

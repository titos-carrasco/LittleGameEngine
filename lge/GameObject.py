import uuid
from lge.Rect import Rect

class GameObject():
    def __init__( self, xy, size, layer, name=None ):
        self.rect = Rect( xy, size )
        self.visible = True
        self.deleteMe = False
        self.layer = layer
        self.name = "noname-" + uuid.uuid4().hex if name is None else name
        if( layer < 0 ):
            raise( "'layer' no puede ser negativo" )

    def GetPosition( self ):
        return self.rect.GetOrigin()

    def GetSize( self ):
        return self.rect.GetSize()

    def IsVisible( self ):
        return self.visible

    def GetLayer( self ):
        return self.layer

    def GetName( self ):
        return self.name

    def SetPosition( self, xy ):
        self.rect.SetOrigin( xy )

    def SetSize( self, size ):
        self.rect.SetSize( size )

    def SetVisible( self, visible ):
        self.visible = visible

    def DeleteMe( self ):
        self.deleteMe = True

    def CollideRect( self, rect ):
        return self.rect.CollideRect( rect )

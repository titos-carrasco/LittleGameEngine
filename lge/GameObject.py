import uuid
from lge.Rectangle import Rectangle

class GameObject():
    def __init__( self, position, size, name=None ):
        self._rect = Rectangle( position, size )
        self._name = "__noname__-" + uuid.uuid4().hex if name is None else name
        self._tag = ""
        self._use_colliders = False

    def GetRectangle( self ):
        return self._rect.Copy()

    def GetPosition( self ):
        x1, y1, x2, y2 = self._rect.GetPoints()
        return x1, y1

    def GetSize( self ):
        return self._rect.GetSize()

    def GetName( self ):
        return self._name

    def GetTag( self ):
        return self._tag

    def SetPosition( self, x, y, bounds=None ):
        self._rect.SetOrigin( x, y )
        if( bounds ):
            self._rect.KeepInsideRectangle( bounds )

    def SetSize( self, w, h ):
        self._rect.SetSize( w, h )

    def SetTag( self, tag ):
        self._tag = tag

    def SetColliders( self, enabled=True ):
        self._use_colliders = enabled

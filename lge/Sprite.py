from lge.GameObject import GameObject
from lge.Engine import Engine


class Sprite( GameObject ):
    def __init__( self, inames, position, name=None ):
        super().__init__( position, ( 1, 1 ), name )

        self._elapsed= 0
        self._surfaces = {}

        if( not isinstance( inames, list ) ): inames = [ inames ]
        for iname in inames:
            self._surfaces[iname] = Engine.GetImages( iname )

        iname = list( self._surfaces.keys() )[0]
        self._shape = [ iname, 0 ]
        self._surface = self._surfaces[iname][0]
        size = self._surface.get_rect().size
        self._rect.SetSize( size[0], size[1] )

    def SetSize( self, w, h ):
        pass

    def GetCurrentShape( self ):
        iname, idx = self._shape
        return iname, idx

    def NextShape( self, dt, segs=0 ):
        self._elapsed= self._elapsed+ dt
        if( self._elapsed< segs ): return
        self._elapsed= 0
        iname, idx = self._shape
        idx = idx + 1
        if( idx >= len( self._surfaces[iname] ) ): idx = 0
        self._shape = iname, idx
        self._surface = self._surfaces[iname][idx]
        size = self._surface.get_rect().size
        self._rect.SetSize( size[0], size[1] )

    def SetShape( self, iname, idx ):
        self._elapsed= 0
        self._shape = iname, idx
        self._surface = self._surfaces[iname][idx]
        size = self._surface.get_rect().size
        self._rect.SetSize( size[0], size[1] )

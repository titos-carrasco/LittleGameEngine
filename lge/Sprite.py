from glob import glob
from pygame import image as pyImage
from pygame import transform as pyTransform

from lge.GameObject import GameObject


class Sprite( GameObject ):
    def __init__( self, fspecs, position, name=None ):
        super().__init__( position, (0,0), name )

        self.surfaces = {}
        if( isinstance( fspecs, str ) ):
            self.surfaces["__no_id__"] = self._LoadShapes( glob( fspecs ) )
        elif( isinstance( fspecs, list ) ):
            self.surfaces["__no_id__"] = self._LoadShapes( fspecs )
        elif( isinstance( fspecs, dict ) ):
            for entry in fspecs:
                fspec = fspecs[entry]
                if( isinstance( fspec, str ) ):
                    fspec = glob( fspec )
                self.surfaces[entry] = self._LoadShapes( fspec )

        entry = list( self.surfaces.keys() )[0]
        self.shape = [ 0, entry ]
        self.surface = self.surfaces[entry][0]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def _LoadShapes( self, fnames ):
        surfaces = []
        fnames.sort()
        for fname in fnames:
            surfaces.append( pyImage.load( fname ).convert_alpha() )
        return surfaces

    def GetCurrentShape( self ):
        return self.shape[0], self.shape[1]

    def NextShape( self ):
        idx, entry = self.shape
        idx = idx + 1
        if( idx >= len( self.surfaces[entry] ) ):
            idx = 0
        self.shape[0] = idx
        self.surface = self.surfaces[entry][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def SetShape( self, idx, entry="__no_id__" ):
        self.shape = [ idx, entry ]
        self.surface = self.surfaces[entry][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def SetSize( self, size ):
        self.Scale( size )

    def Scale( self, size ):
        w, h = size
        if( w < 0 or h < 0 ):
            raise( "'width' o 'height' no pueden ser negativos")
        size = int( w ), int( h )
        for entry in self.surfaces:
            surfaces = self.surfaces[entry]
            n = len( surfaces )
            for i in range( n ):
                s = surfaces[i]
                surfaces[i] = pyTransform.smoothscale( s, size )
        idx, entry = self.shape
        self.surface = self.surfaces[entry][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def ScalePercent( self, percent ):
        if( percent < 0 ):
            raise( "'percent' no puede ser negativo" )
        for entry in self.surfaces:
            surfaces = self.surfaces[entry]
            n = len( surfaces )
            for i in range( n ):
                s = surfaces[i]
                surfaces[i] = pyTransform.smoothscale( s, ( int(s.get_width()*percent), int(s.get_height()*percent)) )
        idx, entry = self.shape
        self.surface = self.surfaces[entry][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def Flip( self, flipX, flipY ):
        for entry in self.surfaces:
            surfaces = self.surfaces[entry]
            n = len( surfaces )
            for i in range( n ):
                s = surfaces[i]
                surfaces[i] = pyTransform.flip( s, flipX, flipY )
        idx, entry = self.shape
        self.surface = self.surfaces[entry][idx]

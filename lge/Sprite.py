import pygame

from lge.GameObject import GameObject
from lge.Engine import Engine


class Sprite( GameObject ):
    def __init__( self, inames, position, name=None ):
        super().__init__( position, (0,0), name )
        self.elapsed = 0

        if( not isinstance( inames, list ) ): inames = [ inames ]
        self.surfaces = {}
        for iname in inames:
            self.surfaces[iname] = Engine.GetImages( iname )

        entry = list( self.surfaces.keys() )[0]
        self.shape = [ 0, entry ]
        self.surface = self.surfaces[entry][0]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def GetCurrentShape( self ):
        return self.shape[0], self.shape[1]

    def NextShape( self, dt, millis=0 ):
        self.elapsed = self.elapsed + dt
        if( self.elapsed < millis ): return
        self.elapsed = 0
        idx, entry = self.shape
        idx = idx + 1
        if( idx >= len( self.surfaces[entry] ) ):
            idx = 0
        self.shape[0] = idx
        self.surface = self.surfaces[entry][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def SetShape( self, idx, entry ):
        self.shape = [ idx, entry ]
        self.surface = self.surfaces[entry][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )
        self.elapsed = 0

    def SetSize( self, size ):
        self.Scale( size )

    def Scale( self, size ):
        for entry in self.surfaces:
            surfaces = self.surfaces[entry]
            n = len( surfaces )
            for i in range( n ):
                s = surfaces[i]
                w, h = s.get_size()
                if( isinstance( size, tuple ) ): scale = size
                else: scale = ( int(w*size),int(h*size) )
                surfaces[i] = pygame.transform.smoothscale( s, scale )

        idx, entry = self.shape
        self.surface = self.surfaces[entry][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def Flip( self, fx, fy ):
        for entry in self.surfaces:
            surfaces = self.surfaces[entry]
            n = len( surfaces )
            for i in range( n ):
                s = surfaces[i]
                surfaces[i] = pygame.transform.flip( s, fx, fy )

        idx, entry = self.shape
        self.surface = self.surfaces[entry][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

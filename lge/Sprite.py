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

        iname = list( self.surfaces.keys() )[0]
        self.shape = [ iname, 0 ]
        self.surface = self.surfaces[iname][0]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def GetCurrentShape( self ):
        iname, idx = self.shape
        return iname, idx

    def NextShape( self, dt, millis=0 ):
        self.elapsed = self.elapsed + dt
        if( self.elapsed < millis ): return
        self.elapsed = 0
        iname, idx = self.shape
        idx = idx + 1
        if( idx >= len( self.surfaces[iname] ) ):
            idx = 0
        self.shape = iname, idx
        self.surface = self.surfaces[iname][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def SetShape( self, iname, idx ):
        self.elapsed = 0
        self.shape = iname, idx
        self.surface = self.surfaces[iname][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def SetSize( self, size ):
        pass

    def ReSize( self, size ):
        for iname in self.surfaces:
            surfaces = self.surfaces[iname]
            n = len( surfaces )
            for i in range( n ):
                s = surfaces[i]
                surfaces[i] = pygame.transform.smoothscale( s, size )

        iname, idx = self.shape
        self.surface = self.surfaces[iname][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def Scale( self, factor ):
        for iname in self.surfaces:
            surfaces = self.surfaces[iname]
            n = len( surfaces )
            for i in range( n ):
                s = surfaces[i]
                w, h = s.get_size()
                size = ( int(w*factor),int(h*factor) )
                surfaces[i] = pygame.transform.smoothscale( s, size )

        iname, idx = self.shape
        self.surface = self.surfaces[iname][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

    def Flip( self, fx, fy ):
        for iname in self.surfaces:
            surfaces = self.surfaces[iname]
            n = len( surfaces )
            for i in range( n ):
                s = surfaces[i]
                surfaces[i] = pygame.transform.flip( s, fx, fy )

        iname, idx = self.shape
        self.surface = self.surfaces[iname][idx]
        size = self.surface.get_rect().size
        self.rect.SetSize( size )

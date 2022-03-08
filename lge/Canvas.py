import pygame
from lge.Engine import Engine
from lge.GameObject import GameObject

class Canvas( GameObject ):
    def __init__( self, position, size, name=None ):
        super().__init__( position, size, name )
        self._surface = pygame.Surface( size, pygame.SRCALPHA )

    def SetSize( self, w, h ):
        pass

    def Fill( self, bgColor ):
        self._surface.fill( bgColor )

    def DrawText( self, text, position, fontName, color ):
        x, y = position
        s  = Engine.fonts[fontName].render( text, True, color )
        self._surface.blit( s, ( x, self._rect.GetSize()[1] - s.get_height() - y ) )

    def DrawPoint( self, position, color ):
        x, y = position
        y = self._rect.GetSize()[1] - y
        pygame.draw.circle( self._surface, color, ( x, y ), 0, 0 )

    def DrawCircle( self, position, radius, color, thickness=False ):
        x, y = position
        if( radius <= 0 ): radius = 1
        thickness = 1 if thickness else 0

        y = self._rect.GetSize()[1] - y
        pygame.draw.circle( self._surface, color, ( x, y ), radius, thickness )

    def DrawRectangle( self, position, size, color, thickness=False ):
        x, y = position
        w, h = size
        if( w <= 0 ): w = 1
        if( h <= 0 ): h = 1
        thickness = 1 if thickness else 0

        y = self._rect.GetSize()[1] - h - y
        pygame.draw.rect( self._surface, color, pygame.Rect( (x,y), (w,h) ), thickness )

    def DrawSurface( self, position, surface ):
        x, y = position
        w, h = self.GetSize()
        self._surface.blit( surface, (x, h - surface.get_height() - y) )

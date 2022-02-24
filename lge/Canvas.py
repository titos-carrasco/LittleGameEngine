import pygame
from lge.Engine import Engine
from lge.GameObject import GameObject

class Canvas( GameObject ):
    def __init__( self, position, size, name=None ):
        super().__init__( position, size, name )
        self.surface = pygame.Surface( size, pygame.SRCALPHA )

    def SetSize( self, size ):
        pass

    def Fill( self, bgColor ):
        self.surface.fill( bgColor )

    def DrawText( self, text, position, fontName, color ):
        s  = Engine.fonts[fontName].render( text, True, color )
        x, y = position
        self.surface.blit( s, ( x,self.rect.GetSize()[1]-s.get_height()-y) )

    def DrawPoint( self, point, color ):
        x, y = point
        y = self.rect.GetSize()[1] - y
        pygame.draw.circle( self.surface, color, (x,y), 0, 0 )

    def DrawCircle( self, center, radius, color, thickness=False ):
        if( radius <= 0 ): radius = 1
        thickness = 1 if thickness else 0

        x, y = center
        y = self.rect.GetSize()[1] - y
        pygame.draw.circle( self.surface, color, (x,y), radius, thickness )

    def DrawRectangle( self, position, size, color, thickness=False ):
        x, y = position
        w, h = size
        if( w <= 0 ): w = 1
        if( h <= 0 ): h = 1
        thickness = 1 if thickness else 0

        y = self.rect.GetSize()[1] - h - y
        pygame.draw.rect( self.surface, color, pygame.Rect( (x,y), (w,h) ), thickness )

    #def DrawLines( self, lines, fgColor, bgColor=None ):
    #    pass

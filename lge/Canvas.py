import pygame

from lge.Engine import Engine
from lge.GameObject import GameObject

class Canvas( GameObject ):
    def __init__( self, position, size, color, name=None ):
        super().__init__( position, size, name )
        self.surface = pygame.Surface( self.GetSize(),pygame.SRCALPHA )
        self.surface.fill( color)

    def SetSize( self, size ):
        pass

    def DrawPoint( self, point, color ):
        point = Engine._Fix_Coordinates( point, self.GetSize()[1] )
        pygame.draw.circle( self.surface, color, point, 0 )

    def DrawCircle( self, center, radius, thickness, fgColor, bgColor=None ):
        center = Engine._Fix_Coordinates( center, self.GetSize()[1] )
        if( radius <= 0 ): radius = 1
        if( thickness <= 0 ): thickness = 1

        if( bgColor ): pygame.draw.circle( self.surface, bgColor, center, radius, 0 )
        pygame.draw.circle( self.surface, fgColor, center, radius, thickness )

    def Fill( self, bgColor, rect=None ):
        if( rect ):
            x, y = Engine._Fix_Coordinates( rect.GetOrigin(), self.GetSize()[1] )
            rect = pygame.Rect( (x,y-rect.GetSize()[1]), rect.GetSize() )
        self.surface.fill( bgColor, rect )

    def DrawRectangle( self, rect, thickness, fgColor, bgColor=None  ):
        x, y = Engine._Fix_Coordinates( rect.GetOrigin(), self.GetSize()[1] )
        rect = pygame.Rect( (x,y-rect.GetSize()[1]), rect.GetSize() )
        if( thickness <= 0 ): thickness = 1

        if( bgColor ): self.surface.fill( bgColor, rect )
        pygame.draw.rect( self.surface, fgColor, rect, thickness )

    def DrawLines( self, lines, fgColor, bgColor=None ):
        pass

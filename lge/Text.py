import pygame

from lge.GameObject import GameObject
from lge.Engine import Engine


class Text( GameObject ):
    def __init__( self, text, position, fontName, fgColor, bgColor=None, name=None ):
        super().__init__( position, (0,0), name )

        self.font = Engine.fonts[fontName]
        self.fgColor = fgColor
        self.bgColor = bgColor
        if( not text is None ):
            self.SetText( text )

    def SetText( self, text ):
        self.text = text
        self.surface =self.font.render( self.text, True, self.fgColor, self.bgColor )
        size = self.surface.get_size()
        super().SetSize( size )

    def SetSize( self, size ):
        pass

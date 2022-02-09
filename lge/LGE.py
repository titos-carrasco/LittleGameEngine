import time
import sys
import pygame

from lge.Rect import Rect
from lge.Sprite import Sprite


class LGE():
    CONSTANTS = pygame.constants

    def __init__( self, worldDim, winDim, title, bgColor, task=None ):
        self.world = Rect( (0,0), worldDim )
        self.viewport = Rect( (0,0), winDim )
        self.title = title
        self.bgColor = bgColor
        self.task = task
        self.fps = 60
        self.events = []
        self.collidersColor = None
        self.textos = []
        self.gobjects = {}
        self.layers = {}
        self.camTarget = None

        pygame.init()
        pygame.display.set_caption( self.title )
        self.screen = pygame.display.set_mode( self.viewport.GetSize() )

    # world
    def GetWorldSize( self ):
        return self.world.GetSize()

    def KeepInsideWorld( self, gobj, newpos ):
        x, y = newpos
        w, h = gobj.GetSize()
        ww, wh = self.world.GetSize()
        if( x < 0 ): x = 0
        elif( x + w > ww ): x = ww - w
        if( y < 0 ): y = 0
        elif( y + h > wh ): y = wh - h
        return x, y

    # camera
    def SetCamPosition( self, position ):
        x, y = self.KeepInsideWorld( self.viewport, position )
        self.viewport.SetOrigin( (x,y) )

    def GetCamPosition( self ):
        return self.viewport.GetOrigin()

    def GetCamSize( self ):
        return self.viewport.GetSize()

    def SetCamTarget( self, target=None ):
        self.camTarget = target

    def AddText( self, text, position, color=(0,0,0) ):
        self.textos.append( [ text, position, color ] )

    def _CamFollowTarget( self ):
        if( self.camTarget is None ): return
        x, y = self.camTarget.GetPosition()
        w, h = self.camTarget.GetSize()
        cw, ch = self.GetCamSize()

        x = x + w/2 - cw/2
        y = y + h/2 - ch/2
        self.SetCamPosition( (x, y) )

    # game
    def SetFPS( self, fps ):
        self.fps = int( fps )

    def AddGObject( self, gobj ):
        name = gobj.name
        if( name in self.gobjects ):
            raise( "'GObject' ya existe" )
        self.gobjects[name] = gobj

        layer = gobj.layer
        if( not layer in self.layers ):
            self.layers[layer] = []
        self.layers[layer].append( gobj )

    def GetGObject( self, name ):
        if( name in self.gobjects ):
            return self.gobjects[name]
        else:
            return None

    def IsKeyDown( self, key ):
        for event in self.events:
            if( event.type == pygame.KEYDOWN ):
                if( event.key == key ):
                    return True
        return False

    def IsKeyUp( self, key ):
        for event in self.events:
            if( event.type == pygame.KEYUP ):
                if( event.key == key ):
                    return True
        return False

    def ShowColliders( self, bc=None ):
        self.collidersColor = bc

    def GetCollisions( self, gobj ):
        gobjs = []
        for go in self.layers[gobj.layer]:
            if( gobj != go and go.IsVisible() ):
                 crop = gobj.CollideRect( go.rect )
                 if( crop is not None ):
                     gobjs.append( (go,crop) )
        return gobjs

    def Quit( self ):
        pygame.quit()
        sys.exit()

    # main loop
    def Run( self ):
        pygame.key.set_repeat( 10 )
        pygame.font.init()
        font = pygame.font.Font( pygame.font.match_font( "consolas" ), 24 )
        clock = pygame.time.Clock()
        while( True ):
            # tiempo en ms desde el ciclo anterior
            dt = clock.tick( self.fps )

            # los eventos
            self.events = pygame.event.get()
            if( pygame.QUIT in [e.type for e in self.events] ):
                self.Quit()

            # la logica de cada GameObject
            for layer in sorted( self.layers.keys() ):
                for gobj in self.layers[layer]:
                    if( hasattr( gobj, "OnUpdate" ) ):
                        gobj.OnUpdate( dt )

            # la logica del world
            if( self.task ):
                self.task( dt )

            # necesario si es que tiene seguimiento automatico
            self._CamFollowTarget()

            # el rendering
            self.screen.fill( self.bgColor )
            for layer in sorted( self.layers.keys() ):
                for gobj in self.layers[layer]:
                    if( hasattr( gobj, "surface" ) ):
                        if( gobj.IsVisible() and gobj.CollideRect( self.viewport ) ):
                            w, h = gobj.GetSize()
                            x, y = self._Fix_XY( gobj.GetPosition(), (w,h) )
                            self.screen.blit( gobj.surface, (x,y) )
                            if( self.collidersColor ):
                                pos = gobj.GetPosition()
                                size = gobj.GetSize()
                                pos = self._Fix_XY( pos, size )
                                points = [ (x,y), (x,y+h-1), (x+w-1,y+h-1), (x+w-1,y) ]
                                pygame.draw.lines( self.screen, self.collidersColor, True, points, 1 )

            # agregamos textos
            info =  "FPS: " + str( int( clock.get_fps() ) )
            self.AddText( info, (0,0) )
            for entry in self.textos:
                text, pos, color = entry
                text_surface = font.render( text, True, color )
                self.screen.blit( text_surface, (pos) )
            self.textos = []

            # mostramos la pantalla
            pygame.display.flip()

            # eliminamos la basura
            names = [ k for k in self.gobjects if self.gobjects[k].deleteMe ]
            for name in names:
                layer = self.gobjects[name].layer
                gobjs = self.layers[layer]
                for idx in range( len( gobjs ) ):
                    if( gobjs[idx].name == name ):
                        break
                del self.gobjects[name]
                del self.layers[layer][idx]


    def _Fix_XY( self, pos, size ):
        xo, yo = pos
        wo, ho = size
        ww, wh = self.world.GetSize()
        vx, vy  = self.viewport.GetOrigin()
        vw, vh = self.viewport.GetSize()
        dy = wh - (vy + vh)
        x = xo - vx
        y = wh - (yo + ho) - dy
        return x, y

import time
import sys
import pygame

from lge.Rect import Rect
from lge.Sprite import Sprite


class LGE():
    CONSTANTS = pygame.constants

    def __init__( self, worldDim, winDim, title, bgColor ):
        self.world = Rect( (0,0), worldDim )
        self.viewport = Rect( (0,0), winDim )
        self.title = title
        self.bgColor = bgColor
        self.collidersColor = None
        self.fps = 0

        self.gObjects = {}
        self.gObjectsToAdd = []
        self.gObjectsToDelete = []
        self.layers = {}

        self.mainTask = None
        self.camTarget = None

        self.events = []
        self.keysPressed = []
        self.textos = []
        self.fonts = {}

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption( self.title )
        self.screen = pygame.display.set_mode( self.viewport.GetSize() )
        self.clock = pygame.time.Clock()

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
        x, y = position
        w, h = self.viewport.GetSize()
        x, y = self.KeepInsideWorld( self.viewport, (int(x-w/2),int(y-h/2)) )
        self.viewport.SetOrigin( (x,y) )

    def GetCamPosition( self ):
        x, y = self.viewport.GetOrigin()
        w, h = self.viewport.GetSize()
        return int(x + w/2), int(y + h/2)

    def GetCamSize( self ):
        return self.viewport.GetSize()

    def SetCamTarget( self, target, center=True ):
        self.camTarget = (target,center)

    def UnSetCamTarget( self ):
        self.camTarget = None

    def LoadMyFont( self, fontName, size, path ):
        k = "%s---%s" % ( fontName, size )
        if( k in self.fonts ): return
        font = pygame.font.Font( path, size )
        self.fonts[k] = font

    def LoadSysFont( self, fontName, size ):
        k = "%s---%s" % ( fontName, size )
        if( k in self.fonts ): return
        font = pygame.font.SysFont( fontName, size )
        self.fonts[k] = font

    def GetSysFonts( self ):
        return pygame.font.get_fonts()

    def AddText( self, text, position, fontName, size, color=(0,0,0), bgColor=None ):
        k = "%s---%s" % ( fontName, size )
        font = self.fonts[k]
        self.textos.append( [ text, position, font, color, bgColor ] )

    def _CamFollowTarget( self ):
        if( self.camTarget is None ): return
        gobj, center = self.camTarget

        x, y = gobj.GetPosition()
        w, h = gobj.GetSize()
        cw, ch = self.GetCamSize()
        if( center ):
            x = x + w/2
            y = y + h/2
        self.SetCamPosition( (x, y) )

    # game
    def SetMainTask( self, task=None ):
        self.mainTask = task

    def SetFPS( self, fps ):
        self.fps = int( fps )

    def GetFPS( self ):
        return self.clock.get_fps()

    def Quit( self ):
        pygame.quit()
        sys.exit()

    # gobjects
    def AddGObject( self, gobj, layer ):
        name = gobj.name
        if( name in self.gObjects ):
            raise ValueError( "'Ya existe un 'gobject' con ese nombre" )
        for t in self.gObjectsToAdd:
            o, _ = t
            if( o.name == name ):
                raise ValueError( "Ya existe un 'gobject' con ese nombre ")
        self.gObjectsToAdd.append( (gobj,layer) )

    def DelGObject( self, gobj ):
        self.DelGObjectByname( gobj.name )

    def DelGObjectByName( self, name ):
        if( not name in self.gObjects ):
            raise ValueError( "'gobject' no existe" )
        if( name in self.gObjectsToDelete ):
            raise ValueError( "'gobject' ya esta marcado para eliminacion" )
        self.gObjectsToDelete.append( name )

    def GetGObject( self, name ):
        if( not name in self.gObjects ):
            raise ValueError( "'gobject' no existe" )
        gobj, layer = self.gObjects[name]
        return gobj

    def ShowColliders( self, bc=None ):
        self.collidersColor = bc

    def GetCollisions( self, name ):
        if( not name in self.gObjects ):
            raise ValueError( "'gobject' no existe" )

        gobj, layer = self.gObjects[name]
        gobjs = []
        for o in self.layers[layer]:
            if( gobj != o and o.IsVisible() ):
                 crop = gobj.CollideRect( o.rect )
                 if( crop is not None ):
                     gobjs.append( (o,crop) )
        return gobjs

    # events
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

    def IsKeyPressed( self, key ):
        return True if self.keysPressed[ key ] else False

    # main loop
    def Run( self ):
        pygame.key.set_repeat( 0 )

        while( True ):
            # tiempo en ms desde el ciclo anterior
            dt = self.clock.tick( self.fps )

            # los gobjects nuevos
            for t in self.gObjectsToAdd:
                gobj, layer = t
                self.gObjects[gobj.name] = t

                if( not layer in self.layers ):
                    self.layers[layer] = []
                self.layers[layer].append( gobj )
            self.gObjectsToAdd = []

            # los gobjects a eliminar
            for name in self.gObjectsToDelete:
                gobj, layer = self.gObjects[name]
                del self.gObjects[name]

                gobjs = self.layers[layer]
                for idx in range( len( gobjs ) ):
                    if( gobjs[idx].name == name ):
                        break
                del self.layers[layer][idx]

                if( not self.camTarget is None and self.camTarget[0] == gobj ):
                    self.camTarget = None
            self.gObjectsToDelete = []

            # los eventos
            self.events = pygame.event.get()
            if( pygame.QUIT in [e.type for e in self.events] ):
                self.Quit()
            self.keysPressed = pygame.key.get_pressed()

            # la logica de cada GameObject
            for layer in sorted( self.layers.keys() ):
                for gobj in self.layers[layer]:
                    if( hasattr( gobj, "OnUpdate" ) ):
                        gobj.OnUpdate( dt )

            # la logica del world
            if( self.mainTask ):
                self.mainTask( dt )

            # necesario si es que tiene seguimiento automatico
            self._CamFollowTarget()

            # el rendering
            self.screen.fill( self.bgColor )
            for layer in sorted( self.layers.keys() ):
                for gobj in self.layers[layer]:
                    if( gobj.IsVisible() and gobj.CollideRect( self.viewport ) ):
                        w, h = gobj.GetSize()
                        x, y = self._Fix_XY( gobj.GetPosition(), (w,h) )
                        if( hasattr( gobj, "surface" ) ):
                            self.screen.blit( gobj.surface, (x,y) )
                        if( self.collidersColor ):
                            pos = gobj.GetPosition()
                            size = gobj.GetSize()
                            pos = self._Fix_XY( pos, size )
                            points = [ (x,y), (x,y+h-1), (x+w-1,y+h-1), (x+w-1,y) ]
                            pygame.draw.lines( self.screen, self.collidersColor, True, points, 1 )

            # mostramos los textos solicitados
            vw, vh = self.viewport.size
            for entry in self.textos:
                text, pos, font, color, bgColor = entry
                text_surface = font.render( text, True, color, bgColor )
                x, y = pos
                y = vh - y - text_surface.get_height()
                self.screen.blit( text_surface, (x,y) )
            self.textos = []

            # mostramos la pantalla
            pygame.display.flip()

    def _Fix_XY( self, pos, size ):
        xo, yo = pos
        wo, ho = size
        ww, wh = self.world.size
        vx, vy  = self.viewport.origin
        vw, vh = self.viewport.size
        dy = wh - (vy + vh)
        x = xo - vx
        y = wh - (yo + ho) - dy
        return x, y

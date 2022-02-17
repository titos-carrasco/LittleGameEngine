import time
import sys
import glob
import pygame

from lge.Rect import Rect


class Engine():
    CONSTANTS    = pygame.constants
    CAM_LAYER    = 0xFFFF

    def Init( worldSize, camSize, title, bgColor=(0,0,0) ):
        Engine.world = Rect( (0,0), worldSize )
        Engine.camera = Rect( (0,0), camSize )
        Engine.title = title
        Engine.bgColor = bgColor
        Engine.collidersColor = None

        Engine.fonts = {}
        Engine.sounds = {}
        Engine.images = {}

        Engine.gObjects = {}
        Engine.gObjectsToAdd = []
        Engine.gObjectsToDelete = []
        Engine.layers = {}

        Engine.mainTask = None
        Engine.camTarget = [ None, 0 ]

        Engine.events = []
        Engine.keysPressed = []

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.display.set_caption( Engine.title )
        Engine.screen = pygame.display.set_mode( Engine.camera.GetSize() )
        Engine.clock = pygame.time.Clock()


    # world
    def GetWorldSize():
        return Engine.world.GetSize()

    def KeepInsideWorld( gobj, newpos ):
        x, y = newpos
        w, h = gobj.GetSize()
        ww, wh = Engine.world.GetSize()
        if( x < 0 ): x = 0
        elif( x + w > ww ): x = ww - w
        if( y < 0 ): y = 0
        elif( y + h > wh ): y = wh - h
        return x, y


    # camera
    def SetCamPosition( position ):
        x, y = position
        w, h = Engine.camera.GetSize()
        x, y = Engine.KeepInsideWorld( Engine.camera, (int(x-w/2),int(y-h/2)) )
        Engine.camera.SetOrigin( (x,y) )

    def GetCamPosition():
        x, y = Engine.camera.GetOrigin()
        w, h = Engine.camera.GetSize()
        return int(x + w/2), int(y + h/2)

    def GetCamSize():
        return Engine.camera.GetSize()

    def SetCamTarget( gobj=None, center=True ):
        Engine.camTarget = (gobj,center)

    def _CamFollowTarget():
        gobj, center = Engine.camTarget
        if( gobj is None ): return
        _, layer = Engine.gObjects[gobj.name]
        if( layer == Engine.CAM_LAYER ):
            Engine.CAM_LAYER = [ None, 0 ]
            return

        x, y = gobj.GetPosition()
        w, h = gobj.GetSize()
        cw, ch = Engine.GetCamSize()
        if( center ):
            x = x + w/2
            y = y + h/2
        Engine.SetCamPosition( (x, y) )


    # gobjects
    def AddGObject( gobj, layer ):
        Engine.gObjectsToAdd.append( (gobj,layer&0xFFFF) )

    def DelGObject( name ):
        if( name == "*" ):
            for name in Engine.gObjects:
                Engine.gObjectsToDelete.append( name )
        elif( name[-1] == "*" ):
            s = name[:-1]
            for name in Engine.gObjects:
                if( name.startswith( s ) ):
                    Engine.gObjectsToDelete.append( name )
        else:
            Engine.gObjectsToDelete.append( name )

    def GetGObject( name ):
        if( name == "*" ):
            gobjs = []
            for name in Engine.gObjects:
                gobj, layer = Engine.gObjects[name]
                gobjs.append( gobj )
            return gobjs
        elif( name[-1] == "*" ):
            s = name[:-1]
            gobjs = []
            for name in Engine.gObjects:
                if( name.startswith( s ) ):
                    gobj, layer = Engine.gObjects[name]
                    gobjs.append( gobj )
            return gobjs
        elif( name in Engine.gObjects ):
            gobj, layer = Engine.gObjects[name]
            return gobj
        else:
            return None

    def ShowColliders( color=None ):
        Engine.collidersColor = color

    def GetCollisions( name ):
        gobj, layer = Engine.gObjects[name]
        gobjs = []
        if( layer != Engine.CAM_LAYER ):
            for o in Engine.layers[layer]:
                if( gobj != o and o.IsVisible() ):
                    crop = gobj.CollideGObject( o )
                    if( crop is not None ):
                        gobjs.append( (o,crop) )
        return gobjs


    # events
    def IsKeyDown( key ):
        for event in Engine.events:
            if( event.type == pygame.KEYDOWN ):
                if( event.key == key ):
                    return True
        return False

    def IsKeyUp( key ):
        for event in Engine.events:
            if( event.type == pygame.KEYUP ):
                if( event.key == key ):
                    return True
        return False

    def IsKeyPressed( key ):
        return True if Engine.keysPressed[ key ] else False

    def GetMousePos():
        x, y = pygame.mouse.get_pos()
        ww, wh = Engine.camera.GetSize()
        return x, wh - y

    def GetMousePressed():
        return pygame.mouse.get_pressed()


    # game
    def SetMainTask( task=None ):
        Engine.mainTask = task

    def GetFPS():
        return Engine.clock.get_fps()

    def Quit():
        pygame.quit()
        sys.exit()


    # main loop
    def Run( fps ):
        pygame.key.set_repeat( 0 )

        while( True ):
            # tiempo en ms desde el ciclo anterior
            dt = Engine.clock.tick( fps )

            # los eventos
            Engine.events = pygame.event.get()
            if( pygame.QUIT in [e.type for e in Engine.events] ):
                Engine.Quit()
            Engine.keysPressed = pygame.key.get_pressed()

            # los gobjects a eliminar
            for name in Engine.gObjectsToDelete:
                if( not name in Engine.gObjects ): continue
                gobj, layer = Engine.gObjects[name]
                del Engine.gObjects[name]

                gobjs = Engine.layers[layer]
                for idx in range( len( gobjs ) ):
                    if( gobjs[idx].name == name ):
                        break
                del Engine.layers[layer][idx]

                if( Engine.camTarget[0] == gobj ):
                    Engine.camTarget = [ None, 0 ]
            Engine.gObjectsToDelete = []

            # los gobjects nuevos
            for t in Engine.gObjectsToAdd:
                gobj, layer = t

                if( gobj.name in Engine.gObjects ): continue
                Engine.gObjects[gobj.name] = t

                if( not layer in Engine.layers ):
                    Engine.layers[layer] = []
                Engine.layers[layer].append( gobj )
            Engine.gObjectsToAdd = []

            # la logica de cada GameObject
            for layer in sorted( Engine.layers.keys() ):
                for gobj in Engine.layers[layer]:
                    if( hasattr( gobj, "OnUpdate" ) ):
                        gobj.OnUpdate( dt )

            # la logica del world
            if( Engine.mainTask ):
                Engine.mainTask( dt )

            # necesario si es que tiene seguimiento automatico
            Engine._CamFollowTarget()

            # el rendering
            Engine.screen.fill( Engine.bgColor )
            for layer in sorted( Engine.layers.keys() ):
                for gobj in Engine.layers[layer]:
                    if( not gobj.IsVisible() ): continue
                    if( layer == Engine.CAM_LAYER and hasattr( gobj, "surface" ) ):
                        x, y = gobj.GetPosition()
                        w, h = gobj.GetSize()
                        vw, vh = Engine.camera.size
                        Engine.screen.blit( gobj.surface, (x,vh-y-h) )
                    else:
                        if( gobj.CollideRect( Engine.camera ) ):
                            w, h = gobj.GetSize()
                            x, y = Engine._Fix_XY( gobj.GetPosition(), (w,h) )
                            if( hasattr( gobj, "surface" ) ):
                                Engine.screen.blit( gobj.surface, (x,y) )
                            if( Engine.collidersColor ):
                                pos = gobj.GetPosition()
                                size = gobj.GetSize()
                                pos = Engine._Fix_XY( pos, size )
                                points = [ (x,y), (x,y+h-1), (x+w-1,y+h-1), (x+w-1,y) ]
                                pygame.draw.lines( Engine.screen, Engine.collidersColor, True, points, 1 )

            # mostramos la pantalla
            pygame.display.update()

    def _Fix_XY( pos, size ):
        xo, yo = pos
        wo, ho = size
        ww, wh = Engine.world.size
        vx, vy  = Engine.camera.origin
        vw, vh = Engine.camera.size
        dy = wh - (vy + vh)
        x = xo - vx
        y = wh - (yo + ho) - dy
        return x, y

    #------------------------------------------------
    # metodos de la clase

    # fonts
    def GetSysFonts():
        return pygame.font.get_fonts()

    def LoadSysFont( name, size ):
        if( name in Engine.fonts ): return
        font = pygame.font.SysFont( name, size )
        Engine.fonts[name] = font

    def LoadTTFFont( name, size, path ):
        if( name in Engine.fonts ): return
        font = pygame.font.Font( path, size )
        Engine.fonts[name] = font


    # sonidos
    def LoadSound( name, fname ):
        Engine.sounds[name] = pygame.mixer.Sound( fname )

    def PlaySound( name, loop=0 ):
        Engine.sounds[name].play( loop )

    def StopSound( name ):
        Engine.sounds[name].stop()

    def SetSoundVolume( name, volume ):
        Engine.sounds[name].set_volume( volume )

    def GetSoundVolume( name ):
        return Engine.sounds[name].get_volume()


    # imagenes
    def LoadImage( iname, pattern ):
        if( "*" in pattern ): fnames = glob.glob( pattern )
        else: fnames = [pattern]

        fnames.sort()
        surfaces = []
        for fname in fnames:
            surfaces.append( pygame.image.load( fname ).convert_alpha() )
        Engine.images[iname] = surfaces

    def GetImages( iname ):
        images = []
        for image in Engine.images[iname]:
            images.append( image.copy() )
        return images

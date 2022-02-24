import glob
import pygame
from lge.Camera import Camera


class Engine():
    CONSTANTS    = pygame.constants
    VLIMIT       = 0xFFFFFFFF

    def Init( camSize, title, bgColor=(0,0,0) ):
        Engine.title = title
        Engine.bgColor = bgColor
        Engine.collidersColor = None

        Engine.fonts = {}
        Engine.sounds = {}
        Engine.images = {}

        Engine.gObjects = {}
        Engine.gObjectsToAdd = []
        Engine.gObjectsToDel = []

        Engine.camera = Camera( (0,0), camSize)
        Engine.cameraTarget = None, False

        Engine.keysUp = []
        Engine.keysPressed = []
        Engine.keysDown = []
        Engine.onUpdate = None
        Engine.running = False

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.key.set_repeat( 0 )
        pygame.display.set_caption( Engine.title )
        Engine.screen = pygame.display.set_mode( Engine.camera.GetSize() )
        Engine.clock = pygame.time.Clock()


    # camera
    def GetCamera():
        return Engine.camera

    def SetCameraTarget( gobj=None, center=False ):
        Engine.cameraTarget = gobj, center

    def _CameraFollowTarget():
        gobj, center = Engine.cameraTarget

        # nadie a quien seguir
        if( not gobj ): return

        # no debe ser GUI
        _, layer = Engine.gObjects[gobj.name]
        assert layer >= 0, "SetCameraTarget: 'gobj' invalido"

        # el centro de la camara en el centro del gobj
        x, y = gobj.GetPosition()
        if( center ):
            w, h = gobj.GetSize()
            x = x + w/2
            y = y + h/2

        cw, ch = Engine.camera.GetSize()
        Engine.camera.SetPosition( (x-cw/2, y-ch/2) )


    # gobjects
    def AddGObject( gobj, layer ):
        assert layer >= 0, "'layer' invalido"
        Engine.gObjectsToAdd.append( (gobj,layer) )

    def AddGObjectGUI( gobj ):
        Engine.gObjectsToAdd.append( (gobj,-1) )

    def DelGObject( name ):
        if( name == "*" ):
            for name in Engine.gObjects:
                Engine.gObjectsToDel.append( name )
        elif( name[-1] == "*" ):
            s = name[:-1]
            for name in Engine.gObjects:
                if( name.startswith( s ) ):
                    Engine.gObjectsToDel.append( name )
        else:
            Engine.gObjectsToDel.append( name )

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
        collisions = []
        for oname, ( o, olayer ) in Engine.gObjects.items():
            if( olayer != layer ): continue
            if( o == gobj ): continue
            if( not o.use_collider ): continue
            if( not o.IsVisible() ): continue
            if( not o.IsActive() ): continue

            if( gobj.rect.CollideRect( o.GetRect() ) ):
                collisions.append( o )
        return collisions

    # events
    def IsKeyDown( key ):
        return key in Engine.keysDown

    def IsKeyUp( key ):
        return key in Engine.keysUp

    def IsKeyPressed( key ):
        return Engine.keysPressed[ key ]

    def GetMousePos():
        x, y = pygame.mouse.get_pos()
        ww, wh = Engine.camera.GetSize()
        return x, wh - y

    def GetMousePressed():
        return pygame.mouse.get_pressed()


    # game
    def SetOnUpdate( func=None ):
        Engine.onUpdate = func

    def GetFPS():
        return Engine.clock.get_fps()

    def Quit():
        Engine.running = False

    # main loop
    def Run( fps ):
        Engine.running = True
        while( Engine.running ):
            # --- tiempo en ms desde el ciclo anterior
            dt = Engine.clock.tick( fps )/1000.0

            # system events
            Engine.keysUp = []
            Engine.keysDown = []
            for event in pygame.event.get():
                if( event.type == pygame.QUIT ): Engine.running = False
                elif( event.type == pygame.KEYUP ): Engine.keysUp.append( event.key )
                elif( event.type == pygame.KEYDOWN ): Engine.keysDown.append( event.key )
            Engine.keysPressed = pygame.key.get_pressed()

            reorder = False
            # --- gobj.OnStart
            onstart = []
            for t in Engine.gObjectsToAdd:
                gobj, layer = t
                assert not gobj.name in Engine.gObjects, "AddGObject: 'gobj' ya existe"
                Engine.gObjects[gobj.name] = t
                if( hasattr( gobj, "OnStart" ) ): onstart.append( gobj )
                reorder = True
            Engine.gObjectsToAdd = []
            for gobj in onstart:
                gobj.OnStart()

            # --- gobj.OnDelete
            ondelete = []
            for name in Engine.gObjectsToDel:
                assert gobj.name in Engine.gObjects, "DelObject: 'gobj' no existe"
                gobj, layer = Engine.gObjects[name]
                del Engine.gObjects[name]
                if( Engine.cameraTarget[0] == gobj ): Engine.cameraTarget = None, False
                if( hasattr( gobj, "OnDelete" ) ): ondelete.append( gobj )
                reorder = True
            Engine.gObjectsToDel = []
            for gobj in ondelete:
                gobj.OnDelete()

            # ---
            if( reorder ):
                Engine.gObjects = dict( sorted( Engine.gObjects.items(), key=lambda item: item[1][1] ) )
                reorder = False
            # --

            # --- gobj.OnPreUpdate
            for name, ( gobj, layer ) in Engine.gObjects.items():
                if( layer >= 0 and gobj.IsActive() and hasattr( gobj, "OnPreUpdate" ) ):
                    gobj.OnPreUpdate( dt )

            # --- gobj.OnUpdate
            for name, ( gobj, layer ) in Engine.gObjects.items():
                if( layer >= 0 and gobj.IsActive() and hasattr( gobj, "OnUpdate" ) ):
                    gobj.OnUpdate( dt )

            # --- gobj.OnPostUpdate
            for name, ( gobj, layer ) in Engine.gObjects.items():
                if( layer >= 0 and gobj.IsActive() and hasattr( gobj, "OnPostUpdate" ) ):
                    gobj.OnPostUpdate( dt )

            # --- game.OnUpdate
            if(  Engine.onUpdate ):
                Engine.onUpdate( dt )

            # --- Camera Tracking
            Engine._CameraFollowTarget()

            # -- Layer Rendering
            Engine.screen.fill( Engine.bgColor )
            for name, ( gobj, layer ) in Engine.gObjects.items():
                if( layer < 0 ): continue
                if( not gobj.IsVisible() ): continue
                if( not gobj.IsActive() ): continue
                if( not gobj.GetRect().CollideRect( Engine.camera.GetRect() ) ): continue

                w, h = gobj.GetSize()
                x, y = Engine._Fix_XY( gobj.GetPosition(), (w,h) )

                if( hasattr( gobj, "surface" ) ):
                    Engine.screen.blit( gobj.surface, (x,y) )

                if( Engine.collidersColor and gobj.use_collider ):
                    points = [ (x,y), (x,y+h-1), (x+w-1,y+h-1), (x+w-1,y) ]
                    pygame.draw.lines( Engine.screen, Engine.collidersColor, True, points, 1 )

            # --- GUI rendering
            for name, ( gobj, layer ) in Engine.gObjects.items():
                if( layer >= 0 ): continue
                if( not gobj.IsVisible() ): continue
                if( not gobj.IsActive() ): continue
                if( not hasattr( gobj, "surface" )): continue

                x, y = gobj.GetPosition()
                w, h = gobj.GetSize()
                vw, vh = Engine.camera.GetSize()
                Engine.screen.blit( gobj.surface, (x,vh-y-h) )

            # ---
            pygame.display.update()

        # eso es todo
        pygame.quit()

    # sistema cartesiano y zona visible dada por la camara
    def _Fix_XY( pos, size ):
        xo, yo = pos
        wo, ho = size
        wh = Engine.VLIMIT
        vx, vy  = Engine.camera.GetPosition()
        vw, vh = Engine.camera.GetSize()
        dy = wh - (vy + vh)
        x = xo - vx
        y = wh - (yo + ho) - dy
        return x, y

    # --- Recursos

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
    def LoadImage( iname, pattern, scale=None, flip=None ):
        if( "*" in pattern ): fnames = sorted( glob.glob( pattern ) )
        else: fnames = [pattern]

        if( flip ): fx, fy = flip
        surfaces = []
        for fname in fnames :
            surface = pygame.image.load( fname ).convert_alpha()
            if( scale ):
                if( not isinstance( scale, tuple ) ):
                    w, h = surface.get_size()
                    scale = ( int(w*scale),int(h*scale) )
                surface = pygame.transform.smoothscale( surface, scale )
            if( flip ):
                surface = pygame.transform.flip( surface, fx, fy )
            surfaces.append( surface )
        Engine.images[iname] = surfaces

    def GetImages( iname ):
        return [ image for image in Engine.images[iname] ]

from glob import glob
import pygame

from lge.Camera import Camera
from lge.Rectangle import Rectangle


class Engine():
    CONSTANTS        = pygame.constants
    VLIMIT           = 0xFFFFFFFF
    GUI_LAYER        = 0xFFFF

    E_ON_DELETE      = 0x00000001
    E_ON_START       = 0x00000010
    E_ON_PRE_UPDATE  = 0x00000100
    E_ON_UPDATE      = 0x00001000
    E_ON_POST_UPDATE = 0x00010000
    E_ON_COLLISION   = 0x00100000
    E_ON_PRE_RENDER  = 0x01000000
    E_ON_QUIT        = 0x01000000

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

        Engine.camera = Camera( ( 0, 0 ), camSize )
        Engine.cameraTarget = None, False

        Engine.events = []
        Engine.keys_pressed = []
        Engine.onUpdate = None
        Engine.running = False
        Engine.on_events_enabled = Engine.E_ON_UPDATE

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.key.set_repeat( 0 )
        pygame.display.set_caption( Engine.title )
        Engine.screen = pygame.display.set_mode( Engine.camera.GetSize() )
        Engine.clock = pygame.time.Clock()


    # gobjects
    def AddGObject( gobj, layer ):
        assert not hasattr( gobj, "_layer" ), "'gobj' ya fue agregado"
        assert layer >= 0 and layer <= Engine.GUI_LAYER, "'layer' invalido"
        gobj._layer = layer
        Engine.gObjectsToAdd.append( gobj )

    def AddGObjectGUI( gobj ):
        Engine.AddGObject( gobj, Engine.GUI_LAYER )

    def GetGObject( name ):
        if( name == "*" ):
            return [ gobj for layer, gobjs in Engine.gObjects.items() for gobj in gobjs ]
        elif( name[-1] == "*" ):
            s = name[:-1]
            return [ gobj for layer, gobjs in Engine.gObjects.items() for gobj in gobjs if gobj._name.startswith( s ) ]
        else:
            gobjs = [ gobj for layer, gobjs in Engine.gObjects.items() for gobj in gobjs if gobj._name == name ]
            if( not gobjs ): return None
            else: return gobjs[0]

    def DelGObject( gobj ):
        assert hasattr( gobj, "_layer" ), "'gobj' no ha sido agregado"
        Engine.gObjectsToDel.append( gobj )

    def DelGObjectByName( name ):
        if( name == "*" ):
            gobjs = Engine.GetGObject( name )
            Engine.gObjectsToDel.extend( gobjs )
        elif( name[-1] == "*" ):
            gobjs = Engine.GetGObject( name )
            Engine.gObjectsToDel.extend( gobjs )
        else:
            gobj = Engine.GetGObject( name )
            assert not gobj is None, "gobj no existe"
            Engine.DelGObject( gobj )

    def ShowColliders( color=None ):
        Engine.collidersColor = color

    def GetCollisions( gobj ):
        return [ o
                    for o in Engine.gObjects[gobj._layer]
                        if o != gobj and \
                           o._use_colliders and \
                           gobj._rect.CollideRectangle( o._rect )
                ]


    # camera
    def GetCamera():
        return Engine.camera

    def SetCameraTarget( gobj=None, center=False ):
        assert hasattr( gobj, "_layer" ), "'gobj' no ha sido agregado"
        assert gobj._layer != Engine.GUI_LAYER, "'gobj' invalido"

        Engine.cameraTarget = gobj, center

    def _CameraFollowTarget():
        gobj, center = Engine.cameraTarget

        # nadie a quien seguir
        if( not gobj ): return

        # el centro de la camara en el centro del gobj
        x, y = gobj.GetPosition()
        if( center ):
            w, h = gobj.GetSize()
            x = x + w/2
            y = y + h/2

        cw, ch = Engine.camera.GetSize()
        Engine.camera.SetPosition( int(x-cw/2), int(y-ch/2) )


    # events
    def KeyDown( key ):
        return key in [ e.key for e in Engine.events if e.type == pygame.KEYDOWN ]

    def KeyUp( key ):
        return key in [ e.key for e in Engine.events if e.type == pygame.KEYUP ]

    def KeyPressed( key ):
        return Engine.keys_pressed[ key ]

    def GetMousePosition():
        x, y = pygame.mouse.get_pos()
        ww, wh = Engine.camera.GetSize()
        return x, wh - y

    def GetMouseButtons():
        return pygame.mouse.get_pressed()

    def GetMousePressed( button ):
        events = [ e for e in Engine.events if e.type == pygame.MOUSEBUTTONDOWN ]
        if( not events ): return None

        e = events[0]
        if( e.button != button ): return None

        x, y = e.pos
        ww, wh = Engine.camera.GetSize()
        return x, wh - y

    def GetMouseReleased( button ):
        events = [ e for e in Engine.events if e.type == pygame.MOUSEBUTTONUP ]
        if( not events ): return None

        e = events[0]
        if( e.button != button ): return None

        x, y = e.pos
        ww, wh = Engine.camera.GetSize()
        return x, wh - y

    # game
    def SetOnUpdate( func=None ):
        Engine.onUpdate = func

    def GetFPS():
        return Engine.clock.get_fps()

    def GetRequestedFPS():
        return Engine.fps

    def Quit():
        Engine.running = False

    def EnableOnEvent( *events ):
        for e in events:
            Engine.on_events_enabled |= e

    def DisableOnEvent( *events ):
        for e in events:
            Engine.on_events_enabled &= ~e

    # main loop
    def Run( fps ):
        Engine.fps = 1.0/fps
        Engine.running = True
        while( Engine.running ):
            # --- tiempo en ms desde el ciclo anterior
            dt = Engine.clock.tick( fps )/1000.0

            # system events
            Engine.events = pygame.event.get()
            for event in Engine.events:
                if( event.type == pygame.QUIT ): Engine.running = False
            Engine.keys_pressed = pygame.key.get_pressed()

           # --- Del gobj and gobj.OnDelete
            ondelete = []
            for gobj in Engine.gObjectsToDel:
                Engine.gObjects[gobj._layer].remove( gobj )
                del gobj._layer
                if( Engine.cameraTarget == gobj ):
                    Engine.cameraTarget = None, False
                if( hasattr( gobj, "OnDelete" ) ): ondelete.append( gobj )
            Engine.gObjectsToDel = []
            if( Engine.on_events_enabled & Engine.E_ON_DELETE ):
                for gobj in ondelete: gobj.OnDelete()

            # --- Add Gobj and gobj.OnStart
            reorder = False
            onstart = []
            for gobj in Engine.gObjectsToAdd:
                if( not gobj._layer in Engine.gObjects ):
                    Engine.gObjects[gobj._layer] = []
                    reorder = True
                Engine.gObjects[gobj._layer].append( gobj )
                if( hasattr( gobj, "OnStart" ) ): onstart.append( gobj )
            Engine.gObjectsToAdd = []
            if( Engine.on_events_enabled & Engine.E_ON_START ):
                for gobj in onstart: gobj.OnStart()

            # ---
            if( reorder ):
                Engine.gObjects = dict( sorted( Engine.gObjects.items() ) )
                reorder = False
            # --

            # --- gobj.OnPreUpdate
            if( Engine.on_events_enabled & Engine.E_ON_PRE_UPDATE ):
                list( gobj.OnPreUpdate( dt ) for layer, gobjs in Engine.gObjects.items() for gobj in gobjs if hasattr( gobj, "OnPreUpdate" ) )

            # --- gobj.OnUpdate
            if( Engine.on_events_enabled & Engine.E_ON_UPDATE ):
                list( gobj.OnUpdate( dt ) for layer, gobjs in Engine.gObjects.items() for gobj in gobjs if hasattr( gobj, "OnUpdate" ) )

            if( Engine.on_events_enabled & Engine.E_ON_POST_UPDATE ):
            # --- gobj.OnPostUpdate
                list( gobj.OnPostUpdate( dt ) for layer, gobjs in Engine.gObjects.items() for gobj in gobjs if hasattr( gobj, "OnPostUpdate" ) )

            # --- game.OnUpdate
            if( Engine.onUpdate ): Engine.onUpdate( dt )

            # --- gobj.OnCollision
            if( Engine.on_events_enabled & Engine.E_ON_COLLISION ):
                oncollisions = []
                for layer, gobjs in Engine.gObjects.items():
                    if( layer == Engine.GUI_LAYER ): continue
                    with_use_colliders = list( ( gobj, gobj.GetRectangle() ) for gobj in gobjs if gobj._use_colliders )
                    with_on_collision = list( ( gobj, rect ) for gobj, rect in with_use_colliders if hasattr( gobj, "OnCollision" ) )

                    for o1, r1 in with_on_collision:
                        o1_collisions = []
                        for o2, r2 in with_use_colliders:
                            if o1 != o2:
                                if r1.CollideRectangle( r2 ):
                                    o1_collisions.append( ( o2, r2 ) )
                        oncollisions.append( ( o1, o1_collisions ) )
                list( gobj.OnCollision( dt, collisions ) for gobj, collisions in oncollisions if collisions )

            # --- gobj.OnPreRender
            if( Engine.on_events_enabled & Engine.E_ON_PRE_RENDER ):
                list( gobj.OnPreRender( dt ) for layer, gobjs in Engine.gObjects.items() for gobj in gobjs if hasattr( gobj, "OnPreRender" ) )

            # --- Camera Tracking
            Engine._CameraFollowTarget()

            # -- Rendering
            Engine.screen.fill( Engine.bgColor )

            vw, vh = Engine.camera.GetSize()
            rect_camera = Engine.camera.GetRectangle()
            for layer, gobjs in Engine.gObjects.items():
                # -- Layer Rendering
                if( layer != Engine.GUI_LAYER ):
                    for gobj in [ gobj for gobj in gobjs if( gobj.GetRectangle().CollideRectangle( rect_camera ) ) ]:
                        w, h = gobj.GetSize()
                        x, y = Engine._Fix_XY( gobj.GetPosition(), (w,h) )

                        if( hasattr( gobj, "_surface" ) ):
                            Engine.screen.blit( gobj._surface, (x,y) )

                        if( Engine.collidersColor and gobj._use_colliders ):
                            pygame.draw.rect( Engine.screen, Engine.collidersColor, pygame.Rect( (x,y), (w,h) ), 1 )

                # --- GUI rendering
                else:
                    for gobj in gobjs:
                        if hasattr( gobj, "_surface" ):
                            x, y = gobj.GetPosition()
                            w, h = gobj.GetSize()
                            Engine.screen.blit( gobj._surface, (x,vh-y-h) )

            # ---
            pygame.display.update()

        # --- gobj.OnPreRender
        if( Engine.on_events_enabled & Engine.E_ON_QUIT):
            list( gobj.OnQuit() for layer, gobjs in Engine.gObjects.items() for gobj in gobjs if hasattr( gobj, "OnQuit" ) )

        # eso es todo
        pygame.quit()

    # sistema cartesiano y zona visible dada por la camara
    def _Fix_XY( pos, size ):
        xo, yo = pos
        wo, ho = size
        wh = Engine.VLIMIT
        vx, vy  = Engine.camera._rect._x1, Engine.camera._rect._y1
        vw, vh = Engine.camera._rect._w, Engine.camera._rect._h
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
        if( "*" in pattern ): fnames = sorted( glob( pattern ) )
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

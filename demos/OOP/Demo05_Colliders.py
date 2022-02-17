from random import random
from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Text import Text
from lge.Rect import Rect

class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (640,480), "Colliders" )
        Engine.SetWorldBounds( Rect( (0,0), (1920,1056) ) )
        Engine.SetMainTask( self.MainControl )

        # activamos la musica de fondo
        Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        Engine.PlaySound( "fondo", loop=-1 )

        # cargamos los recursos que usaremos
        Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
        Engine.LoadImage( "idle", "../images/Swordsman/Idle/Idle_0*.png" )
        Engine.LoadImage( "run", "../images/Swordsman/Run/Run_0*.png" )
        Engine.LoadImage( "ninja", "../images/Swordsman/Idle/Idle_000.png" )
        Engine.LoadTTFFont( "monospace", 20, "../fonts/FreeMono.ttf" )
        Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        Engine.LoadSound( "aves", "../sounds/bird-thrush-nightingale.wav" )
        Engine.LoadSound( "poing", "../sounds/cartoon-poing.wav" )
        Engine.SetSoundVolume( "poing", 0.1 )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        Engine.AddGObject( fondo, 0 )

        # agregamos al heroe
        heroe = MiHeroe()
        Engine.AddGObject( heroe, 1 )

        # agregamos otro ninja
        gobj = Sprite( "ninja", (350,250) )
        gobj.Scale( 0.16 )
        Engine.AddGObject( gobj, 1 )

        # agregamos la barra de info
        infobar = Text( None, (0,460), "monospace", (0,0,0), None, "infobar" )
        Engine.AddGObject( infobar, Engine.CAM_LAYER )

        # establecemos que la camara siga al heroe en su origen
        Engine.SetCamTarget( heroe, False )

        # para visualizar el despliegue de los contornos de los objetos
        Engine.ShowColliders( (0xFF,0x00,0x00) )
        self.showColliders = True

    def MainControl( self, dt ):
        # abortamos con la tecla Escape
        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_ESCAPE ) ):
            Engine.Quit()

        # mostramos los FPS actuales y datos del mouse
        fps = Engine.GetFPS()
        fps = "FPS: %07.2f" % fps

        mx, my = Engine.GetMousePos()
        mb1, mb2, mb3 = Engine.GetMousePressed()
        minfo = "Mouse: (%4d,%4d) (%d,%d,%d)" % ( mx, my, mb1, mb2, mb3 )

        info = Engine.GetGObject( "infobar" )
        info.SetText( fps + " "*15 + minfo )

        # mostramos los bordes
        if( Engine.IsKeyUp( Engine.CONSTANTS.K_c) ):
            self.showColliders = not self.showColliders
            if( self.showColliders ):
                Engine.ShowColliders( (0xFF, 0x00, 0x00) )
            else:
                Engine.ShowColliders()

        # de manera aleatorio activamos sonido de aves
        n = int( random()*1000 )
        if( n < 3 ):
            Engine.PlaySound( "aves", 0 )

    # main loop
    def Run( self ):
        Engine.Run( 60 )


class MiHeroe( Sprite ):
    def __init__( self ):
        # agregamos el heroe con diferentes imagenes
        super().__init__( ["idle","run"], (550,346), "Heroe" )
        self.Scale( 0.16 )
        self.SetShape( 0, "idle" )
        self.heading = 1

    def TestCollisions( self, dt ):
        crops = Engine.GetCollisions( self.name )
        if( len(crops) == 0 ): return

        Engine.PlaySound( "poing", 0 )

        obj, r = crops[0]
        xr, yr = r.GetOrigin()
        wr,hr = r.GetSize()
        x, y = self.GetPosition()
        w, h = self.GetSize()

        # viene horizontal
        if( hr > wr ):
            if( xr == x ):
                x = xr + wr + 1
            else:
                x = xr - w
        else:
            if( yr == y ):
                y = yr + hr + 1
            else:
                y = yr - h

        self.SetPosition( (x,y) )

    def OnUpdate( self, dt ):
        # moveremos al heroe "ppm" pixeles por minuto
        ppm = 240
        pixels = (ppm*dt)/1000

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
        moving = False
        idx, name = self.GetCurrentShape()
        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_RIGHT ) ):
            x = x + pixels
            if( self.heading != 1 ):
                self.Flip( True, False )
                self.heading = 1
            if( name != "run" ):
                self.SetShape( 0, "run" )
            moving = True
        elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_LEFT ) ):
            x = x - pixels
            if( self.heading != -1 ):
                self.Flip( True, False )
                self.heading = -1
            if( name != "run" ):
                self.SetShape( 0, "run" )
            moving = True

        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_DOWN ) ):
            y = y - pixels
            moving = True
        elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_UP ) ):
            y = y + pixels
            moving = True

        if( not moving and name != "idle" ):
                self.SetShape( 0, "idle" )

        # siguiente imagen de la secuencia
        self.NextShape( dt, 50 )

        # lo posicionamos asegurando que se encuentre dentro del mundo definido
        self.SetPosition( (x,y), Engine.GetWorldBounds() )

        # vemos las colisiones
        self.TestCollisions( dt )


#--- show time
game = MiJuego()
game.Run()

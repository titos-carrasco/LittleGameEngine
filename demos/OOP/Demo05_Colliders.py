from random import random
from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Text import Text
from lge.Rect import Rect


class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (640,480), "Colliders" )
        Engine.SetUpdate( self.MainUpdate )

        # activamos la musica de fondo
        Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        Engine.PlaySound( "fondo", loop=-1 )

        # cargamos los recursos que usaremos
        Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
        Engine.LoadImage( "heroe_idle_right", "../images/Swordsman/Idle/Idle_0*.png", 0.16 )
        Engine.LoadImage( "heroe_idle_left", "../images/Swordsman/Idle/Idle_0*.png", 0.16, (True,False) )
        Engine.LoadImage( "heroe_run_right", "../images/Swordsman/Run/Run_0*.png", 0.16 )
        Engine.LoadImage( "heroe_run_left", "../images/Swordsman/Run/Run_0*.png", 0.16, (True,False) )
        Engine.LoadImage( "ninja", "../images/Swordsman/Idle/Idle_000.png", 0.16 )
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
        Engine.AddGObject( gobj, 1 )

        # agregamos la barra de info
        infobar = Text( None, (0,460), "monospace", (0,0,0), None, "infobar" )
        Engine.AddGObject( infobar, Engine.CAM_LAYER )

        # configuramos la camara
        camera = Engine.GetCamera()
        camera.SetBounds( Rect( (0,0), (1920,1056) ) )

        # establecemos que la camara siga al heroe en su origen
        Engine.SetCameraTarget( heroe, False )

        # para visualizar el despliegue de los contornos de los objetos
        Engine.ShowColliders( (0xFF,0x00,0x00) )
        self.showColliders = True

    def MainUpdate( self, dt ):
        # abortamos con la tecla Escape
        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_ESCAPE ) ):
            Engine.Quit()

        # mostramos info
        fps = Engine.GetFPS()
        fps = "FPS: %07.2f" % fps

        ngobjs = len( Engine.GetGObject( "*") )
        ngobjs = "gObjs: %03d" % ngobjs

        mx, my = Engine.GetMousePos()
        mb1, mb2, mb3 = Engine.GetMousePressed()
        minfo = "Mouse: (%3d,%3d) (%d,%d,%d)" % ( mx, my, mb1, mb2, mb3 )

        info = Engine.GetGObject( "infobar" )
        info.SetText( fps + " - " + ngobjs + " - " + minfo )

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
        super().__init__( ["heroe_idle_right","heroe_idle_left","heroe_run_right","heroe_run_left"], (550,346), "Heroe" )
        self.SetShape( "heroe_idle_right", 0 )
        self.heading = 1


    def OnUpdate( self, dt ):
        # moveremos al heroe "pps" pixeles por segundo
        pps = 240
        pixels = round( (pps*dt)/1000 )

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
        moving = False
        name, idx = self.GetCurrentShape()
        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_RIGHT ) ):
            x = x + pixels
            if( self.heading != 1 ):
                self.heading = 1
            if( name[:9] != "heroe_run" ):
                self.SetShape( "heroe_run_right", 0 )
            moving = True
        elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_LEFT ) ):
            x = x - pixels
            if( self.heading != -1 ):
                self.heading = -1
            if( name[:9] != "heroe_run" ):
                self.SetShape( "heroe_run_left", 0 )
            moving = True

        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_DOWN ) ):
            y = y - pixels
            moving = True
        elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_UP ) ):
            y = y + pixels
            moving = True

        if( not moving and name[:10] != "heroe_idle" ):
            if( self.heading == 1 ): self.SetShape( "heroe_idle_right", 0 )
            else: self.SetShape( "heroe_idle_left", 0 )

        # siguiente imagen de la secuencia
        self.NextShape( dt, 50 )

        # lo posicionamos asegurando que se encuentre dentro del mundo definido
        camera = Engine.GetCamera()
        bounds = camera.GetBounds()
        self.SetPosition( (x,y), bounds )

        # verificamos si hemos colisionado
        collisions = Engine.GetCollisions( self.name )
        if( collisions ):
            Engine.PlaySound( "poing", 0 )

            obj, r = collisions[0]
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

#--- show time
game = MiJuego()
game.Run()

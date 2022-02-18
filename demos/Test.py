import uuid
import random
import time

from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Text import Text
from lge.Rect import Rect


class Test():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (800,440), "The World" )
        Engine.SetUpdate( self.MainUpdate )

        # activamos la musica de fondo
        Engine.LoadSound( "fondo", "./sounds/happy-and-sad.wav" )
        Engine.PlaySound( "fondo", loop=-1 )

        # cargamos los recursos que usaremos
        Engine.LoadImage( "fondo", "./images/Backgrounds/FreeTileset/Fondo.png" )
        Engine.LoadImage( "heroe", "./images/Swordsman/Idle/Idle_00*.png" )
        Engine.LoadImage( "bird", "./images/BlueBird/frame-*.png" )
        Engine.LoadTTFFont( "monospace", 20, "./fonts/FreeMono.ttf" )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        fondo.ReSize( (800,440) )
        Engine.AddGObject( fondo, 0 )

        # agregamos la barra de info
        infobar = Text( None, (0,420), "monospace", (0,0,0), None, "infobar" )
        Engine.AddGObject( infobar, Engine.CAM_LAYER )

        # agregamos al heroe
        heroe = Sprite( "heroe", (226,142), "Heroe" )
        heroe.Scale( 0.08 )
        heroe.OnUpdate = lambda dt: heroe.NextShape(dt,60)
        Engine.AddGObject( heroe, 2 )

        # agregamos pajaros
        ww, wh = Engine.GetCamera().GetSize()
        start = time.time()
        for i in range( 500 ):
            x = int( random.random()*ww )
            y = int( random.random()*(wh - 40) )
            bird = Bird( "bird", (x,y) )
            bird.Scale( 0.04 )
            Engine.AddGObject( bird, 1 )
        end = time.time()
        print( end - start )

    def MainUpdate( self, dt ):
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

    # main loop
    def Run( self ):
        Engine.Run( 60 )


class Bird(Sprite):
    def __init__( self, inames, position ):
        super().__init__( inames, position )

    def OnUpdate( self, dt ):
        self.NextShape( dt, 60)

# ----
test=Test()
test.Run()

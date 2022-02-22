import random

from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Canvas import Canvas


class Test():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (800,440), "The World" )
        Engine.SetUpdate( self.MainUpdate )

        # activamos la musica de fondo
        Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        Engine.PlaySound( "fondo", loop=-1 )

        # cargamos los recursos que usaremos
        Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png", (800,440) )
        Engine.LoadImage( "heroe", "../images/Swordsman/Idle/Idle_00*.png", 0.08 )
        Engine.LoadImage( "bird", "../images/BlueBird/frame-*.png", 0.04 )
        Engine.LoadTTFFont( "monospace", 20, "../fonts/FreeMono.ttf" )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        Engine.AddGObject( fondo, 0 )

        # agregamos la barra de info
        infobar =Canvas( (0,420), (800,20), "infobar" )
        Engine.AddGObject( infobar, Engine.CAM_LAYER )

        # agregamos al heroe
        heroe = Sprite( "heroe", (226,142), "Heroe" )
        heroe.OnUpdate = lambda dt: heroe.NextShape( dt, 0.060 )
        Engine.AddGObject( heroe, 2 )

        # agregamos pajaros
        ww, wh = Engine.GetCamera().GetSize()
        for i in range( 500 ):
            x = int( random.random()*ww )
            y = int( random.random()*(wh - 40) )
            bird = Bird( "bird", (x,y) )
            Engine.AddGObject( bird, 1 )

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

        infobar = Engine.GetGObject( "infobar" )
        infobar.Fill( (0,0,0,20) )
        infobar.DrawText( fps + "    -    " + ngobjs + "    -    " + minfo, (0,0), "monospace", (0,0,0) )

    # main loop
    def Run( self ):
        Engine.Run( 60 )


class Bird(Sprite):
    def __init__( self, inames, position ):
        super().__init__( inames, position )

    def OnUpdate( self, dt ):
        self.NextShape( dt, 0.060 )

# ----
test=Test()
test.Run()

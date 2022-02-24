from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rect import Rect

from BlockHorizontal import BlockHorizontal


class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (800,600), "Vulcano" )
        camera = Engine.GetCamera()
        camera.SetBounds( Rect( (0,0), (2560,704) ) )
        camera.SetPosition( (0,0) )

        # cargamos algunos recursos
        Engine.LoadImage( "fondo", "../images/Platform/Platform.png" )
        Engine.LoadImage( "roca", "../images/Volcano_Pack_1.1/volcano_pack_alt_39.png" )
        Engine.LoadImage( "ninja", "../images/Swordsman/Idle/Idle_0*.png", 0.16 )
        Engine.LoadTTFFont( "monospace", 16, "../fonts/LiberationMono-Regular.ttf" )
        Engine.LoadTTFFont( "cool", 30, "../fonts/backlash.ttf" )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        Engine.AddGObject( fondo, 0 )

        # agregamos la barra de info
        infobar = Canvas( (0,684), (800,20), "infobar" )
        Engine.AddGObjectGUI( infobar )

        # agregamos el ninja
        ninja = Sprite( "ninja", (340,300), "ninja" )
        ninja.OnUpdate = self.NinjaUpdate
        Engine.AddGObjectGUI( ninja )

        # agregamos el bloque que se mueve vertical
        bloque = BlockHorizontal( (13*64, 1*64) )
        Engine.AddGObject( bloque, 1 )

        # agregamos el mensaje
        pressbar = Canvas( (200,260), (400, 30), "pressbar" )
        pressbar.DrawText( "Presiona la Barra Espaciadora", (0,0), "cool", (255,255,255) )
        Engine.AddGObjectGUI( pressbar )

        # agregamos el control del juego
        self.camRight = True
        Engine.SetOnUpdate( self.MainUpdate )

    def MainUpdate( self, dt ):
        # velocity = pixeles por segundo
        velocity = 240
        pixels = velocity*dt

        # verificamos la salida
        self.CheckEscape()

        # movemos la camara
        camera = Engine.GetCamera()
        x, y = camera.GetPosition()

        if( self.camRight ): x = x + pixels
        else: x = x - pixels
        camera.SetPosition( (x,y) )

        xn, yn = camera.GetPosition()
        if( xn != x ): self.camRight = not self.camRight

        # verificamos si se ha presionada la barra espaciadora
        if( not Engine.IsKeyDown( Engine.CONSTANTS.K_SPACE ) ): return

        # reposicionamos la camara
        camera.SetPosition( (0,0) )

    def NinjaUpdate( self, dt ):
        ninja = Engine.GetGObject( "ninja" )
        ninja.NextShape( dt, 0.050 )

    # barra de info
    def CheckEscape( self ):
        # abortamos con la tecla Escape
        if( Engine.IsKeyDown( Engine.CONSTANTS.K_ESCAPE ) ):
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
        infobar.Fill( (0,0,0,50) )
        infobar.DrawText( fps + " - " + ngobjs + " - " + minfo, (120,0), "monospace", (255,255,255) )
    # main loop
    def Run( self ):
        Engine.Run( 60 )


# -- show time
game = MiJuego()
game.Run()

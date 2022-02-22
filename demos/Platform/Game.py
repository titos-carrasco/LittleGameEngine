from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rect import Rect

from BlockHorizontal import BlockHorizontal


class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (800,704), "Vulcano" )
        Engine.GetCamera().SetBounds( Rect( (0,0), (2560,704) ) )

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
        Engine.AddGObject( infobar, Engine.CAM_LAYER )

        # agregamos el ninja en la camara
        ninja = Sprite( "ninja", (340,370), "ninja" )
        ninja.OnUpdate = self.NinjaUpdate
        Engine.AddGObject( ninja, Engine.CAM_LAYER )

        # Dejamos lista la escena
        self.EscenaIntro()

    def NinjaUpdate( self, dt ):
        ninja = Engine.GetGObject( "ninja" )
        ninja.NextShape( dt, 0.050 )

    # main loop
    def Run( self ):
        Engine.Run( 60 )

    # barra de info
    def CheckEscape( self ):
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
        infobar.Fill( (0,0,0,50) )
        infobar.DrawText( fps + " - " + ngobjs + " - " + minfo, (120,0), "monospace", (255,255,255) )

    #-------------------------------------------------------------------------------------------
    def EscenaIntro( self ):
        # posicionamos la camara
        Engine.GetCamera().SetPosition( (0,0) )

        # el bloque que se mueve horizontal
        bloque = BlockHorizontal( (13*64, 1*64) )
        Engine.AddGObject( bloque, 1 )

        # agregamos mensaje
        pressbar = Canvas( (200,340), (400, 30), "pressbar" )
        pressbar.DrawText( "Presiona la Barra Espaciadora", (0,0), "cool", (255,255,255) )
        Engine.AddGObject( pressbar, Engine.CAM_LAYER )

        # agregamos el control de esta escena
        self.camRight = True
        Engine.SetUpdate( self.IntroUpdate )

    def IntroUpdate( self, dt ):
        # moveremos la camara "pps" pixeles por segundo
        pps = 240
        pixels = pps*dt

        # verificamos ESCP
        self.CheckEscape()

        # novemos la camara
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


# -- show time
game = MiJuego()
game.Run()

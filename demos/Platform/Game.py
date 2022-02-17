from lge.Sprite import Sprite
from lge.Text import Text
from lge.Engine import Engine

from BlockHorizontal import BlockHorizontal

class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (2560,704), (800,704), "Vulcano", (0xFF, 0xFF, 0xFF) )

        # cargamos algunos recursos
        Engine.LoadImage( "fondo", "../images/Platform/Platform.png" )
        Engine.LoadImage( "roca", "../images/Volcano_Pack_1.1/volcano_pack_alt_39.png" )
        Engine.LoadImage( "ninja", "../images/Swordsman/Idle/Idle_0*.png" )
        Engine.LoadTTFFont( "Monospace 20", 20, "../fonts/LiberationMono-Regular.ttf" )
        Engine.LoadTTFFont( "Cool 30", 30, "../fonts/backlash.ttf" )


        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        Engine.AddGObject( fondo, 0 )

        # agregamos la barra de info
        infobar = Text( None, (0,680), "Monospace 20", (255,255,255), None, "infobar" )
        Engine.AddGObject( infobar, Engine.CAM_LAYER )

        # agregamos el ninja en la camara
        ninja = Sprite( "ninja", (320,370), "ninja" )
        ninja.Scale( 0.16 )
        ninja.OnUpdate = self._ninja
        Engine.AddGObject( ninja, Engine.CAM_LAYER )

        # Dejamos lista la escena
        self.InitEscenaIntro()

    def _ninja( self, dt ):
        ninja = Engine.GetGObject( "ninja" )
        ninja.NextShape( dt, 50 )

    # main loop
    def Run( self ):
        Engine.Run( 60 )

    # barra de info
    def CheckEscape( self ):
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
        info.SetText( fps + " "*28 + minfo )

    #-------------------------------------------------------------------------------------------
    def InitEscenaIntro( self ):
        # posicionamos la camara
        Engine.SetCamPosition( (0,0) )

        # el bloque que se mueve horizontal
        bloque = BlockHorizontal( (13*64, 1*64) )
        Engine.AddGObject( bloque, 1 )

        # agregamos mensaje
        pressbar = Text( "Presiona la Barra Espaciadora", (200,340), "Cool 30", (255,255,255) )
        Engine.AddGObject( pressbar, Engine.CAM_LAYER )

        # agregamos el control de esta escena
        self.camRight = True
        Engine.SetMainTask( self.ControlEscenaIntro )

    def ControlEscenaIntro( self, dt ):
        # movemos la camara "ppm" pixeles por minuto
        ppm = 120
        pixels = round( (ppm*dt)/1000 )

        self.CheckEscape()

        x, y = Engine.GetCamPosition()
        if( self.camRight ): x = x + pixels
        else: x = x - pixels
        Engine.SetCamPosition( (x,y) )
        xn, yn = Engine.GetCamPosition()
        if( xn != x ): self.camRight = not self.camRight

        # verificamos si se ha presionada la barra espaciadora
        if( not Engine.IsKeyDown( Engine.CONSTANTS.K_SPACE ) ): return

        # reposicionamos la camara
        Engine.SetCamPosition( (0,0) )


# -- show time
game = MiJuego()
game.Run()

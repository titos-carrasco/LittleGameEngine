from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.LGE import LGE

from BlockHorizontal import BlockHorizontal

class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (2560,704), (800,704), "Vulcano", (0xFF, 0xFF, 0xFF) )
        self.engine.SetFPS( 60 )

        # cargamos algunos fonts
        # self.engine.LoadSysFont( "consolas", 20 )
        self.engine.LoadTTFFont( "Monospace 20", 20, "../fonts/LiberationMono-Regular.ttf" )
        self.engine.LoadTTFFont( "Cool 30", 30, "../fonts/backlash.ttf" )

        # posicionamos la camara
        self.engine.SetCamPosition( (0,0) )

        # mostramos los colliders
        #self.engine.ShowColliders( (0xF0,0x00,0x00) )

        # la escena introductoria
        self.Intro()

    # main loop
    def Run( self ):
        self.engine.Run()

    # control principal
    def CheckEscape( self ):
        # abortamos con la tecla Escape
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_ESCAPE ) ):
            self.engine.Quit()

        # mostramos los FPS
        fps = self.engine.GetFPS()
        fps = "FPS: %07.2f" % fps
        self.engine.AddText( fps, (0,682), "Monospace 20", (255,255,255) )

    #-------------------------------------------------------------------------------------------
    # escena de inicio
    def Intro( self ):
        # agregamos el fondo
        fondo = Sprite( "../images/Platform/Platform.png", (0,0) )
        self.engine.AddGObject( fondo, 0 )

        # el bloque que se mueve horizontal
        BlockHorizontal( self.engine, (13*64, 1*64), 1 )

        # agregamos el control de esta escena
        self.camRight = True
        self.engine.SetMainTask( self.IntroControl )

    def IntroControl( self, dt ):
        # movemos la camara "ppm" pixeles por minuto
        ppm = 120
        pixels = round( (ppm*dt)/1000 )

        self.CheckEscape()
        self.engine.AddText( "Presiona la Barra Espaciadora", (180,286), "Cool 30", (255,255,255) )

        x, y = self.engine.GetCamPosition()
        if( self.camRight ): x = x + pixels
        else: x = x - pixels
        self.engine.SetCamPosition( (x,y) )
        xn, yn = self.engine.GetCamPosition()
        if( xn != x ): self.camRight = not self.camRight

        if( not self.engine.IsKeyDown( LGE.CONSTANTS.K_SPACE ) ): return
        self.engine.DelAllGObjects()
        self.engine.SetMainTask()
        self.Play01()

    #-------------------------------------------------------------------------------------------
    # primera escena
    def Play01( self ):
        self.engine.SetMainTask( self.Play01Control )
        pass

    def Play01Control( self, dt ):
        pass


# -- show time
game = MiJuego()
game.Run()

from lge.Sprite import Sprite
from lge.LGE import LGE


class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (1920,1056), (640,480), "Move Player", (0xFF,0xFF,0xFF) )
        self.engine.SetFPS( 60 )
        self.engine.SetMainTask( self.MainControl )

        # cargamos un font
        self.engine.LoadSysFont( "consolas", 20 )

        # agregamos el fondo
        fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0) )
        self.engine.AddGObject( fondo, 0 )

        # agregamos un Sprite
        heroe = MiHeroe( self.engine )

        # establecemos que la camara siga al centro del heroe
        self.engine.SetCamTarget( heroe, True )

        # agregamos una música de fondo
        self.engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        self.engine.PlaySound( "fondo", loop=-1 )

    def MainControl( self, dt ):
        # abortamos con la tecla Escape
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_ESCAPE ) ):
            self.engine.Quit()

        # mostramos los FPS actuales
        fps = self.engine.GetFPS()
        fps = "FPS: %07.2f" % fps
        self.engine.AddText( fps, (0,460), "consolas" )

    # main loop
    def Run( self ):
        self.engine.Run()


class MiHeroe( Sprite ):
    def __init__( self, engine ):
        super().__init__( "../images/Swordsman/Idle/Idle_000.png", (550,346), "Heroe" )
        self.engine = engine
        self.ScalePercent( 0.16 )
        self.heading = 1
        self.engine.AddGObject( self, 1 )

    def OnUpdate( self, dt ):
        # moveremos al heroe "ppm" pixeles por minuto
        ppm = 240
        pixels = (ppm*dt)/1000

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # cambiamos sus coordenadas y orientacion segun la tecla presionada
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_RIGHT ) ):
            x = x + pixels
            if( self.heading != 1 ):
                self.Flip( True, False )
                self.heading = 1
        elif( self.engine.IsKeyPressed( LGE.CONSTANTS.K_LEFT ) ):
            x = x - pixels
            if( self.heading != -1 ):
                self.Flip( True, False )
                self.heading = -1
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_DOWN ) ):
            y = y - pixels
        elif( self.engine.IsKeyPressed( LGE.CONSTANTS.K_UP ) ):
            y = y + pixels

        # lo posicionamos asegurando que se encuentre dentro del mundo definido
        x, y = self.engine.KeepInsideWorld( self, (x,y) )
        self.SetPosition( (x,y) )


#--- show time
game = MiJuego()
game.Run()

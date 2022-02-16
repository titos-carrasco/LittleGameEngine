from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.LGE import LGE


class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (1920,1056), (640,480), "Animated Player", (0xFF,0xFF,0xFF) )
        self.engine.SetMainTask( self.MainControl )

        # activamos la musica de fondo
        LGE.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        LGE.PlaySound( "fondo", loop=-1 )

        # cargamos los recursos que usaremos
        LGE.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
        LGE.LoadImage( "idle", "../images/Swordsman/Idle/Idle_0*.png" )
        LGE.LoadImage( "run", "../images/Swordsman/Run/Run_0*.png" )
        LGE.LoadSysFont( "consolas", 20 )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        self.engine.AddGObject( fondo, 0 )

        # agregamos al heroe con sus animaciones
        heroe = MiHeroe( self.engine )
        self.engine.AddGObject( heroe, 1 )

        # establecemos que la camara siga al heroe en su origen
        self.engine.SetCamTarget( heroe, False )

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
        self.engine.Run( 60 )


class MiHeroe( Sprite ):
    def __init__( self, engine ):
        # agregamos el heroe con diferentes imagenes
        super().__init__( ["idle","run"], (550,346), "Heroe" )
        self.engine = engine
        self.Scale( 0.16 )
        self.SetShape( 0, "idle" )
        self.heading = 1

    def OnUpdate( self, dt ):
        # moveremos al heroe "ppm" pixeles por minuto
        ppm = 240
        pixels = (ppm*dt)/1000

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
        moving = False
        idx, name = self.GetCurrentShape()
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_RIGHT ) ):
            x = x + pixels
            if( self.heading != 1 ):
                self.Flip( True, False )
                self.heading = 1
            if( name != "run" ):
                self.SetShape( 0, "run" )
            moving = True
        elif( self.engine.IsKeyPressed( LGE.CONSTANTS.K_LEFT ) ):
            x = x - pixels
            if( self.heading != -1 ):
                self.Flip( True, False )
                self.heading = -1
            if( name != "run" ):
                self.SetShape( 0, "run" )
            moving = True

        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_DOWN ) ):
            y = y - pixels
            moving = True
        elif( self.engine.IsKeyPressed( LGE.CONSTANTS.K_UP ) ):
            y = y + pixels
            moving = True

        if( not moving and name != "idle" ):
                self.SetShape( 0, "idle" )

        # siguiente imagen de la secuencia
        self.NextShape( dt, 50 )

        # lo posicionamos asegurando que se encuentre dentro del mundo definido
        x, y = self.engine.KeepInsideWorld( self, (x,y) )
        self.SetPosition( (x,y) )


#--- show time
game = MiJuego()
game.Run()

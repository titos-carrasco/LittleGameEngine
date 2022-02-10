from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.LGE import LGE


class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (1920,1056), (640,480), "Animated Player", (0xFF,0xFF,0xFF) )
        self.engine.SetFPS( 60 )

        # agregamos el fondo
        fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0) )
        self.engine.AddGObject( fondo, 0 )

        # agregamos al heroe con sus animaciones
        heroe = MiHeroe( self.engine )
        self.engine.AddGObject( heroe, 1 )

        # establecemos que la camara siga al heroe en su origen
        self.engine.SetCamTarget( heroe, False )

    # main loop
    def Run( self ):
        self.engine.Run()


class MiHeroe( Sprite ):
    def __init__( self, lge ):
        # agregamos el heroe con diferentes imagenes
        fnames = {
            "idle": "../images/Swordsman/Idle/Idle_0*.png",
            "run" : "../images/Swordsman/Run/Run_0*.png"
        }
        super().__init__( fnames, (550,346), "Heroe" )
        self.engine = lge
        self.ScalePercent( 0.16 )
        self.SetShape( 0, "idle" )
        self.heading = 1
        self.elapsed = 0

    def OnUpdate( self, dt ):
        # abortamos con la tecla Escape
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_ESCAPE ) ):
            return self.engine.Quit()

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
        t = self.elapsed + dt
        if( t >= 50 ):
            self.NextShape()
            t = 0
        self.elapsed = t

        # lo posicionamos asegurando que se encuentre dentro del mundo definido
        x, y = self.engine.KeepInsideWorld( self, (x,y) )
        self.SetPosition( (x,y) )


#--- show time
game = MiJuego()
game.Run()

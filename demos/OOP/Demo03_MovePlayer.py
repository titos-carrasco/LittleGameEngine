from lge.Sprite import Sprite
from lge.LGE import LGE


class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (1920,1056), (640,480), "Move Player", (0xFF,0xFF,0xFF) )
        self.engine.SetFPS( 60 )

        # agregamos el fondo
        fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0), 0 )
        self.engine.AddGObject( fondo )

        # agregamos un Sprite
        heroe = MiHeroe( self.engine )

        # establecemos que la camara siga al heroe
        self.engine.SetCamTarget( heroe )

    # main loop
    def Run( self ):
        self.engine.Run()


class MiHeroe( Sprite ):
    def __init__( self, lge ):
        super().__init__( "../images/Swordsman/Idle/Idle_000.png", (550,346), 1, "Heroe" )
        self.engine = lge
        self.ScalePercent( 0.16 )
        self.heading = 1
        self.engine.AddGObject( self )

    def OnUpdate( self, dt ):
        # abortamos con la tecla Escape
        if( self.engine.IsKeyDown( LGE.CONSTANTS.K_ESCAPE ) ):
            return self.engine.Quit()

        # moveremos al heroe "ppm" pixeles por minuto
        ppm = 240
        pixels = (ppm*dt)/1000

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # cambiamos sus coordenadas y orientacion segun la tecla presionada
        if( self.engine.IsKeyDown( LGE.CONSTANTS.K_RIGHT ) ):
            x = x + pixels
            if( self.heading != 1 ):
                self.Flip( True, False )
                self.heading = 1
        elif( self.engine.IsKeyDown( LGE.CONSTANTS.K_LEFT ) ):
            x = x - pixels
            if( self.heading != -1 ):
                self.Flip( True, False )
                self.heading = -1
        if( self.engine.IsKeyDown( LGE.CONSTANTS.K_DOWN ) ):
            y = y - pixels
        elif( self.engine.IsKeyDown( LGE.CONSTANTS.K_UP ) ):
            y = y + pixels

        # lo posicionamos asegurando que se encuentre dentro del mundo definido
        x, y = self.engine.KeepInsideWorld( self, (x,y) )
        self.SetPosition( (x,y) )


#--- show time
game = MiJuego()
game.Run()

from lge.Sprite import Sprite
from lge.LGE import LGE


class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (800, 440), (800, 440), "The World", (0xFF, 0xFF, 0xFF) )
        self.engine.SetFPS( 60 )

        # agregamos el fondo
        fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0) )
        fondo.Scale( (800,440) )
        self.engine.AddGObject( fondo, 0 )

        # agregamos un Sprite
        heroe = Sprite( "../images/Swordsman/Idle/Idle_000.png", (220,140), "Heroe" )
        heroe.ScalePercent( 0.10 )
        self.engine.AddGObject( heroe, 1 )

        # posicionamos la camara
        self.engine.SetCamPosition( (0,0) )

    # main loop
    def Run( self ):
        self.engine.Run()


# -- show time
game = MiJuego()
game.Run()

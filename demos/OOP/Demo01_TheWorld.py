from lge.Sprite import Sprite
from lge.LGE import LGE


class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (800, 440), (800, 440), "The World", (0xFF, 0xFF, 0xFF) )

        # activamos la musica de fondo
        LGE.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        LGE.PlaySound( "fondo", loop=-1 )

        # cargamos los recursos que usaremos
        LGE.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
        LGE.LoadImage( "heroe", "../images/Swordsman/Idle/Idle_001.png" )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        fondo.Scale( (800,440) )
        self.engine.AddGObject( fondo, 0 )

        # agregamos un Sprite
        heroe = Sprite( "heroe", (220,140), "Heroe" )
        heroe.Scale( 0.1 )
        self.engine.AddGObject( heroe, 1 )

        # posicionamos la camara
        self.engine.SetCamPosition( (0,0) )

    # main loop
    def Run( self ):
        self.engine.Run( 60 )


# -- show time
game = MiJuego()
game.Run()

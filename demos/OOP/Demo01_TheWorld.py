from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Rect import Rect


class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (800, 440), "The World" )

        # activamos la musica de fondo
        Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        Engine.PlaySound( "fondo", loop=-1 )

        # cargamos los recursos que usaremos
        Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
        Engine.LoadImage( "heroe", "../images/Swordsman/Idle/Idle_00*.png" )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0), "fondo" )
        fondo.ReSize( (800,440) )
        Engine.AddGObject( fondo, 0 )

        # agregamos un Sprite
        heroe = Sprite( "heroe", (226,142), "Heroe" )
        heroe.Scale( 0.08 )
        Engine.AddGObject( heroe, 1 )

        # python un poco mas avanzado
        heroe.OnUpdate = lambda dt: heroe.NextShape(dt,60)

    # main loop
    def Run( self ):
        Engine.Run( 60 )


# -- show time
game = MiJuego()
game.Run()

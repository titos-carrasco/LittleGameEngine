from lge.Engine import Engine
from lge.Sprite import Sprite


# creamos el juego
Engine.Init( (800,440), "The World" )

# activamos la musica de fondo
Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
Engine.PlaySound( "fondo", loop=-1 )

# cargamos los recursos que usaremos
Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png", (800,440) )
Engine.LoadImage( "heroe", "../images/Swordsman/Idle/Idle_00*.png", 0.08 )

# agregamos el fondo
fondo = Sprite( "fondo", (0,0) )
Engine.AddGObject( fondo, 0 )

# agregamos un Sprite
heroe = Sprite( "heroe", (226,142), "Heroe" )
Engine.AddGObject( heroe, 1 )

# python un poco mas avanzado
heroe.OnUpdate = lambda dt: heroe.NextShape(dt,60)

# main loop
Engine.Run( 60 )

from lge.Sprite import Sprite
from lge.Engine import Engine

# creamos el juego
Engine.Init( (800,440), (800,440), "The World", (0xFF,0xFF,0xFF) )

# activamos la musica de fondo
Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
Engine.PlaySound( "fondo", loop=-1 )

# cargamos los recursos que usaremos
Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
Engine.LoadImage( "heroe", "../images/Swordsman/Idle/Idle_000.png" )

# agregamos el fondo
fondo = Sprite( "fondo", (0,0) )
fondo.Scale( (800,440) )
Engine.AddGObject( fondo, 0 )

# agregamos un Sprite
heroe = Sprite( "heroe", (220,140), "Heroe" )
heroe.Scale( 0.1 )
Engine.AddGObject( heroe, 1 )

# posicionamos la camara
Engine.SetCamPosition( (0,0) )

# main loop
Engine.Run( 60 )

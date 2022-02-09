from lge.Sprite import Sprite
from lge.LGE import LGE

# creamos el juego
engine = LGE( (800,440), (800,440), "The World", (0xFF,0xFF,0xFF) )
engine.SetFPS( 60 )

# agregamos el fondo
fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0), 0 )
fondo.Scale( (800,440) )
engine.AddGObject( fondo )

# agregamos un Sprite
heroe = Sprite( "../images/Swordsman/Idle/Idle_000.png", (220,140), 1, "Heroe" )
heroe.ScalePercent( 0.10 )
engine.AddGObject( heroe )

# posicionamos la camara
engine.SetCamPosition( (0,0) )

# main loop
engine.Run()

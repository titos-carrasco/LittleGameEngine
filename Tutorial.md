# Tutorial

```python
from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Canvas import Canvas

# creamos el juego
Engine.Init( (800,440), "The World" )

# activamos la musica de fondo
Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
Engine.PlaySound( "fondo", loop=-1 )

# cargamos los recursos que usaremos
Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png", (800,440) )
Engine.LoadImage( "heroe", "../images/Swordsman/Idle/Idle_00*.png", 0.08 )
Engine.LoadTTFFont( "backlash", 40, "../fonts/backlash.ttf" )

# agregamos el fondo
fondo = Sprite( "fondo", (0,0) )
Engine.AddGObject( fondo, 0 )

# agregamos un Sprite
heroe = Sprite( "heroe", (226,142), "Heroe" )
Engine.AddGObject( heroe, 1 )

# agregamos un texto con transparencia
canvas = Canvas( (200,110), (400,200) )
canvas.Fill( (0,0,0,40) )
canvas.DrawText( "Little Game Engine", (40,70), "backlash", (30,30,30) )
Engine.AddGObject( canvas, Engine.CAM_LAYER )

# python un poco mas avanzado
heroe.OnUpdate = lambda dt: heroe.NextShape(dt,0.060)

# main loop
Engine.Run( 60 )
```

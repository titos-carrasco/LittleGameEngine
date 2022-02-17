# LittleGameEngine
Un pequeño motor de juegos para aprender a programar con Python

![](images/world.png)

```python
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
```

![](images/collisions.png)
![](images/Betty.png)
![](images/Plataforma.png)


---
## Clases
```python
# imports
from lge.Rect import Rect
from lge.GameObject import GameObject
fron lge.Text import Text
from lge.Sprite import Sprite
from lge.Engine import Engine


# --- Engine.py
Engine.Init( worldDim, winDim, title, bgColor )

# world
Engine.GetWorldSize() -> width, height
Engine.KeepInsideWorld( gobj, (x,y) ) -> x, y

# camera
Engine.SetCamPosition( (x,y)) )
Engine.GetCamPosition() -> x, y
Engine.GetCamSize() -> width, height
Engine.SetCamTarget( gobj=None, center=True )

# gobjects
Engine.AddGObject( gobj, layer )
Engine.DelGObject( name )
Engine.GetGObject( name ) -> gobj or [gobj, gobj, ...]
Engine.ShowColliders( color=None )
Engine.GetCollisions( name ) -> [ (gobj,crop), (gobj,crop), ...]

# events
Engine.IsKeyDown( key ) -> bool
Engine.IsKeyUp( key ) -> bool
Engine.IsKeyPressed( key ) -> bool
Engine.GetMousePos() -> x, y
Engine.GetMousePressed() -> [ b1, b2, b3, ... ]

# game
Engine.SetMainTask( task=None )
Engine.GetFPS() -> fps
Engine.Quit()
Engine.Run( fps )

# fonts
Engine.GetSysFonts() -> [ name, name, name, ... ]
Engine.LoadSysFont( name, size )
Engine.LoadTTFFont( name, size, path )

# sonidos
Engine.LoadSound( name, fname )
Engine.PlaySound( name, loop=0 )
Engine.StopSound( name )
Engine.SetSoundVolume( name, volume )
Engine.GetSoundVolume( name ) -> volume

# imágenes
Engine.LoadImage( iname, pattern )
Engine.GetImages( iname ) -> [ surface, surface, ... ]


# --- Sprite.py
Sprite( inames, position, name=None ) -> gobj
gobj.GetCurrentShape() -> idx, iname
gobj.NextShape( dt, millis=0 )
gobj.SetShape( idx, iname )
gobj.Setsize( size )
gobj.Scale( size )
gobj.Flip( fx, fy )


# --- Text.py
Text( text, position, fontName, fgColor, bgColor, name=None ) -> gobj
gobj.SetText( text )


# --- GameObject.py
GameObject( (left,bottom), (width,height), name=None ) -> gobj
gobj.GetPosition() -> left, bottom
gobj.GetSize() -> width, height
gobj.GetName() -> name
gobj.GetTag() -> tag
gobj.IsVisible() -> bool
gobj.SetPosition( (left,bottom) )
gobj.SetSize( (width,height) )
gobj.SetVisible( visibility )
gobj.CollideGObject( gobj ) -> x, y, width, height (or None)
gobj.CollideRect( rect ) -> x, y, width, height (or None)
gobj.CollidePoint( (x,y) ) -> bool

# --- Rect.py
Rect( (x,y), (width,height) ) -> rect
rect.GetOrigin() -> x, y
rect.GetSize() -> width, height
rect.SetOrigin( (x,y) )
rect.SetSize( (width,height) )
rect.CollideRect( rect ) -> x, y, width, height (or None)
rect.CollidePoint( (x,y) ) -> bool

```

---
## Pendientes
- Luces


---
## Imágenes
- https://opengameart.org/content/one-more-lpc-alternate-character
- https://opengameart.org/content/free-platformer-game-tileset
- https://opengameart.org/content/2d-game-character-pack-slim-version
- https://opengameart.org/content/game-character-blue-flappy-bird-sprite-sheets
- https://opengameart.org/content/dungeon-crawl-32x32-tiles
- https://www.kenney.nl
- https://opengameart.org/content/2d-platformer-volcano-pack-11

## Sonidos
- https://freesound.org/people/TiagoThanos/sounds/571229/
- https://freesound.org/people/MATRIXXX_/sounds/365668/

## Fonts
- backlash.ttf - Backlash BRK - No contiene información de licencia
- FreeMono.ttf - FreeMono - Parte de los FreeFont de GNU - GNU General Public License
- LiberationMonoRegular.ttf - Liberation Mono - Liberation Fonts License

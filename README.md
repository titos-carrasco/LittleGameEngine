# LittleGameEngine
Un pequeño motor de juegos para incursionar en Python

![](images/world.png)

```python
from lge.Sprite import Sprite
from lge.LGE import LGE

# creamos el juego
engine = LGE( (800,440), (800,440), "The World", (0xFF,0xFF,0xFF) )
engine.SetFPS( 60 )

# agregamos el fondo
fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0) )
fondo.Scale( (800,440) )
engine.AddGObject( fondo, 0 )

# agregamos un Sprite
heroe = Sprite( "../images/Swordsman/Idle/Idle_000.png", (220,140), "Heroe" )
heroe.ScalePercent( 0.10 )
engine.AddGObject( heroe, 1 )

# posicionamos la camara
engine.SetCamPosition( (0,0) )

# main loop
engine.Run()
```

![](images/collisions.png)


---
## Clases
```python
game = LGE( worldDim, winDim, title, bgColor )

# world
width, height = game.GetWorldSize()
game.KeepInsideWorld( gobj, newpos )

# camera
game.SetCamPosition( position )
x, y = game.GetCamPosition()
width, height = game.GetCamSize()
game.SetCamTarget( target=None )
game.UnSetCamTarget()
game.AddText( text, position, color=(0,0,0) )

# game
game.SetMainTask( task=None )
game.SetFPS( fps )
game.Quit()
game.Run()

# gobjects
game.AddGObject( gobj, layer )
game.DelGobject( gobj )
game.DelGobjectByName( name )
gobj = game.GetGObject( name )
game.ShowColliders( bc=None )
arr = game.GetCollisions( name )        # [ (gobj,crop), (gobj,crop), ...]

# events
b = game.IsKeyUp( key )
b = game.IsKeyDown( key )
b = game.IsKeyPressed( key )

# sprites
gobj = Sprite( fspecs, (left,bottom), name=None )
idx, key = gobj.GetCurrentShape()
gobj.NextShape()
gobj.SetShape( idx, entry="__no_id__" )
gobj.SetSize( (width,height) )
gobj.Scale( (width,height) )
gobj.ScalePercent( percent )
gobj.Flip( flipX, flipY )

# objects
gobj = GameObject( (left,bottom), (width,height), name=None )
left, bottom = gobj.GetPosition()
width, height = gobj.GetSize()
name = gobj.GetName()
visibility = gobj.IsVisible()
gobj.SetPosition( (left,bottom) )
gobj.SetSize( (width,height) )
gobj.SetVisible( visibility )
crop = gobj.CollideRect( rect )
if( crop is not None): x, y, width, height = crop

# rect
r = Rect( (x,y), (width,height) )
x, y = r.GetOrigin()
width, height = r.GetSize()
r.SetOrigin( (x,y) )
r.SetSize( (width,height) )
crop = r.CollideRect( rect )
if( crop is not None): x, y, width, height = crop

```

---
## Imágenes

Las imágenes de los demos fueron obtenidas desde
- https//opengameart.org/content/one-more-lpc-alternate-character
- https//opengameart.org/content/free-platformer-game-tileset
- https//opengameart.org/content/2d-game-character-pack-slim-version
- https//opengameart.org/content/game-character-blue-flappy-bird-sprite-sheets
- https//opengameart.org/content/dungeon-crawl-32x32-tiles

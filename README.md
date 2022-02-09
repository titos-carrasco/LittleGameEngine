# LittleGameEngine
Un pequeño motor de juegos para incursionar en Python

![](images/world.png)
![](images/collisions.png)


---
## Clases
```python
r = Rect( origin=(0,0), size=(0,0) )
x, y = r.GetOrigin()
width, height = r.GetSize()
r.SetOrigin( origin )
r.SetSize( size )
crop = r.CollideRect( rect )
if( crop is not None): x, y, width, height = crop


gobj = GameObject( xy, size, layer, name=None )
x, y = gobj.GetPosition()
width, height = gobj.GetSize()
visibility = gobj.IsVisible()
layernum = gobj.GetLayer()
name = gobj.GetName()
gobj.SetPosition( xy )
gobj.SetSize( size )
gobj.SetVisible( visible )
gobj.DeleteMe()
crop = gobj.CollideRect( rect )
if( crop is not None): x, y, width, height = crop


gobj = Sprite( specification, position, layer, name=None )
idx, key = gobj.GetCurrentShape()
gobj.idx, key = NextShape()
gobj.SetShape( idx, entry="__no_id__" )
gobj.SetSize( size )
gobj.Scale( size )
gobj.ScalePercent( percent )
gobj.Flip( flipX, flipY )


game = LGE( worldDim, winDim, title, bgColor, task=None )
width, height = game.GetWorldSize()
x, y = game.GetCamPosition()
width, height = game.GetCamSize()
gobj = game.GetGObject( name )
b = game.IsKeyUp( key )
b = game.IsKeyDown( key )
arr = game.GetCollisions( gobj )        # [ (gobj,crop), (gobj,crop), ...]
game.SetFPS( fps )
game.SetCamPosition( position )
game.SetCamTarget( target=None )
game.AddGObject( gobj )
game.AddText( text, position, color=(0,0,0) )
game.KeepInsideWorld( gobj, newpos )
game.ShowColliders( bc=None )
game.Quit()
game.Run()
```

---
## Imágenes

Las imágenes de los demos fueron obtenidas desde
- https//opengameart.org/content/one-more-lpc-alternate-character
- https//opengameart.org/content/free-platformer-game-tileset
- https//opengameart.org/content/2d-game-character-pack-slim-version
- https//opengameart.org/content/game-character-blue-flappy-bird-sprite-sheets
- https//opengameart.org/content/dungeon-crawl-32x32-tiles

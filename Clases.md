# Clases

Todas las coordenadas están en el **Sistema Cartesiano**

```Python
from lge.Engine import Engine
from lge.Camera import Camera
from lge.Sprite import Sprite
from lge.Text import Text
from lge.GameObject import GameObject
from lge.Rect import rect
```

## Engine

```
Engine.CONSTANTS
Engine.VLIMIT
Engine.GUI_LAYER
```

---
```
Init( camSize, title, bgColor=(0,0,0) )
```

---
```
Run( fps )
```

---
```
Quit()
```

---
```
SetOnUpdate( func=None )
```

---
```
GetFPS()
```

---
```
GetRequestedFPS()
```

#### Game Objects
```
AddGObject( gobj, layer )
```

---
```
AddGObjectGUI( gobj )
```

---
```
GetGObject( name )
```

---
```
DelGObject( gobj )
```

---
```
DelGObjectByName( name )
```

---
```
ShowColliders( color=None )
```

---
```
GetCollisions( gobj )
```


#### Camara
```
GetCamera()
```

---
```
SetCameraTarget( gobj=None, center=False )
```


#### Eventos
```
KeyDown( key )
```

---
```
KeyUp( key )
```

---
```
IsKeyPressed( key )
```

---
```
GetMousePosition()
```

---
```
GetMouseButtons()
```

---
```
GetMousePressed( button )
```

---
```
GetMouseReleased( button )
```

---

#### Fonts
```
GetSysFonts()
```

---
```
LoadSysFont( name, size )
```

---
```
LoadTTFFont( name, size, path )
```

### Sonidos
```
LoadSound( name, fname )
```

---
```
PlaySound( name, loop=0 )
```

---
```
StopSound( name )
```

---
```
SetSoundVolume( name, volume )
```

---
```
GetSoundVolume( name )
```

#### Imágenes
```
LoadImage( iname, pattern, scale=None, flip=None )
```

---
```
GetImages( iname )
```


### Camera
Clase para mostrar la zona visible de la superficie del juego

---
```
camera = Camera( position, size )
```

---
```
rect = camera.GetRectangle()
```

---
```
x, y = camera.GetPosition()
```

---
```
w, h = camera.GetSize()
```

---
```
rect = camera.GetBounds()
```

---
```
camera.SetPosition( x, y )
```

---
```
camera.SetBounds( rect )
```


## Sprites
GameObject para operar con imágenes

---
```
sprite = Sprite( inames, position, name=None )
```
Crea un GameObject de tipo Sprite en la posición dada y con el nombre especificado. El parámetro `inames` puede ser un `string` o una `lista de strings` con los nombres de las listas imágenes previamente cargadas con **Engine.LoadImage**

| Parámetros | Descripción
|---|---
|`inames`| El o los nombres de las imágenes a utilizar por este Sprite
|`position`| Las coordenadas (x,y) de la posición del GameObject
|`name`| El nombre único a asignar al GameObject

| Retorno | Descripción
|---|---
|`sprite`| El GameObject creado

---
```
idx, iname = sprite.GetCurrentShape()
```
Retorna cual es la imagen actual utilizada en el sprite

| Retorno | Descripción
|---|---
|`idx`| El número de la imagen actual dentro de `iname`
|`iname`| El nombre de la imagen actual

---
```
sprite.NextShape( dt, segs=0.0 )

```
Cambia a la siguiente imagen si es que han transcurrido los milisegundos especificados

| Parámetros | Descripción
|---|---
|`dt`| Tiempo transcurrido desde el último cuadro del juego
|`segs`| segundos que deben transcurrir para que se pase a la siguiente imagen

---
```
sprite.SetShape( idx, iname )
```
Establece la imagen del sprite

| Parámetros | Descripción
|---|---
|`idx`| El número de la imagen dentro de la lista `iname`
|`iname`| MEl nombre de la lista de imágenes


## Canvas
Una pizarra para dibujar

---
```
canvas = Canvas( position, size, name=None )
```
Crea un GameObject de tipo canvas en la posición y tamano dados.

| Parámetros | Descripción
|---|---
|`position`| Las coordenadas (x,y) de la posición del GameObject
|`size`| eñ tamano del gameobject
|`name`| El nombre único a asignar al GameObject

---
```
canvas.Fill( bgColor )
```

---
```
canvas.DrawText( text, position, fontName, color ):
```

---
```
canvas.DrawPoint( point, color )
```

---
```
canvas.DrawCircle( center, radius, color, thickness=False )
```

---
```
canvas.DrawRectangle( position, size, color, thickness=False  )
```

---
```
canvas.DrawImage( position, image_id )
```


## GameObject
Clase base de **Little Game Engine** (todo es un **GameObject**)

---
```
gobj = GameObject( position, size, name=None )
```
Crea un GameObject en la posición y dimensiones especificadas

| Parámetros | Descripción
|---|---
|`position`| Las coordenadas (x,y) de la posición del GameObject
|`size`| La dimensión (width,height) del GameObject
|`name`| El nombré único a asignar al GameObject

| Retorno | Descripción
|---|---
|`gobj`| El GameObject creado

---
```
rect = gobj.GetRectangle()
```

---
```
x, y = gobj.GetPosition()
```
Retorna la posición del GameObject

| Retorno | Descripción
|---|---
|`x, y`| La posición (x,y) del GameObject

---
```
w, h = gobj.GetSize()
```
Retorna la dimensión del GameObject

| Retorno | Descripción
|---|---
|`w, h`| La dimensión (width, height) del rGameObject

---
```
name = gobj.GetName()
```
Retorna el nombre del GameObject

| Retorno | Descripción
|---|---
|`name`| El nombre del GameObject

---
```
tag = gobj.GetTag()
```
Retorna el tag del GameObject

| Retorno | Descripción
|---|---
|`tag`| El tag del GameObject

---
```
gobj.SetPosition( x, y, rect=None )
```
Establece la posición del GameObject

| Parámetros | Descripción
|---|---
|`x, y`| La nueva posición (x,y) del GameObject
|`rect`| Si se específica, la posición del GameObject queda confiada al rectángulo dado

---
```
gobj.SetSize( w, h )
```
Establece la dimensión del GameObject

| Parámetros | Descripción
|---|---
|`w, h`| La nueva dimensión (width,height)  del GameObject

---
```
gobj.SetTag( tag )
```
Establece un tag para el GameObject

| Parámetros | Descripción
|---|---
|`tag`| El tag para el GameObject

---
```
gobj.SetColliders( enabled=True )
```


## Rectángulo
Clase de apoyo utilizada en todo **Little Game Engine**

---
```
rect = Rectangle( origen, size )
```
Crea un rectángulo en el origen y dimensiones especificadas

| Parámetros | Descripción
|---|---
|`origen`| Las Coordenadas (x,y) del origen del rectángulo
|`size`| La dimensión (width,height) del rectángulo

| Retorno | Descripción
|---|---
|`rect`| El rectángulo creado

---
```
rect2 = rect.Copy()
```
Crea una copia del rectángulo

| Retorno | Descripción
|---|---
|`rect`| La copia del rectángulo

---
```
x1, y1, x2, y2 = rect.Getpoints()
```
Retorna el origen del rectángulo

| Retorno | Descripción
|---|---
|`x1, y1, x2, y2 `| Las coordenadas del rectángulo

---
```
w, h = rect.GetSize()
```
Retorna la dimensión del rectángulo

| Retorno | Descripción
|---|---
|`w, h`| La dimensión (width, height) del rectángulo

---
```
rect.SetOrigin( x, y ) )
```
Establece las coordenadas de origen del rectángulo

| Parámetros | Descripción
|---|---
|`x, y`| Las nuevas coordenadas (x,y) del origen del rectángulo

---
```
rect.SetSize( w, h )
```
Establece la dimensión del rectángulo

| Parámetros | Descripción
|---|---
|`w, h`| La nueva dimensión (width, height) del rectángulo

---
```
rect.KeepInsideRectangle( rect2 )
```
Ajusta el origen tal que el rectángulo queda dentro del rectángulo dado

| Parámetros | Descripción
|---|---
|`rect2`| El rectángulo a utilizar como límites

---
```
b = rect.CollidePoint( px, py )
```
Determina si un punto intersecta al rectángulo

| Parámetros | Descripción
|---|---
|`px, py`| Las coordenadas (x,y) del punto a verificar

| Retorno | Descripción
|---|---
|`b`| `True` si es que el punto intersecta al rectángulo, `False` en caso contrario

---
```
b = rect.CollideRectangle( rect2 )
```
Determina si un rectángulo intersecta a este rectángulo

| Parámetros | Descripción
|---|---
|`rect2`| El rectángulo a evaluar

| Retorno | Descripción
|---|---
|`b`| `True` si es que el rectángulo intersecta al otro rectángulo, `False` en caso contrario

---
```
rect3 = rect.GetCollideRectangle( rect2 )
```
Determina el rectángulo de intersección con el rectángulo dado

| Parámetros | Descripción
|---|---
|`rect2`| El rectángulo a evaluar

| Retorno | Descripción
|---|---
|`rect3`| `Rectangle` de intersección, `None` en caso contrario

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
Engine.CAM_LAYER
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
SetUpdate( func=None )
```

---
```
GetFPS()
```

#### Camara
```
GetCamera()
```

---
```
SetCameraTarget( gobj=None, center=True )
```

#### Game Objects
```
AddGObject( gobj, layer )
```

---
```
DelGObject( name )
```

---
```
GetGObject( name )
```

---
```
ShowColliders( color=None )
```

---
```
GetCollisions( name )
```

#### Eventos
```
IsKeyDown( key )
```

---
```
IsKeyUp( key )
```

---
```
IsKeyPressed( key )
```

---
```
GetMousePos()
```

---
```
GetMousePressed()
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
LoadImage( iname, pattern )
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
position = camera.GetPosition()
```

---
```
size = camera.GetSize()
```

---
```
camera.SetBounds( bounds )
```

---
```
bounds = camera.GetBounds()
```

---
```
camera.SetPosition( position )
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
sprite.NextShape( dt, millis=0 )

```
Cambia a la siguiente imagen si es que han transcurrido los milisegundos especificados

| Parámetros | Descripción
|---|---
|`dt`| Tiempo transcurrido desde el último cuadro del juego
|`millis`| Milisegundos que deben transcurrir para que se pase a la siguiente imagen

---
```
sprite.SetShape( idx, iname )
```
Establece la imagen del sprite

| Parámetros | Descripción
|---|---
|`idx`| El número de la imagen dentro de la lista `iname`
|`iname`| MEl nombre de la lista de imágenes

---
```
sprite.ReSize( size )
```
Cambia el tamaño de la imagen del sprite

| Parámetros | Descripción
|---|---
|`size`| Nuevo tamaño (width,height)

---
```
sprite.Scale( factor )
```
Cambia el tamaño de la imagen del sprite

| Parámetros | Descripción
|---|---
|`factor`| El factor de escala a utilizar para escalar la imagen

---
```
sprite.Flip( fx, fy )
```
Invierte la imagen en horizontal y/o vertical

| Parámetros | Descripción
|---|---
|`fx`| `True` si se debe invertir en el eje X
|`fx`| `True` si se debe invertir en el eje Y


## Textos
GameObject para operar con textos

---
```
textGObj= Text( text, position, fontName, fgColor, bgColor=None, name=None )
```
Crea un GameObject de tipo Text en la posición y nombre de la fuente, color y color de fondo dados.

| Parámetros | Descripción
|---|---
|`text`| El texto para este GameObject
|`position`| Las coordenadas (x,y) de la posición del GameObject
|`fontName`| El nombre de la fuente a utilizar (cargada previamente)
|`fgColor`| El color del texto
|`bgColor`| El color de fondo a utilizar. Para fondo transparente utiliza `None`
|`name`| El nombre único a asignar al GameObject

| Retorno | Descripción
|---|---
|`textGObj`| El GameObject creado

---
```
textGObj.SetText( text )
```
Establece el texto de este GameObject

| Parámetros | Descripción
|---|---
|`text`| El nuevo texto para este GameObject


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
position = gobj.GetPosition()
```
Retorna la posición del GameObject

| Retorno | Descripción
|---|---
|`position`| La posición (x,y) del GameObject

---
```
size = gobj.GetSize()
```
Retorna la dimensión del GameObject

| Retorno | Descripción
|---|---
|`size`| La dimensión (width, height) del rGameObject

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
visible = gobj.IsVisible()
```
Retorna la visibilidad del GameObject

| Retorno | Descripción
|---|---
|`Visible`| `True` si es que el GameObject es visible, `False` en caso contrario

---
```
gobj.SetPosition( position, rect=None )
```
Establece la posición del GameObject

| Parámetros | Descripción
|---|---
|`position`| La nueva posición (x,y) del GameObject
|`rect`| Si se específica, la posición del GameObject queda confiada al rectpangulo dado

---
```
gobj.SetSize( size )
```
Establece la dimensión del GameObject

| Parámetros | Descripción
|---|---
|`size`| La nueva dimensión (width,height)  del GameObject

---
```
gobj.SetVisible( visibility )
```
Establece la visibilidad del GameObject

| Parámetros | Descripción
|---|---
|`visibility`| `True` para especificar que el GameObject es visible, `False` en caso contrario

---
```
rect = gobj.CollideGObject( gobj2 )
```
Verifica si el GameObject intersecta con otro

| Parámetros | Descripción
|---|---
|`gobj2`| El GameObject contra el cual verificar

| Retorno | Descripción
|---|---
|`rect`| Un rectángulo dado por la intersección de ambos GameObjects. `None` en caso de que no intersecten

---
```
rect = gobj.CollideRect( rect )
```
Verifica si el GameObject intersecta con el rectángulo dado

| Parámetros | Descripción
|---|---
|`rect`| El rectángulo contra el cual verificar

| Retorno | Descripción
|---|---
|`rect`| Un rectángulo dado por la intersección con el rectángulo. `None` en caso de que no intersecten

---
```
collide = gobj.CollidePoint( point )
```
Determina si un punto intersecta al GameObject

| Parámetros | Descripción
|---|---
|`point`| Las coordenadas (x,y) del punto a verificar

| Retorno | Descripción
|---|---
|`collide`| `True` si es que el punto intersecta al GameObject, `False` en caso contrario


## Rectángulo
Clase de apoyo utilizada en todo **Little Game Engine**

---
```
rect = Rect( origen, size )
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
origen = rect.GetOrigin()
```
Retorna el origen del rectángulo

| Retorno | Descripción
|---|---
|`origen`| El origen (x,y) del rectángulo

---
```
size = rect.GetSize()
```
Retorna la dimensión del rectángulo

| Retorno | Descripción
|---|---
|`size`| La dimensión (width, height) del rectángulo

---
```
rect.SetOrigin( origen ) )
```
Establece las coordenadas de origen del rectángulo

| Parámetros | Descripción
|---|---
|`origen`| Las nuevas coordenadas (x,y) del origen del rectángulo

---
```
rect.SetSize( size )
```
Establece la dimensión del rectángulo

| Parámetros | Descripción
|---|---
|`size`| La nueva dimensión (width, height) del rectángulo

---
```
collide = rect.CollidePoint( point )
```
Determina si un punto intersecta al rectángulo

| Parámetros | Descripción
|---|---
|`point`| Las coordenadas (x,y) del punto a verificar

| Retorno | Descripción
|---|---
|`collide`| `True` si es que el punto intersecta al rectángulo, `False` en caso contrario

---
```
rect3 = rect.CollideRect( rect2 )
```
Determina si un rectángulo intersecta a este rectángulo

| Parámetros | Descripción
|---|---
|`rect2`| El rectángulo a evaluar

| Retorno | Descripción
|---|---
|`rect3`| Un rectángulo dado por la intersección de ambos rectángulos. `None` en caso de que no intersecten

---
```
point = rect.KeepInsideRect( rect2 )
```
Retorna un origen ah¿justado tal que el rectángulo queda dentro del rectángulo dado

| Parámetros | Descripción
|---|---
|`rect2`| El rectángulo a utilizar como límites

| Retorno | Descripción
|---|---
|`point`| Origen (x,y) ajustados

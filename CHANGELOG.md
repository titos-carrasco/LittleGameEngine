# ChangeLog

## @v0.1.0 2022-02-19
- lge/Engine.py
    - Modifica LoadImage() para realizar transformaciones en la carga
    - Optimizacioens varias
-lge/Sprite.py
    - Elimina métodos SetSize(), Scale() y Flip()
- demos/
    Ajusta todos los demos acorde a los cambios

## 2022-02-18
- lge/Rect.py
    - Agrega métodos Copy() y KeepInsideRect()
-lge/GameObject.py
    - Modifica método SetPosition() agregando parámetro del tipo Rect() a
      utilizar como límites para las coordenadas dadas
- lge/Engine.py
    - Elimina parámetro worldSize del método Initi()
    - Agrega métodos SetWorldBounds(), GetWorldBounds() y ResetWorldBounds()
    - elimina método KeepInsideWorld()
    - Mueve operaciones de la camara a nueva clase
- demos/
    Ajusta todos los demos acorde a los cambios

## @v0.1.0-pre.1 2022-02-17
- Agrega Tutorial (Tutorial.md)
- Agrega descripción de Clases (Clases.md)
- lge/Rect.py
    - CollideRect() retorna un rectángulo
- lge/Sprite.py
    - Método Scale() solo requiere del factor de escala
    - Método SetSize() no hace nada
    - Agrega método ReSize()
- lge/Engine.py
    - Ajustes internos
- demos/
    - Ajustes menores

## @v0.0.8 2022-02-16
- lge/LGE.py
    - **Cambia de nombre a Engine.py**
- lge/Engine.py
    - Todos los métodos son estáticos
    - Los GameObjects en la capa CAM_LAYER aparecen en la Camara
    - DelGObject puede recibir un patrón de eliminación
    - GetGObject puede recibir un patrón de búsqueda
    - Se agregan métodos para el mouse
- lge/Rect.py
    - Se agrega método CollidePoint
- lge/GameObject.py
    - Se agrega método CollidePoint()
    - Se agrega método CollideGObject()
- lge/Text.py
    - Agrega GameObject del tipo Texto
- demos/fonts
    - Se agrega FreeMono.ttf
- demos/
    - Se ajustan todos los demos acorde a los cambios realizados

## @v0.0.7 2022-02-15
- lge/LGE.py
    - Fonts, sonidos e imágenes se manejan a nivel de la clase
    - Se agregan los métodos para cargar imagenes
- lge/Rect.py:
    - Agrega método CollidePoint()
- lge/GameObject.py:
    - Agrega método CollidePoint()
- lge/Sprite.py
    - Se actualiza acorde a los cambios relizados
- demos/
    - Se actualizan acorde a los cambios relizados
    - FPS ahora es parámetro de Run()

## 2022-02-13
- lge/LGE.py
    - Agrega manejo de sonidos
    - Cambia de nombre método GetGObject() a GetGObjectByName()
    - Elimina método UnSetCamTarge()
    - Elimina método DelGObject()
- lge/Sprite.py
    - Modifica NextShape() para especificar tiempo en el cambio de shape
- demos/
    - Agrega sonido en algunos demos

## @v0.0.6 2022-02-12
- lge/LGE.py
    - Corrige métodos para agregar y eliminar objetos
    - Agrega uso de fonts TTF
- lge/GameObject.py
    - Atributo TAG (tipo str) en GameObject para usarlo como un tipo de objeto ("suelo", "zombie", "veneno", etc)
- demos/Betty
    - Agrega Demo básico al estilo PacMan

## 2022-02-10
- lge/LGE.py
    - Agrega método SetMainTask()
    - Agrega método DelGObject()
    - Agrega método DelGObjectByName()
- lge/Rect.py
    - Se eliminan valores por defecto en el constructor
    - Corrige uso de 'raise'
    - Se elimina en el constructor el parámetro 'task'
    - Se modifica SetCamPosition para trabajar con el centro de a cámara
    - Modifica métodos ára agregar/eliminar gobjects
- lge/GameObject.py
    - Elimina parámetro 'layer'
    - Elimina método DeteleMe()
    - Corrige uso de 'raise'
- lge/Sprite.py
    - Elimina parámetro 'layer'
- demos/
    - Ajusta demos acorde a cambios realizados

## @v0.0.5 2022-02-09
- Agrega límite al "mundo"
- Agrega uso de Layers
- Agrega GameObject()
- Agrega Cámara (viewport)
- Agrega Sprites
- Agrega Colisiones

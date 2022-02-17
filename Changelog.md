# ChangeLog

## 2022-02-16

### Changed
- lge/LGE.py
    - **Cambia de nombre a Engine.py**
    - Todos los métodos son estáticos
    - DelGObject puede recibir un patrón de eliminación
    - GetGObject puede recibir un patrón de búsqueda
    - Se agregan métodos para el mouse
- lge/Rect.py
    - Se agrega método CollidePoint
- lge/GameObject.py
    - Se agrega método CollidePoint()
    - Se agrega método CollideGObject()
- lge/demos
    - se ajustan todos los demos acorde a los cambios realizados

### Added
- lge/Text.py
    - GameObject del tipo Texto
- demos/fonts
    - Se agrega FreeMono.ttf


## 2022-02-15

### Changed
- lge/LGE.py
    - Fonts, sonidos e imágenes se manejan a nivel de la clase
    - Se agregan los métodos para cargar imagenes

- lge/Sprite.py
    - Se actualiza acorde a los cambios relizados
- lge/demos
    - Se actualizan acorde a los cambios relizados
    - FPS ahora es parámetro de Run()

### Added
- lge/Rect.py:
    - Agrega método CollidePoint()
- lge/GameObject.py:
    - Agrega método CollidePoint()


## 2022-02-13

### Added
- lge/LGE.py
    - Agrega manejo de sonidos
- demos/
    - Agrega sonido en algunos demos

### Changed
- lge/LGE.py
    - Agrega manejo de sonidos
    - Cambia de nombre método GetGObject() a GetGObjectByName()
    - Finaliza demo Betty (queda como desafio agregar sonidos, puntos, etc)
- lge/Sprite.py
    - Modifica NextShape() para especificar tiempo en el cambio de shape

### Deleted
- lge/LGE.py
    - Elimina método UnSetCamTarge()
    - Elimina método DelGObject()

## @v0.0.6 2022-02-12

### Changed
- lge/LGE.py
    - Corrige métodos para agregar y eliminar objetos

### Added
- lge/LGE.py
    - Uso de fonts TTF
- lge/GameObject.py
    - Atributo TAG (tipo str) en GameObject para usarlo como un tipo de objeto ("suelo", "zombie", "veneno", etc)
- demos/Betty
    - Demo básico al estilo PacMan

## 2022-02-10

### Changed
- lge/Rect.py
    - Se eliminan valores por defecto en el constructor
    - Corrige uso de 'raise'

- lge/GameObject.py
    - Elimina parámetro 'layer'
    - Elimina método DeteleMe()
    - Corrige uso de 'raise'

- lge/Sprite.py
    - Elimina parámetro 'layer'

- lge/LGE.py
    - Se elimina en el constructor el parámetro 'task'
    - Se modifica SetCamPosition para trabajar con el centro de a cámara
    - Modifica métodos ára agregar/eliminar gobjects

- demos/*.py
    - Ajusta deos acorde a cambios en lge

### Added
- lge/LGE.py
    - Agrega método SetMainTask()
    - Agrega método DelGObject()
    - Agrega método DelGObjectByName()

## @v0.0.5 2022-02-09

### Added
- World
- Layers
- GameObject
- Camera
- Sprites
- Colisiones

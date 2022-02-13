# ChangeLog

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

# ChangeLog

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

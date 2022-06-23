# ChangeLog

# v0.7.1 2022-06-23
- Renombre método para carga de imágenes

# v0.7.0 2022-06-22
- Agrega método LittleGameEngine.contains() para obtener todos los GameObjects que contienen a un punto dado

# 2022-06-22
- Crea clase ImageManager para el manejo de imagen
- Crea clase SoundManager para el manejo de sonidos
- Crea clase Fontmanager para el manejo de fonts
- Manejo de imágenes, sonido y fonts se llevan a las clases señaladas
- Canvas agrega método para mostrar imágenes precargadas
- Se corrigen los demos acorde a lo anterior
- Se reestructuran directorios. Todo quedaen en src/ y demos/ cambia de nombre a test/

# v0.6.0 2022-05-28
- Versión estable

# v0.5.7.2 2022-05-28
- Renombra loadTTTFont a loadTTFont()

## v0.5.7 2022-05-26
- GameObject.py
    - Se crean todas las rutinas de manejo de eventos, los objetos deberán sobreescribirlas

- LittleGameEngine.py
    - Se renombra collidesWithGObjects() a collidesWith()
    - Se ajusta main loop acorde a los cambios de GameObject
    - Se reemplazan vrias list comprehension por ciclos anidados
     
- Se ajustan demos acorde a los cambios

## v0.5.6.1 2022-05-18
- Ajustes a demos

## 2022-05-17
- Se modifica Rectangle.py para trabajar coordenadas (x,y) como floats
- Se modifica Camera.py para manejar su posición siempre con enteros
- Se modifican algunos demos según lo anterior

## 2022-05-15
- Se modifican los demos para no utilizar onCollision() ya que ralentiza demasiado el mainloop

## v0.5.6 2022-05-10
- GameObject.py
    - Agrega método getLayer()
- Sprite.py
    - Corrige método SetImage
- LittleGameEngine.py
    - Agrega método findGObjectsByTag()
- Agrega demo "Cementerio"

## 2022-04-26
- Sprite.py:Corrige errorn en retorno de setImage()

## v0.5.5 2022-04-24
- GameObject.py
    - Permite múltiples rectángulos como colisionador
    - Renombra useColliders() a enableCollider()
    - Agrega setCollider() para establecer varios rectángulos como parte del colisionador
    - Agrega getCollider() para retornar los rectángulos ajustados a las coordenadas
    - Agrega collidesWith() para determinar su colisiona con un GameObject dado
- Sprite.py
    - Agrega getImagesIndex() para retornar el indice actual dentro de la secuencia de imagenes
    - getImagesName() retorna ahora el nombre de la secuencia de imágenes en uso
    - nextImage() retorna ahora el indice actual dentro de la secuencia de imagenes
    - setImage() retorna ahora el indice actual dentro de la secuencia de imagenes
    - Ajusta uso de colisiones
- LittleGameEngine.py
    - Se modifica para manejar múltiples rectángulos en las colisiones
- Se ajustan los demos acorde a los cambios

## v0.5.4 2022-04-23
- Sprite.py: 
    - Modifica constructor para recibir una única referencia a una secuencia de imágenes
    - Cambia de nombre método getCurrentIName() a getImagesName()
    - Elimina método getCurrentIdx() 
    - Cambia de nombre método nextShape() a nextShapeImage()
    - Cambia de nombre y modifica método setShape() por setImage()
- Se ajustan los demos acorde a los cambios

## v0.5.3 2022-04-22
- Cambia coordenadas a la clásica 2D coincidiendo así con las coordenadas de pantalla (IV cuadrante)

## v0.5.2.1 2022-04-21
- Documentación

## v0.5.2 2022-04-07
- Formateo de código con PyDev
- Agrega clase para manejar clic del mouse
- Mejora manejo de eventos de teclado y mouse

## v0.5.1 2020-04-05
- Convierte nombres de variables y métodos a camelCase

## 2022-05-04
- Deja disponible el objeto LGE dentro de cada GameObject
- Ajusta demos

## v0.5.0 2022-04-03
- Corrige métodos DrawCircle y DrawCanvas en la referencia a "surface"
- Modifica activación de eventos para ser realizada sólo sobre un GameObject
- Actualiza demos

## 2022-04-01
- Elimina archivo Clases.md dado que se documentará todo con pdoc3
- Elimina directorio plantilla
- Inicia documentación del código utilizando docstrings
- Corrige método Intersect de la clase Rectangle
- Mejora captura de eventos
- Mejora detección de colisiones
- Corrige seteo de volumen en clips de audio
- AJusta varios demos


## 2022-04-01
- Mueve directorios fonts, images y sounds a subdirectorio resources
- Cambia de nombre archivo Engine.py a LittleGameEngine, reordena su código y cambia invocación inicial a LGE
- Formatea código acorde a pep8
- Modifica código para alinearlo acorde al avance de la versión java JLittleGameMachine
- Ajusta demos acorde a los cambos

## @v0.4.3 2022-03-08
- Agrega eventos OnQuit() a ser ejecutados justo antes de pygame.quit()
- En Canvas elimina método DrawImage() y agrega DrawSurface()
- Agrega demo para mostrar imágenes capturadas con opencv dentro de un Canvas

## @v0.4.2 2022-03-07
- Modifica orde de invocación de los OnCollision()
- Ajusta todas las posiciones y tamaños a int()
- Modifica Engine para que el target de la cámara se ajuste después de todos los eventos y justo antes del rendering
- Agrega plantilla base para generar juegso tipo plataforma
- Cambia todos los archivos de CRLF a LF

## @v0.4.1 2022-03-06
- Agrega método para activar/desactivar eventos en el loop
- Ordena demos/Benchmark
- Ajusta demos acorde al cambio en el loop

## @v0.4.0 2022-03-05
- Optimizaciones en la clase Rectangle
- Optimización en el manejo de colisiones
- Agrega prefijo "_" a las variables de clase
- Agrega método DrawImage en Canvas
- Optimizaciones varias en Engine

## @v0.3.0 2022-02-26
- Se reversa el uso de múltiples colliders en un GameObject hasta no tener un mejor algoritmo
- Optimizaciones varias
- Se ajustan los demos acorde a los cambios


## 2022-02-25
- Renombra Rect.py a Rectangle.py y actualiza todos los archivos afectados
- Agrega demo con pseudo-física
- Modifica uso de colliders permitiendo multiples rectángulos

## 2022-02-24
- Agrego demo de Canvas con rebote de pelotas
- Optimiza CollideRect en Rect
- Avanza en Canvas
- Corrige y mejora demos

## 2022-02-23
- Corrige algunos cálculos en Rect.py y Camera.py
- Los GameObject deben ahora habilitar el uso del collider
- Agregas mas eventos en el loop principal
- Ajusta demos acorde a los cambios

## 2022-02-22
- Elimina round() e int() de todos los métodos
- dt es entregado como segundos en lugar de milisegundos
- Elimina game object del tipo Text
- Agrega game object del tipo Canvas
- Reordena directorio de demos
- Ajusta demos acorde a los cambios

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

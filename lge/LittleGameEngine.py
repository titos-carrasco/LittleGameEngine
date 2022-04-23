"""
La Pequena Maquina de Juegos (LGE)

@author Roberto carrasco (titos.carrasco@gmail.com)
"""

from glob import glob
import pygame

from lge.Camera import Camera
from lge.GameObject import GameObject
from lge.Rectangle import Rectangle


class LittleGameEngine():
    CONSTANTS = pygame.constants
    GUI_LAYER = 0xFFFF
    E_ON_DELETE = 0b00000001
    E_ON_START = 0b00000010
    E_ON_PRE_UPDATE = 0b00000100
    E_ON_UPDATE = 0b00001000
    E_ON_POST_UPDATE = 0b00010000
    E_ON_COLLISION = 0b00100000
    E_ON_PRE_RENDER = 0b01000000
    E_ON_QUIT = 0b10000000

    lge = None

    # ------ game engine ------
    def __init__(self, camSize:tuple, title:str, bgColor:tuple):
        """
        Crea el juego
        
        : *winSize* : dimensiones de la ventana de despliegue
        : *title* : titulo de la ventana
        : *bgColor* : color de fondo de la ventana
         """
        assert LittleGameEngine.lge is None, "LittleGameEngine ya se encuentra activa"
        LittleGameEngine.lge = self

        self.fpsData = [0] * 30
        self.fpsIdx = 0

        self.running = False
        self.onMainUpdate = None

        self.bgColor = bgColor
        self.collidersColor = None

        self.fonts = {}
        self.sounds = {}
        self.images = {}

        self.gObjects = {}
        self.gLayers = {}
        self.gObjectsToAdd = []
        self.gObjectsToDel = []

        self.camera = Camera((0, 0), camSize)

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.key.set_repeat(0)
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode(camSize)
        self.keysPressed = pygame.key.get_pressed()

    def getInstance():
        """
        Obtiene una instancia del juego en ejecucion. Util para las diferentes clases
        utilizadas en un juego tal de acceder a metodos estaticos
        
        **Retorna**
        : *LittleGameEngine* : una referencia a LGE en ejecucion 
         """
        return LittleGameEngine.lge

    def getFPS(self) -> float:
        """
        Obtiene los FPS calculados como el promedio de los ultimos 30 valores
        
        **Retorna**
        : *float* : los frame por segundo calculados
         """
        dt = 0.0
        for val in self.fpsData:
            dt += val
        dt = dt / len(self.fpsData)
        return 0 if dt == 0 else 1 / dt

    def showColliders(self, color:tuple):
        """
        Si se especifica un color se habilita el despliegue del rectangulo que bordea
        a todos los objetos (util para ver colisiones).
        
        Si se especifica None se desactiva
        
        **Parametros**
        : *color* : el color para los bordes de los rectangulos
        """
        self.collidersColor = color

    def setOnMainUpdate(self, func):
        """
        Establece la funcion/metodo que recibira el evento onMainUpdate que es invocado justo
        despues de invocar a los metodos onUpdate() de los GameObjects.
        
        **Parametros**
        : *func* : la funcion o metodo que procesara los eventos onMainUpdate
         """
        self.onMainUpdate = func

    def quit(self):
        """
        Finaliza el Game Loop de LGE
        """
        self.running = False

    def run(self, fps:int):
        """
        Inicia el Game Loop de LGE tratando de mantener los fps especificados
     
        : *fps* : los fps a mantener
        """
        clock = pygame.time.Clock()
        self.running = True
        while(self.running):
            # events
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.running = False

            # --- tiempo en ms desde el ciclo anterior
            dt = clock.tick(fps) / 1000.0
            self.fpsData[self.fpsIdx] = dt
            self.fpsIdx += 1
            self.fpsIdx %= len(self.fpsData)

           # --- Del gobj and gobj.onDelete
            ondelete = []
            for gobj in self.gObjectsToDel:
                del self.gObjects[gobj.name]
                self.gLayers[gobj.layer].remove(gobj)
                if(self.camera.target == gobj):
                    self.camera.target = None
                if((gobj.onEventsEnabled & LittleGameEngine.E_ON_DELETE)):
                    self.ondelete.append(gobj)
            self.gObjectsToDel = []
            for gobj in ondelete:
                gobj.onDelete()
            del ondelete

            # --- Add Gobj and gobj.onStart
            reorder = False
            onstart = []
            for gobj in self.gObjectsToAdd:
                layer = gobj.layer
                if(not layer in self.gLayers):
                    self.gLayers[layer] = []
                    reorder = True
                gobjs = self.gLayers[layer]
                if(not gobj in gobjs):
                    self.gLayers[gobj.layer].append(gobj)
                    if((gobj.onEventsEnabled & LittleGameEngine.E_ON_START)):
                        onstart.append(gobj)
            self.gObjectsToAdd = []
            for gobj in onstart:
                gobj.onStart()
            del onstart

            # ---
            if(reorder):
                self.gLayers = dict(sorted(self.gLayers.items()))
                reorder = False
            # --

            # --- gobj.onPreUpdate
            list(gobj.onPreUpdate(dt)
                    for layer, gobjs in self.gLayers.items()
                        for gobj in gobjs
                            if gobj.onEventsEnabled & LittleGameEngine.E_ON_PRE_UPDATE
                 )

            # --- gobj.onUpdate
            list(gobj.onUpdate(dt)
                    for layer, gobjs in self.gLayers.items()
                        for gobj in gobjs
                            if gobj.onEventsEnabled & LittleGameEngine.E_ON_UPDATE
                 )

            # --- gobj.onPostUpdate
            list(gobj.onPostUpdate(dt)
                    for layer, gobjs in self.gLayers.items()
                        for gobj in gobjs
                            if gobj.onEventsEnabled & LittleGameEngine.E_ON_POST_UPDATE
                 )

            # --- game.onUpdate
            if(self.onMainUpdate):
                self.onMainUpdate(dt)

            # --- gobj.onCollision
            oncollisions = []
            for layer, gobjs in self.gLayers.items():
                if(layer == LittleGameEngine.GUI_LAYER):
                    continue
                withUseColliders = list([gobj for gobj in gobjs if gobj.useColliders])
                withOnCollision = list([gobj for gobj in withUseColliders if gobj.onEventsEnabled & LittleGameEngine.E_ON_COLLISION])

                for o1 in withOnCollision:
                    colliders = []
                    for o2 in withUseColliders:
                        if o1 != o2:
                            if o1.rect.intersects(o2.rect):
                                colliders.append(o2)
                    oncollisions.append((o1, colliders))
            list(gobj.onCollision(dt, colliders)
                    for gobj, colliders in oncollisions
                        if colliders
                 )
            del oncollisions

            # --- gobj.onPreRender
            list(gobj.onPreRender(dt)
                    for layer, gobjs in self.gLayers.items()
                        for gobj in gobjs
                            if gobj.onEventsEnabled & LittleGameEngine.E_ON_PRE_RENDER
                 )

            # --- Camera Tracking
            self.camera.followTarget()

            # --- Rendering
            self.screen.fill(self.bgColor)

            # layers
            for layer, gobjs in self.gLayers.items():
                if(layer != LittleGameEngine.GUI_LAYER):
                    for gobj in [gobj for gobj in gobjs if(gobj.rect.intersects(self.camera.rect))]:
                        x, y = self.fixXY(gobj)
                        if(gobj.surface != None):
                            self.screen.blit(gobj.surface, (x, y))

                        if(self.collidersColor and gobj.useColliders):
                            pygame.draw.rect(self.screen, self.collidersColor, pygame.Rect((x, y), (gobj.rect.width, gobj.rect.height)), 1)

            # GUI
            for layer, gobjs in self.gLayers.items():
                if(layer == LittleGameEngine.GUI_LAYER):
                    for gobj in gobjs:
                        if(gobj.surface != None):
                            x, y = gobj.getPosition()
                            self.screen.blit(gobj.surface, (x, y))

            # ---
            pygame.display.update()

        # --- gobj.onQuit
        list(gobj.onQuit()
                for layer, gobjs in self.gLayers.items()
                    for gobj in gobjs
                        if gobj.onEventsEnabled & LittleGameEngine.E_ON_QUIT
             )

        # eso es todo
        pygame.quit()

    # sistema cartesiano y zona visible dada por la camara
    def fixXY(self, gobj:GameObject) -> tuple:
        """
        Traslada las coordenadas del GameObject a la zona de despliegue de la camara
        
        **Parametros**
        : *gobj* : el objeto del cual trasladar sus coordenadas
        
        **Retorna**
        : *tuple* : las coordenadas trasladadas
        """
        xo = gobj.rect.x
        vx = self.camera.rect.x
        x = xo - vx

        yo = gobj.rect.y
        vy = self.camera.rect.y
        y = yo - vy
        return x, y

    # ------ gobjects ------
    def addGObject(self, gobj:GameObject, layer:int):
        """
        Agrega un GameObject al juego el que quedara habilitado en el siguiente ciclo
        
        **Parametros**
        : *gobj* :  el gameObject a agregar
        : *layer* : la capa a la cual pertenece
        """
        assert gobj.layer < 0, "'gobj' ya fue agregado"
        assert layer >= 0 and layer <= LittleGameEngine.GUI_LAYER, "'layer' invalido"
        gobj.layer = layer
        self.gObjects[gobj.name] = gobj
        self.gObjectsToAdd.append(gobj)

    def addGObjectGUI(self, gobj:GameObject):
        """
        Agrega un GameObject a la interfaz grafica del juego
        
        **Parametros**
        : *gobj* : el GameObject a agregar
        """
        self.addGObject(gobj, LittleGameEngine.GUI_LAYER)

    def getGObject(self, name:str) -> GameObject:
        """
        Retorna el GameObject identificado con el nombre especificado
        
        **Parametros**
        : *name* : el nombre del GameObject a buscar
        
        **Retorna**
        : *GameObject* : el GameObject buscado (nulo si no lo encuentra)
        """
        return self.gObjects[name]

    def getCountGObjects(self) -> int:
        """
        Retorna el total de GameObjects en el juego
        
        **Retorna**
        : *int* : el total de gameObjects
        """
        return len(self.gObjects)

    def delGObject(self, gobj:GameObject):
        """
        Elimina un GameObject del juego en el siguiente ciclo
        
        **Parametros**
        : *gobj* : el gameObject a eliminar        
        """
        assert gobj.layer >= 0, "'gobj' no ha sido agregado"
        self.gObjectsToDel.append(gobj)

    def intersectGObjects(self, gobj) -> list:
        """
        Obtiene todos los GameObject que colisionan con un GameObject dado en la
        misma capa
        
        **Parametros**
        : *gobj* : el GameObject a inspeccionar
        
        **Retorna**
        : *list* : los GameObjects con los que colisiona
        """
        if(gobj.useColliders):
            layer = gobj.layer
            return [o for o in self.gLayers[layer] if o != gobj and o.useColliders and gobj.rect.intersects(o.rect)]

        return []

    # ------ camera ------
    def getCameraPosition(self) -> tuple:
        """
        Retorna la posiciona de la camara
        
        **Retorna**
        
        : *tuple* : la posicion
        """
        return self.camera.getPosition()

    def getCameraSize(self) -> tuple:
        """
        Retorna la dimension de la camara
        
        **Retorna**
        : *tuple* : la dimension
        """
        return self.camera.getSize()

    def setCameraTarget(self, gobj:GameObject, center:bool=True):
        """
        Establece el GameObject al cual la camara seguira de manera automatica
        
        **Parametros**
        : *gobj* : el GameObject a seguir
        : *center* : si es verdadero la camara se centrara en el centro del
                     GameObject, en caso contrario lo hara en el extremo superior
                     izquierdo
        """
        assert gobj.layer >= 0, "'gobj' no ha sido agregado"
        assert gobj.layer != LittleGameEngine.GUI_LAYER, "'gobj' invalido"

        self.camera.target = gobj
        self.camera.targetInCenter = center

    def setCameraBounds(self, bounds:Rectangle):
        """
        Establece los limites en los cuales se movera la camara
        
        **Parametros**
        : *bounds* : los limites
        """
        self.camera.setBounds(bounds)

    def setCameraPosition(self, x:float, y:float):
        """
        Establece la posicion de la camara
        
        **Parametros**
        : *position* : la posicion
        """
        self.camera.setPosition(x, y)

    # ------ keys ------
    def keyPressed(self, key:int) -> bool:
        """
        Determina si una tecla se encuentra presionada o no
        
        **Parametros**
        : *key* : la tecla a inspeccionar
        
        **Retorna**
        : *bool* : verdadero si la tecla se encuentra presionada
        """
        return pygame.key.get_pressed()[key]

    # ------ mouse ------
    def getMouseButtons(self) -> list:
        """
        Retorna el estado de los botones del mouse
        
        **Retorna**
        : *list* : el estado de los botones
        """
        return pygame.mouse.get_pressed()

    def getMousePosition(self) -> tuple:
        """
        Determina la posicion del mouse en la ventana
        
        **Retorna**
        : *tuple* : la posicion del mouse
        """
        x, y = pygame.mouse.get_pos()
        return x, y

    # ------ fonts ------
    def getSysFonts(self) -> list:
        """
        Obtiene los tipos de letra del sistema
        
        **Retorna**
        : *list* : los tipos de letra
        """
        return pygame.font.get_fonts()

    def loadSysFont(self, name:str, size:int, bold:bool=False, italic:bool=False):
        """
         Carga un tipo de letra para ser utilizado en el juego
        
        **Parametros**
        : *name* : nombre interno a asignar
        : *size* : tamano del tipo de letra
        : *bold* : true para usar negrita
        : *italic* : true para usar italica
        """
        if(not name in self.fonts):
            font = pygame.font.SysFont(name, size, bold, italic)
            self.fonts[name] = font

    def loadTTFFont(self, name:str, path:str, size:int):
        """
         Carga un tipo de letra True Type para ser utilizado en el juego
        
        **Parametros**
        : *name* : nombre interno a asignar
        : *path* : nombre del archivo que contiene la fuente TTF
        : *size* : tamano del tipo de letra
        """
        if(not name in self.fonts):
            font = pygame.font.Font(path, size)
            self.fonts[name] = font

    def getFont(self, fname:str):
        """
        Recupera un tipo de letra previamente cargado
        
        **Parametros**
        : *fname* : el nombre del tipo de letra a recuperar
        
        **Retorna**
        : *pygame.Font* : el tipo de letra
        """
        return self.fonts[fname]

    # ------ sounds ------
    def loadSound(self, name:str, fname:str):
        """
        Carga un archivo de sonido para ser utilizado durante el juego
        
        **Parametros**
        : *name* :  nombre a asignar al sonido
        : *fname* : nombre del archivo que contiene el sonido
        """
        self.sounds[name] = pygame.mixer.Sound(fname)

    def playSound(self, name:str, loop:int, level:float):
        """
        Inicia la reproduccion de un sonido
        
        **Parametros**
        :  *name* : el sonido (previamente cargado) a reproducir
        : *loop* : el numero de veces a repetirlo
        : *level* : el nivel de volumen
        """
        if(loop):
            loop = -1
        else:
            loop = 0
        self.sounds[name].set_volume(level / 100)
        self.sounds[name].play(loop)

    def stopSound(self, name:str):
        """
        Detiene la reproduccion de un sonido
        
        **Parametros**
        : *name* : el nombre del sonido a detener
        """
        self.sounds[name].stop()

    def setSoundVolume(self, name:str, level:float):
        """
        Establece el volumen de un sonido previamente cargado
        
        **Paranmetros**
        : *name* :  el nombre del sonido
        : *level* : el nivel de volumen
        """
        self.sounds[name].set_volume(level / 100)

    def getSoundVolume(self, name:str) -> float:
        """
        Obtiene el volumen de un sonido previamente cargado
        
        **Paranmetros**
        : *name* : el nombre del sonido
        
        
        **Retorna**
        : *float* : el nivel de volumen
        """
        return self.sounds[name].get_volume() * 100

    #  ------ images ------
    def createOpaqueImage(self, width:int, height:int) -> pygame.Surface:
        """
        Crea una imagen sin transparencia de dimensiones dadas
        
        **Parametros**
        : *width* : ancho deseado
        : *height* : alto deseado
        
        **Retorna**
        : *pygame.Surface* : la imagen creada
        """
        return pygame.Surface((width, height))

    def createTranslucentImage(self, width, height):
        """
        Crea una imagen con transparencia de dimensiones dadas
        
        **Parametros**
        : *width* : ancho deseado
        : *height* : alto deseado
        
        **Retorna**
        : *pygame.Surface* : la imagen creada
        """
        return pygame.Surface((width, height), pygame.SRCALPHA)

    def getImages(self, iname) -> list:
        """
        Recupera un grupo de imagenes previamente cargadas
        
        **Parametros**
        : *iname* : el nombre asignado al grupo de imagenes
        
        **Retorna**
        : *list* : las imagenes
        """
        return [image for image in self.images[iname]]

    def loadImage(self, iname, pattern:str, scale=None, flip:list=None):
        """
        Cara una imagen o grupo de imagenes desde archivos para ser utilizadas en el
        juego
        
        **Parametros**
        : *iname* : nombre a asignar a la imagen o grupo de imagenes cargados
        : *pattern* : nombre del archivo de imagenes a cargar. Si contiene un '\*' se
                      cargaran todas las imagenes con igual nombre utilizando dicho
                      caracter como caracter comodin de busqueda (ej.imagen_0*.png)
        : *scale* : si es un float corresponde al factor de escala a aplicar a la imagen cargada
        : *scale* : si es una tupla (width, height) corresponde al nuevo tamano de la imagen cargada
        : *flip* : (true, true) para invertir la imagen en el eje X e Y
        """
        if("*" in pattern):
            fnames = sorted(glob(pattern))
        else:
            fnames = [pattern]

        if(flip):
            fx, fy = flip

        surfaces = []
        for fname in fnames:
            surface = pygame.image.load(fname).convert_alpha()
            if(scale):
                if(not isinstance(scale, tuple)):
                    w, h = surface.get_size()
                    scale = (int(w * scale), int(h * scale))
                surface = pygame.transform.smoothscale(surface, scale)
            if(flip):
                surface = pygame.transform.flip(surface, fx, fy)
            surfaces.append(surface)
        self.images[iname] = surfaces

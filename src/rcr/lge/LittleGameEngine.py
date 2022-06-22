"""
La Pequena Maquina de Juegos (LGE)

@author Roberto carrasco (titos.carrasco@gmail.com)
"""
import pygame
import sys

from lge.Camera import Camera
from lge.FontManager import FontManager
from lge.GameObject import GameObject
from lge.ImageManager import ImageManager
from lge.Rectangle import Rectangle
from lge.SoundManager import SoundManager


class LittleGameEngine():
    CONSTANTS = pygame.constants
    GUI_LAYER = 0xFFFF
    lge = None

    # ------ game engine ------
    def __init__(self, winSize:tuple, title:str, bgColor:tuple):
        """
        Crea el juego

        : *winSize* : dimensiones de la ventana de despliegue
        : *title* : titulo de la ventana
        : *bgColor* : color de fondo de la ventana
         """
        if(LittleGameEngine.lge is not None):
            print("LittleGameEngine ya se encuentra activa")
            sys.exit();

        LittleGameEngine.lge = self
        self.running = False
        self.winSize = winSize

        self.fpsData = [0] * 30
        self.fpsIdx = 0

        self.onMainUpdate = None

        self.bgColor = bgColor
        self.collidersColor = None

        self.imageManager = ImageManager()
        self.fontManager = FontManager()
        self.soundManager = SoundManager()

        self.gObjects = {}
        self.gLayers = {}
        self.gObjectsToAdd = []
        self.gObjectsToDel = []

        self.camera = Camera((0, 0), winSize)

        pygame.display.init()
        self.screen = pygame.display.set_mode(winSize)
        self.screen.fill(self.bgColor)
        pygame.display.flip()
        pygame.display.set_caption(title)

        pygame.key.set_repeat(0)
        self.keysPressed = pygame.key.get_pressed()

    def getInstance():
        """
        Obtiene una instancia del juego en ejecucion. Util para las diferentes clases
        utilizadas en un juego tal de acceder a metodos estaticos

        **Retorna**
        : *LittleGameEngine* : una referencia a LGE en ejecucion
         """
        if(LittleGameEngine.lge is None):
            print("LittleGameEngine no se encuentra activa")
            sys.exit();

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
        return 0 if dt == 0 else 1.0 / dt

    def showColliders(self, color:tuple):
        """
        Si se especifica un color se habilita el despliegue del rectangulo que bordea
        a todos los objetos (util para ver colisiones).

        Si se especifica None se desactiva

        **Parametros**
        : *color* : el color para los bordes de los rectangulos
        """
        self.collidersColor = color

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
            for gobj in self.gObjectsToDel:
                del self.gObjects[gobj.name]
                self.gLayers[gobj.layer].remove(gobj)
                if(self.camera.target == gobj):
                    self.camera.target = None
            for gobj in self.gObjectsToDel:
                gobj.onDelete()
            self.gObjectsToDel = []

            # --- Add Gobj and gobj.onStart
            reorder = False
            for gobj in self.gObjectsToAdd:
                layer = gobj.layer
                if(not layer in self.gLayers):
                    self.gLayers[layer] = []
                    reorder = True
                gobjs = self.gLayers[layer]
                if(not gobj in gobjs):
                    self.gLayers[gobj.layer].append(gobj)
            for gobj in self.gObjectsToAdd:
                gobj.onStart()
            self.gObjectsToAdd = []

            # ---
            if(reorder):
                self.gLayers = dict(sorted(self.gLayers.items()))
                reorder = False
            # --

            # --- gobj.onPreUpdate
            for layer, gobjs in self.gLayers.items():
                for gobj in gobjs:
                    gobj.onPreUpdate(dt)

            # --- gobj.onUpdate
            for layer, gobjs in self.gLayers.items():
                for gobj in gobjs:
                    gobj.onUpdate(dt)

            # --- gobj.onPostUpdate
            for layer, gobjs in self.gLayers.items():
                for gobj in gobjs:
                    gobj.onPostUpdate(dt)

            # --- game.onMainUpdate
            if(self.onMainUpdate):
                self.onMainUpdate(dt)

            # --- gobj.onCollision
            oncollisions = []
            for layer, gobjs in self.gLayers.items():
                if(layer == LittleGameEngine.GUI_LAYER):
                    continue
                withUseColliders = list([gobj for gobj in gobjs if gobj.useCollider])
                withOnCollision = list([gobj for gobj in withUseColliders if gobj.callOnCollision])

                for o1 in withOnCollision:
                    colliders = []
                    for o2 in withUseColliders:
                        if o1 != o2:
                            if o1.collidesWith(o2):
                                colliders.append(o2)
                    oncollisions.append((o1, colliders))
            list(gobj.onCollision(dt, colliders)
                    for gobj, colliders in oncollisions
                        if colliders
                 )
            del oncollisions

            # --- gobj.onPreRender
            for layer, gobjs in self.gLayers.items():
                for gobj in gobjs:
                    gobj.onPreRender(dt)

            # --- Camera Tracking
            self.camera.followTarget()

            # --- Rendering
            self.screen.fill(self.bgColor)

            # layers
            for layer, gobjs in self.gLayers.items():
                if(layer != LittleGameEngine.GUI_LAYER):
                    for gobj in [gobj for gobj in gobjs if(gobj.rect.intersects(self.camera.rect))]:
                        x, y = self.fixXY(gobj.getPosition())
                        if(gobj.surface != None):
                            self.screen.blit(gobj.surface, (x, y))

                        if(self.collidersColor and gobj.useCollider):
                            for r in gobj.getCollider():
                                x, y = self.fixXY((r.x, r.y))
                                pygame.draw.rect(self.screen, self.collidersColor, pygame.Rect((x, y), (r.width, r.height)), 1)

            # GUI
            for layer, gobjs in self.gLayers.items():
                if(layer == LittleGameEngine.GUI_LAYER):
                    for gobj in gobjs:
                        if(gobj.surface != None):
                            x, y = gobj.getPosition()
                            self.screen.blit(gobj.surface, (x, y))

            # ---
            pygame.display.flip()

        # --- gobj.onQuit
        for layer, gobjs in self.gLayers.items():
            for gobj in gobjs:
                gobj.onQuit()

        # eso es todo
        pygame.quit()

    # sistema cartesiano y zona visible dada por la camara
    def fixXY(self, position:tuple) -> tuple:
        """
        Traslada las coordenadas del GameObject a la zona de despliegue de la camara

        **Parametros**
        : *position* : coordenadas a convertir

        **Retorna**
        : *tuple* : las coordenadas trasladadas
        """
        x, y = position
        xo = x
        vx = self.camera.rect.x
        x = xo - vx

        yo = y
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

    def findGObjectsByTag(self, layer:int, tag:str) -> list:
        """
        Retorna los GameObject cuto tag comienza con el tag especificado

        **Parametros**
        : *layer* : el layer de los GameObject a buscar
        : *tag* : el texto de inicio del tag

        **Retorna**
        : *list* : la lista de GameObjects (nulo si no lo encuentra)
        """
        return [o
                for o in self.gLayers[layer]
                    if o.tag.startswith(tag)]

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
        self.gObjectsToDel.append(gobj)

    def collidesWith(self, gobj) -> list:
        """
        Obtiene todos los GameObject que colisionan con un GameObject dado en la
        misma capa

        **Parametros**
        : *gobj* : el GameObject a inspeccionar

        **Retorna**
        : *list* : los GameObjects con los que colisiona
        """
        if(gobj.useCollider):
            layer = gobj.layer
            return [o
                    for o in self.gLayers[layer]
                        if o != gobj and o.useCollider and gobj.collidesWith(o)]

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

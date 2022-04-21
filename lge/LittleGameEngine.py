"""
La Pequena Maquina de Juegos

@author Roberto carrasco (titos.carrasco@gmail.com)
"""

from glob import glob
import pygame

from lge.Camera import Camera


class LittleGameEngine():
    CONSTANTS = pygame.constants
    VLIMIT = 0xFFFFFFFF
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
    def __init__(self, camSize, title, bgColor):
        """
        Crea el juego
        
        Parametros
            - tuple camSize : alto y ancho de la ventana de despliegue
            - string title : titulo de la ventana
            - tuple bgColor : color de fondo de la ventana
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
        return LittleGameEngine.lge

    def getFPS(self):
        dt = 0.0
        for val in self.fpsData:
            dt += val
        dt = dt / len(self.fpsData)
        return 0 if dt == 0 else 1 / dt

    def showColliders(self, color):
        self.collidersColor = color

    def setOnMainUpdate(self, func):
        self.onMainUpdate = func

    def quit(self):
        self.running = False

    def run(self, fps):
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
                            w, h = gobj.getSize()
                            self.screen.blit(gobj.surface, (x, self.camera.rect.height - y - h))

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
    def fixXY(self, gobj):
        xo = gobj.rect.x
        yo = gobj.rect.y
        # wo = gobj.rect.width
        ho = gobj.rect.height

        wh = LittleGameEngine.VLIMIT

        vx = self.camera.rect.x
        vy = self.camera.rect.y
        # vw = self.camera.rect.width
        vh = self.camera.rect.height

        dy = wh - (vy + vh)
        x = xo - vx
        y = wh - (yo + ho) - dy

        return x, y

    # ------ gobjects ------
    def addGObject(self, gobj, layer):
        assert gobj.layer < 0, "'gobj' ya fue agregado"
        assert layer >= 0 and layer <= LittleGameEngine.GUI_LAYER, "'layer' invalido"
        gobj.layer = layer
        self.gObjects[gobj.name] = gobj
        self.gObjectsToAdd.append(gobj)

    def addGObjectGUI(self, gobj):
        self.addGObject(gobj, LittleGameEngine.GUI_LAYER)

    def getGObject(self, name):
        return self.gObjects[name]

    def getCountGObjects(self):
        return len(self.gObjects)

    def delGObject(self, gobj):
        assert gobj.layer >= 0, "'gobj' no ha sido agregado"
        self.gObjectsToDel.append(gobj)

    def intersectGObjects(self, gobj):
        if(gobj.useColliders):
            layer = gobj.layer
            return [o for o in self.gLayers[layer] if o != gobj and o.useColliders and gobj.rect.intersects(o.rect)]

        return []

    # ------ camera ------
    def getCameraPosition(self):
        return self.camera.getPosition()

    def getCameraSize(self):
        return self.camera.getSize()

    def setCameraTarget(self, gobj, center=True):
        assert gobj.layer >= 0, "'gobj' no ha sido agregado"
        assert gobj.layer != LittleGameEngine.GUI_LAYER, "'gobj' invalido"

        self.camera.target = gobj
        self.camera.targetInCenter = center

    def setCameraBounds(self, bounds):
        self.camera.setBounds(bounds)

    def setCameraPosition(self, x, y):
        self.camera.setPosition(x, y)

    # ------ keys ------
    def keyPressed(self, key):
            return pygame.key.get_pressed()[key]

    # ------ mouse ------
    def getMouseButtons(self):
        return pygame.mouse.get_pressed()

    def getMousePosition(self):
        x, y = pygame.mouse.get_pos()
        wh = self.camera.rect.height
        return x, wh - y - 1

    # ------ fonts ------
    def getSysFonts(self):
        return pygame.font.get_fonts()

    def loadSysFont(self, name, size, bold=False, italic=False):
        if(not name in self.fonts):
            font = pygame.font.SysFont(name, size, bold, italic)
            self.fonts[name] = font

    def loadTTFFont(self, name, path, size):
        if(not name in self.fonts):
            font = pygame.font.Font(path, size)
            self.fonts[name] = font

    def getFont(self, fname):
        return self.fonts[fname]

    # ------ sounds ------
    def loadSound(self, name, fname):
        self.sounds[name] = pygame.mixer.Sound(fname)

    def playSound(self, name, loop, level):
        if(loop):
            loop = -1
        else:
            loop = 0
        self.sounds[name].set_volume(level / 100)
        self.sounds[name].play(loop)

    def stopSound(self, name):
        self.sounds[name].stop()

    def setSoundVolume(self, name, level):
        self.sounds[name].set_volume(level / 100)

    def getSoundVolume(self, name):
        return self.sounds[name].get_volume() * 100

    #  ------ images ------
    def createOpaqueImage(self, width, height):
        return pygame.Surface((width, height))

    def createTranslucentImage(self, width, height):
        return pygame.Surface((width, height), pygame.SRCALPHA)

    def getImages(self, iname):
        return [image for image in self.images[iname]]

    def loadImage(self, iname, pattern, scale=None, flip=None):
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

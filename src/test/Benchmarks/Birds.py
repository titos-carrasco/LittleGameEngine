import cProfile
import random
import time

from lge.Canvas import Canvas
from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class Birds():

    def __init__(self):
        # instante de inicio
        self.tIni = time.time()

        # creamos el juego
        winSize = (800, 440)

        self.lge = LittleGameEngine(winSize, "Birds", (0, 0, 0))
        self.lge.onMainUpdate = self.onMainUpdate

        # cargamos los recursos que usaremos
        resourceDir = "../resources"

        self.lge.imageManager.loadImages("fondo", resourceDir + "/images/Backgrounds/FreeTileset/Fondo.png", winSize)
        self.lge.imageManager.loadImages("heroe", resourceDir + "/images/Swordsman/Idle/Idle_00*.png", 0.08)
        self.lge.imageManager.loadImages("bird", resourceDir + "/images/BlueBird/frame-*.png", 0.04)
        self.lge.fontManager.loadTTFont("monospace", resourceDir + "/fonts/FreeMono.ttf", (False, False), 16)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.addGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 0), (800, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # agregamos al heroe
        heroe = Sprite("heroe", (226, 254))
        self.lge.addGObject(heroe, 1)

        # agregamos pajaros
        ww, wh = self.lge.getCameraSize()
        for i in range(500):
            x = random.randint(0, ww)
            y = random.randint(15, wh)
            bird = Bird("bird", (x, y))
            self.lge.addGObject(bird, 1)

    def onMainUpdate(self, dt):
        # limite de ejecucion
        if(time.time() - self.tIni > 10):
            self.lge.quit()
            return

        # abortamos con la tecla Escape
        if(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_ESCAPE)):
            self.lge.quit()

        # mostramos info
        mx, my = self.lge.getMousePosition()
        mb1, mb2, mb3 = self.lge.getMouseButtons()

        info = "FPS: %07.2f - gObjs: %03d - Mouse: (%3d,%3d) (%d,%d,%d)" % (
            self.lge.getFPS(),
            self.lge.getCountGObjects(), mx, my,
            mb1, mb2, mb3
        )
        infobar = self.lge.getGObject("infobar")
        infobar.fill((20, 20, 20, 10))
        infobar.drawText(info, (140, 0), "monospace", (0, 0, 0))

    # main loop
    def run(self, fps):
        self.lge.run(fps)


class Bird(Sprite):

    def __init__(self, inames, position):
        super().__init__(inames, position)

    # @Override
    def onUpdate(self, dt):
        self.nextImage(dt, 0.1)


# ----
bird = Birds()
cProfile.run("bird.run(60)")

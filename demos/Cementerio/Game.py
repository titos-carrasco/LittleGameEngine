import pygame

from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle

from Ninja import Ninja
from Platform import Platform


class Game():

    def __init__(self):
        self.winSize = (640, 342)

        self.lge = LittleGameEngine(self.winSize, "El Cementerio", (0, 0, 0))
        self.lge.setOnMainUpdate(self.onMainUpdate)
        self.lge.showColliders((255, 0, 0))

        # cargamos los recursos que usaremos
        resourceDir = "./resources"
        self.lge.loadImage("fondo", resourceDir + "/fondo.png")
        self.lge.loadImage("ninja-idle-right", resourceDir + "/NinjaGirl/Idle_*.png", 0.1)
        self.lge.loadImage("ninja-idle-left", resourceDir + "/NinjaGirl/Idle_*.png", 0.1, (True, False))
        self.lge.loadImage("ninja-run-right", resourceDir + "/NinjaGirl/Run_*.png", 0.1)
        self.lge.loadImage("ninja-run-left", resourceDir + "/NinjaGirl/Run_*.png", 0.1, (True, False))
        self.lge.loadImage("platform", resourceDir + "/platform.png", 0.3)

        # el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.addGObject(fondo, 0)

        # los Non Player Characters (NPC)
        self.makeFloor()
        self.makePlatforms()

        # nuestra heroina
        ninja = Ninja(90, 163)
        ninja.setBounds(Rectangle((0, 0), (self.winSize[0], self.winSize[1] + 100)))
        self.lge.addGObject(ninja, 1);

    def makeFloor(self):
        suelos = [
            Canvas((0, 85), (170, 1)),
            Canvas((0, 214), (170, 1)),
            Canvas((214, 300), (128, 1)),
            Canvas((342, 214), (127, 1)),
            Canvas((470, 257), (127, 1)),
            Canvas((513, 86), (127, 1))
        ]
        for s in suelos:
            s.enableCollider(True)
            s.setTag("suelo")
            self.lge.addGObject(s, 1)

    def makePlatforms(self):
        platforms = [
            Platform(200, 200, "U", 100, 1),
            Platform(400, 100, "L", 100, 1)
        ]
        for p in platforms:
            self.lge.addGObject(p, 1)

    def onMainUpdate(self, dt):
        # abortamos con la tecla Escape
        if (self.lge.keyPressed(pygame.K_ESCAPE)):
            self.lge.quit()

    # main loop
    def run(self, fps):
        self.lge.run(fps)


# show time
game = Game()
game.run(60)
print("Eso es todo!!!")


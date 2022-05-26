import pygame

from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Rectangle import Rectangle


class Platform(Sprite):

    def __init__(self, x, y, dir, distance, speed):
        super().__init__("platform", (x, y))

        # acceso a LGE
        self.lge = LittleGameEngine.getInstance()

        # los eventos que recibiremos
        self.setCollider(Rectangle((0, 0), (self.getWidth(), 1)))
        self.enableCollider(True)
        self.setTag("plataforma")

        # mis atributos
        self.dir = dir
        self.pixels = speed
        self.distance = distance
        self.travel = 0

    # @Override
    def onUpdate(self, dt):
        x, y = self.getPosition()

        d = self.pixels * dt
        if(self.dir == "R"):
            x = x + d
        elif(self.dir == "L"):
            x = x - d
        elif(self.dir == "D"):
            y = y + d
        elif(self.dir == "U"):
            y = y - d

        self.setPosition(x, y)

        self.travel = self.travel + d
        if(self.travel > self.distance):
            self.travel = 0
            if(self.dir == "R"):
                self.dir = "L"
            elif(self.dir == "L"):
                self.dir = "R"
            elif(self.dir == "D"):
                self.dir = "U"
            elif(self.dir == "U"):
                self.dir = "D"

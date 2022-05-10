import pygame
import math

from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Rectangle import Rectangle


class Ninja(Sprite):

    def __init__(self, x, y):
        super().__init__("ninja-idle-right", (x, y))

        # acceso a LGE
        self.lge = LittleGameEngine.getInstance()
        w, h = self.lge.getCameraSize()

        # los eventos que recibiremos
        self.setOnEvents(LittleGameEngine.E_ON_POST_UPDATE)
        self.setOnEvents(LittleGameEngine.E_ON_COLLISION)
        self.enableCollider(True)

        # el colisionador
        self.colisionador = Rectangle((20, 5), (15, self.getHeight() - 5))
        self.setCollider(self.colisionador)

        # mis atributos
        self.vx = 2
        self.vy = 0
        self.g = 0.8
        self.vsalto = 8

    def fixPosition(self, dx, dy):
        gobjs = self.lge.collidesWithGObjects(self)
        for gobj in gobjs:
            tag = gobj.getTag()
            if(tag == "suelo"):
                self.setPosition(self.getX(), gobj.getY() - self.getHeight())
                return True
            elif(tag == "plataforma"):
                if(gobj.dir == "L"):
                    self.setPosition(self.getX() - gobj.pixels, gobj.getY() - self.getHeight())
                if(gobj.dir == "R"):
                    self.setPosition(self.getX() + gobj.pixels, gobj.getY() - self.getHeight())
                else:
                    self.setPosition(self.getX(), gobj.getY() - self.getHeight())
                return True

        return False

    # despues de que todo fue actualizado
    def onPostUpdate(self, dt):
        # nuestra posicion actual
        x, y = self.getPosition()
        x0, y0 = x, y

        # primero el movimiento en X
        move_x = 0
        if (self.lge.keyPressed(pygame.K_LEFT)):
            move_x = -1
            self.setImage("ninja-run-left")
        elif (self.lge.keyPressed(pygame.K_RIGHT)):
            move_x = 1
            self.setImage("ninja-run-right")
        else:
            self.setImage("ninja-idle-right")
        x = x + move_x * self.vx

        # ahora el movimiento en Y
        y = y + self.vy

        # nueva posicion
        self.setPosition(x, y)
        self.nextImage(dt, 0.04)
        self.setCollider(self.colisionador)

        # la velocidad en Y es afectada por la gravedad
        self.vy = self.vy + self.g

        # estamos en un suelo?
        onfloor = self.fixPosition(x - x0, y - y0)

        # nos piden saltar
        if(onfloor and self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_SPACE)):
            self.vy = -self.vsalto

        if(onfloor and self.vy > 0):
            self.vy = 1

    # solo para detectar premios, energia, muerte, etc...
    def onCollision(self, dt, gobjs):
        pass


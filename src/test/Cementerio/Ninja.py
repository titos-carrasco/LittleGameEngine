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
        self.enableCollider(True)

        # el colisionador
        self.colisionador = Rectangle((20, 5), (15, self.getHeight() - 5))
        self.setCollider(self.colisionador)

        # algo se fisicas
        self.vx = 120  # velocidad constante en X
        self.vy = 0  # velocidad variable en Y al saltar o caer
        self.vym = 500  # maxima velocidad en Y
        self.g = 480  # aceleración constante en Y
        self.vsalto = 140  # velocidad inicial al saltar

    def fixPosition(self, dx, dy, dt):
        gobjs = self.lge.collidesWith(self)
        for gobj in gobjs:
            tag = gobj.getTag()
            if(tag == "suelo"):
                self.setPosition(self.getX(), gobj.getY() - self.getHeight())
                return True
            elif(tag == "plataforma"):
                if(gobj.dir == "L"):
                    self.setPosition(self.getX() - gobj.pixels * dt, gobj.getY() - self.getHeight() + 1)
                elif(gobj.dir == "R"):
                    self.setPosition(self.getX() + gobj.pixels * dt, gobj.getY() - self.getHeight() + 1)
                elif(gobj.dir == "U"):
                    self.setPosition(self.getX(), self.getY() - gobj.pixels * dt)
                elif(gobj.dir == "D"):
                    self.setPosition(self.getX(), self.getY() + gobj.pixels * dt)
                return True

        return False

    # despues de que todo fue actualizado
    # @Override
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
        x = x + move_x * self.vx * dt

        # siguiente imagen y su colisionador
        self.nextImage(dt, 0.04)
        self.setCollider(self.colisionador)

        # ahora el movimiento en Y
        y = y + self.vy * dt
        self.vy = self.vy + self.g * dt

        # nueva posicion
        self.setPosition(x, y)

        # estamos en un suelo?
        onfloor = self.fixPosition(x - x0, y - y0, dt)

        # nos piden saltar
        if(onfloor):
            if(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_SPACE)):
                self.vy = -self.vsalto
            else:
                self.vy = 0

        # limitamos la velocidad en Y
        if(self.vy > self.vym):
            self.vy = self.vym

import cProfile
import random
import time

from lge.LittleGameEngine import LittleGameEngine
from lge.Canvas import Canvas


class Particles():

    def __init__(self):
        # instante de inicio
        self.tIni = time.time()

        # creamos el juego
        winSize = (800, 440)

        self.lge = LittleGameEngine(winSize, "Particles", (255, 255, 255))
        self.lge.setOnMainUpdate(self.onMainUpdate)

        # cargamos los recursos que usaremos
        resourceDir = "../resources"

        self.lge.loadTTFFont("monospace.16", resourceDir + "/fonts/FreeMono.ttf", 16)

        # agregamos la barra de info
        infobar = Canvas((0, 0), (800, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # un canvas para plotear
        panel = Canvas((0, 0), (800, 600), "Panel")
        panel.fill((255, 255, 255))
        self.lge.addGObject(panel, 1)

        # las particulas
        self.numParticles = 500
        self.particles = [0] * self.numParticles
        for i in range(self.numParticles):
            x = 300 + random.random() * 200
            y = 100 + random.random() * 100
            vx = -120 + random.random() * 240
            vy = -120 + random.random() * 240
            m = 0.1 + random.random()
            self.particles[i] = Particle(x, y, vx, vy, m)

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
        infobar.drawText(info, (140, 0), "monospace.16", (0, 0, 0))

        # las particulas
        for i in range(self.numParticles):
            particle = self.particles[i]
            particle.onUpdate(dt)

        panel = self.lge.getGObject("Panel")
        panel.fill((255, 255, 255))
        for i in range(self.numParticles):
            particle = self.particles[i]
            x = round(particle.x)
            y = round(particle.y)
            r = round(particle.m * 5)
            # panel.drawPoint( (x,y), (0,0,0) )
            # panel.drawCircle( (x,y), r, (0,0,0) )
            panel.drawRectangle((x, y), (r, r), (0, 0, 0))

    def run(self):
        self.lge.run(60)


class Particle():

    def __init__(self, x, y, vx, vy, m):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m

    def computeForce(self):
        # return 0, self.m * -9.81
        return 0, self.m * -60

    def onUpdate(self, dt):
        fx, fy = self.computeForce()
        ax, ay = fx / self.m, fy / self.m
        self.vx = self.vx + ax * dt
        self.vy = self.vy + ay * dt
        self.x = self.x + self.vx * dt
        self.y = self.y - self.vy * dt


# -- show time
game = Particles()
cProfile.run("game.run()")

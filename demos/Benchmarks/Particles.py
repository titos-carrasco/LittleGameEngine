import cProfile
import random
import time

from lge.LittleGameEngine import LittleGameEngine
from lge.Canvas import Canvas


class Particles():
    def __init__(self):
        # instante de inicio
        self.t_ini = time.time()

        # creamos el juego
        win_size = (800, 440)

        self.lge = LittleGameEngine(win_size, "Particles", (255, 255, 0))
        self.lge.SetOnMainUpdate(self.OnMainUpdate)

        # cargamos los recursos que usaremos
        resource_dir = "../resources"

        self.lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)

        # agregamos la barra de info
        infobar = Canvas((0, 420), (800, 20), "infobar")
        self.lge.AddGObjectGUI(infobar)

        # un canvas para plotear
        panel = Canvas((0, 0), (800, 600), "Panel")
        panel.Fill((255, 255, 255))
        self.lge.AddGObject(panel, 1)

        # las particulas
        self.num_particles = 500
        self.particles = [0]*self.num_particles
        for i in range(self.num_particles):
            x = 100 + random.random()*600
            y = 300 + random.random()*200
            vx = -60 + random.random()*120
            vy = -120 + random.random()*240
            m = 0.1 + random.random()
            self.particles[i] = Particle(x, y, vx, vy, m)

    def OnMainUpdate(self, dt):
        # limite de ejecucion
        if(time.time() - self.t_ini > 10):
            self.lge.Quit()
            return

        # abortamos con la tecla Escape
        if(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_ESCAPE)):
            self.lge.Quit()

        # mostramos info
        mx, my = self.lge.GetMousePosition()
        mb1, mb2, mb3 = self.lge.GetMouseButtons()

        info = "FPS: %07.2f - gObjs: %03d - Mouse: (%3d,%3d) (%d,%d,%d)" % (
            self.lge.GetFPS(),
            self.lge.GetCountGObjects(), mx, my,
            mb1, mb2, mb3
        )
        infobar = self.lge.GetGObject("infobar")
        infobar.Fill((20, 20, 20, 10))
        infobar.DrawText(info, (140, 0), "monospace.16", (0, 0, 0))

        # las particulas
        for i in range(self.num_particles):
            particle = self.particles[i]
            particle.OnUpdate(dt)

        panel = self.lge.GetGObject("Panel")
        panel.Fill((255, 255, 255))
        for i in range(self.num_particles):
            particle = self.particles[i]
            x = round(particle.x)
            y = round(particle.y)
            r = round(particle.m*5)
            #panel.DrawPoint( (x,y), (0,0,0) )
            #panel.DrawCircle( (x,y), r, (0,0,0) )
            panel.DrawRectangle((x, y), (r, r), (0, 0, 0))

    def Run(self):
        self.lge.Run(60)


class Particle():
    def __init__(self, x, y, vx, vy, m):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m

    def ComputeForce(self):
        # return 0, self.m * -9.81
        return 0, self.m * -60

    def OnUpdate(self, dt):
        fx, fy = self.ComputeForce()
        ax, ay = fx/self.m, fy/self.m
        self.vx = self.vx + ax*dt
        self.vy = self.vy + ay*dt
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt


# -- show time
game = Particles()
cProfile.run("game.Run()")

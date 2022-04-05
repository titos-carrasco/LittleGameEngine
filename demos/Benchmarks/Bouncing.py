import cProfile
import random
import time

from lge.LittleGameEngine import LittleGameEngine
from lge.Canvas import Canvas


class Bouncing():
    def __init__(self):
        # instante de inicio
        self.t_ini = time.time()

        # creamos el juego
        win_size = (800, 440)

        self.lge = LittleGameEngine(win_size, "Bouncing Balls", (255, 255, 255))
        self.lge.SetOnMainUpdate(self.OnMainUpdate)
        #self.lge.ShowColliders((255, 0, 0))

        # cargamos los recursos que usaremos
        resource_dir = "../resources"

        self.lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)

        # agregamos la barra de info
        infobar = Canvas((0, 420), (800, 20), "infobar")
        self.lge.AddGObjectGUI(infobar)

        # agregamos el suelo
        ground = Canvas((0, 0), (800, 100), "ground")
        ground.Fill((200, 200, 200))
        ground.SetTag("ground")
        ground.UseColliders(True)
        self.lge.AddGObject(ground, 1)

        # los objetos a rebotar
        for i in range(100):
            x = 50 + random.random()*700
            y = 200 + random.random()*200
            vx = -50 + random.random()*100
            vy = 0
            gobj = Ball(x, y, vx, vy)
            self.lge.AddGObject(gobj, 1)

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

    def Run(self):
        self.lge.Run(60)


class Ball(Canvas):
    def __init__(self, x, y, vx, vy):
        super().__init__((x, y), (20, 20))

        # acceso al motor de juegos
        self.lge = self.GetLGE()

        self.vx = vx
        self.vy = vy
        self.g = 240
        self.e = 0.8
        self.Fill((0, 128, 0, 200))
        self.UseColliders(True)
        self.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.SetOnEvents(LittleGameEngine.E_ON_COLLISION)

    def OnUpdate(self, dt):
        x, y = self.GetPosition()

        x = x + self.vx*dt
        y = y + self.vy*dt

        if(x < 0):
            self.lge.DelGObject(self)
            return

        self.vy = self.vy - self.g*dt
        self.SetPosition(x, y)

    def OnCollision(self, dt, gobjs):
        for gobj in gobjs:
            if(gobj.GetTag() == "ground"):
                self.SetPosition(self.GetX(), gobj.GetY() + gobj.GetHeight())

                self.vy = -self.vy*self.e
                if(abs(self.vy) < 30):
                    self.vy = 0
                    self.vx = 0
                    self.g = 0
                break


# -- show time
game = Bouncing()
cProfile.run("game.Run()")

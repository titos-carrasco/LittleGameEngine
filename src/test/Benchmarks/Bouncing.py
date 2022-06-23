import cProfile
import random

from lge.Canvas import Canvas
from lge.LittleGameEngine import LittleGameEngine


class Bouncing():

    def __init__(self, fps):
        self.fps = fps

        # instante de inicio
        self.counter = self.fps * 10

        # creamos el juego
        winSize = (800, 440)

        self.lge = LittleGameEngine(winSize, "Bouncing Balls", (255, 255, 255))
        self.lge.onMainUpdate = self.onMainUpdate
        # self.lge.showColliders((255, 0, 0))

        # cargamos los recursos que usaremos
        resourceDir = "../resources"

        self.lge.fontManager.loadTTFont("monospace", resourceDir + "/fonts/FreeMono.ttf", (False, False), 16)

        # agregamos la barra de info
        infobar = Canvas((0, 0), (800, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # agregamos el suelo
        self.ground = Canvas((0, 340), (800, 100), "ground")
        self.ground.fill((200, 200, 200))
        self.ground.enableCollider(True)
        self.lge.addGObject(self.ground, 1)

        # los objetos a rebotar
        for i in range(200):
            x = random.randint(50, 750)
            y = random.randint(50, 200)
            vx = random.randint(-50, 50)
            vy = 0
            gobj = Ball(x, y, vx, vy)
            self.lge.addGObject(gobj, 1)

    def onMainUpdate(self, dt):
        # limite de ejecucion
        self.counter = self.counter - 1
        if(self.counter <= 0):
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

    def run(self):
        self.lge.run(self.fps)


class Ball(Canvas):

    def __init__(self, x, y, vx, vy):
        super().__init__((x, y), (20, 20))

        # acceso al motor de juegos
        self.lge = LittleGameEngine.getInstance()

        self.vx = vx
        self.vy = vy
        self.g = 240
        self.e = 0.4
        self.fill((0, 128, 0, 200))
        self.enableCollider(True)
        self.ground = self.lge.getGObject("ground")

    # @Override
    def onUpdate(self, dt):
        x, y = self.getPosition()

        x = x + self.vx * dt
        y = y + self.vy * dt

        if(x < 0):
            self.lge.delGObject(self)
            return

        self.vy = self.vy + self.g * dt
        self.setPosition(x, y)

    # @Override
    def onPostUpdate(self, dt):
        if(self.collidesWith(self.ground)):
            self.setPosition(self.getX(), self.ground.getY() - self.getHeight())
            self.vy = -self.vy * self.e
            if(abs(self.vy) < 50):
                self.vy = 0
                self.vx = 0
                self.g = 0


# -- show time
game = Bouncing(60)
cProfile.run("game.run()")

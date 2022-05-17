from lge.LittleGameEngine import LittleGameEngine
from lge.Canvas import Canvas

from Ball import Ball


class Pong():

    def __init__(self):
        # creamos el juego
        winSize = (640, 640)

        self.lge = LittleGameEngine(winSize, "Pong", (0, 0, 0))
        self.lge.setOnMainUpdate(self.onMainUpdate)
        # self.lge.showColliders((255, 0, 0))

        # cargamos los recursos que usaremos
        resourceDir = "../resources"

        self.lge.loadTTFFont("monospace.16", resourceDir + "/fonts/FreeMono.ttf", 16)

        # agregamos la barra de info
        infobar = Canvas((0, 0), (640, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # el campo de juego
        field = Canvas((24, 80), (592, 526), "field")
        field.fill((0, 0, 100))
        self.lge.addGObject(field, 0)

        # los bordes
        wall = Canvas((0, 76), (640, 4))
        wall.fill((255, 255, 255))
        wall.setTag("wall-horizontal")
        wall.enableCollider(True)
        self.lge.addGObject(wall, 1)

        wall = Canvas((0, 606), (640, 4))
        wall.fill((255, 255, 255))
        wall.setTag("wall-horizontal")
        wall.enableCollider(True)
        self.lge.addGObject(wall, 1)

        wall = Canvas((20, 80), (4, 526))
        wall.fill((255, 255, 255))
        wall.setTag("wall-vertical")
        wall.enableCollider(True)
        self.lge.addGObject(wall, 1)

        wall = Canvas((616, 80), (4, 526))
        wall.fill((255, 255, 255))
        wall.setTag("wall-vertical")
        wall.enableCollider(True)
        self.lge.addGObject(wall, 1)

        # los actores
        ball = Ball((320, 400), (8, 8), "ball")
        self.lge.addGObject(ball, 1)

        paddle = Canvas((90, 270), (8, 60), "user-paddle")
        paddle.fill((255, 255, 255))
        paddle.setTag("paddle")
        paddle.enableCollider(True)
        paddle.setBounds(field.getRectangle())
        self.lge.addGObject(paddle, 1)

        paddle = Canvas((540, 270), (8, 60), "system-paddle")
        paddle.fill((255, 255, 255))
        paddle.setTag("paddle")
        paddle.enableCollider(True)
        paddle.setBounds(field.getRectangle())
        self.lge.addGObject(paddle, 1)

        self.paddleSpeed = 240

    def onMainUpdate(self, dt):
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
        infobar.fill((80, 80, 80, 200))
        infobar.drawText(info, (50, 0), "monospace.16", (255, 255, 255))

        # user paddle
        userPaddle = self.lge.getGObject("user-paddle")
        speed = self.paddleSpeed * dt
        x = userPaddle.getX()
        y = userPaddle.getY()

        if (self.lge.keyPressed(self.lge.CONSTANTS.K_UP)):
            userPaddle.setPosition(x, y - speed)
        elif (self.lge.keyPressed(self.lge.CONSTANTS.K_DOWN)):
            userPaddle.setPosition(x, y + speed)

        # la pelota
        ball = self.lge.getGObject("ball")
        # bx = ball.getX()
        by = ball.getY()

        # system paddle
        systemPaddle = self.lge.getGObject("system-paddle")
        px = systemPaddle.getX()
        py = systemPaddle.getY()
        # pw = systemPaddle.getWidth()
        ph = systemPaddle.getHeight()

        if (py + ph / 2 < by):
            py = py + speed
        elif (py + ph / 2 > by):
            py = py - speed
        systemPaddle.setPosition(px, py)

    # main loop
    def run(self, fps):
        self.lge.run(fps)


# ----
game = Pong()
game.run(60)

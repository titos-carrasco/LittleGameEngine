from lge.LittleGameEngine import LittleGameEngine
from lge.Canvas import Canvas

from Ball import Ball


class Pong():
    def __init__(self):
        # creamos el juego
        win_size = (640, 640)

        self.lge = LittleGameEngine(win_size, "Pong", (0, 0, 0))
        self.lge.SetOnMainUpdate(self.OnMainUpdate)

        # cargamos los recursos que usaremos
        resource_dir = "../resources"

        self.lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)

        # agregamos la barra de info
        infobar = Canvas((0, 620), (640, 20), "infobar")
        self.lge.AddGObjectGUI(infobar)

        # el campo de juego
        field = Canvas((24, 34), (592, 526), "field")
        field.Fill((0, 0, 100))
        self.lge.AddGObject(field, 0)

        # los bordes
        wall = Canvas((0, 560),  (640, 4))
        wall.Fill((255, 255, 255))
        wall.SetTag("wall-horizontal")
        wall.UseColliders(True)
        self.lge.AddGObject(wall, 1)

        wall = Canvas((0, 30),  (640, 4))
        wall.Fill((255, 255, 255))
        wall.SetTag("wall-horizontal")
        wall.UseColliders(True)
        self.lge.AddGObject(wall, 1)

        wall = Canvas((20, 34),  (4, 526))
        wall.Fill((255, 255, 255))
        wall.SetTag("wall-vertical")
        wall.UseColliders(True)
        self.lge.AddGObject(wall, 1)

        wall = Canvas((616, 34),  (4, 526))
        wall.Fill((255, 255, 255))
        wall.SetTag("wall-vertical")
        wall.UseColliders(True)
        self.lge.AddGObject(wall, 1)

        # los actores
        ball = Ball((320, 400),  (8, 8), "ball")
        self.lge.AddGObject(ball, 1)

        paddle = Canvas((90, 270),  (8, 60), "user-paddle")
        paddle.Fill((255, 255, 255))
        paddle.SetTag("paddle")
        paddle.UseColliders(True)
        paddle.SetBounds(field.GetRectangle())
        self.lge.AddGObject(paddle, 1)

        paddle = Canvas((540, 270),  (8, 60), "system-paddle")
        paddle.Fill((255, 255, 255))
        paddle.SetTag("paddle")
        paddle.UseColliders(True)
        paddle.SetBounds(field.GetRectangle())
        self.lge.AddGObject(paddle, 1)

        self.paddle_speed = 240

    def OnMainUpdate(self, dt):
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
        infobar.Fill((80, 80, 80, 200))
        infobar.DrawText(info, (50, 0), "monospace.16", (255, 255, 255))

        # user paddle
        user_paddle = self.lge.GetGObject("user-paddle")
        speed = self.paddle_speed * dt
        x = user_paddle.GetX()
        y = user_paddle.GetY()

        if (self.lge.KeyPressed(self.lge.CONSTANTS.K_UP)):
            user_paddle.SetPosition(x, y + speed)
        elif (self.lge.KeyPressed(self.lge.CONSTANTS.K_DOWN)):
            user_paddle.SetPosition(x, y - speed)

        # la pelota
        ball = self.lge.GetGObject("ball")
        #bx = ball.GetX()
        by = ball.GetY()

        # system paddle
        system_paddle = self.lge.GetGObject("system-paddle")
        px = system_paddle.GetX()
        py = system_paddle.GetY()
        #pw = system_paddle.GetWidth()
        ph = system_paddle.GetHeight()

        if (py + ph / 2 < by):
            py = py + speed
        elif (py + ph / 2 > by):
            py = py - speed
        system_paddle.SetPosition(px, py)

    # main loop
    def Run(self):
        self.lge.Run(60)


# ----
game = Pong()
game.Run()

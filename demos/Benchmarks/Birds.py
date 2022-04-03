import cProfile
import random

from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle


class Birds():
    def __init__(self):
        # creamos el juego
        win_size = (800, 440)

        self.lge = LittleGameEngine(win_size, "Birds", (255, 255, 0))
        self.lge.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.lge.SetOnMainUpdate(self.MainUpdate)
        self.lge.ShowColliders((255, 0, 0))

        # cargamos los recursos que usaremos
        resource_dir = "../resources"

        self.lge.LoadImage("fondo", resource_dir + "/images/Backgrounds/FreeTileset/Fondo.png", win_size)
        self.lge.LoadImage("heroe", resource_dir + "/images/Swordsman/Idle/Idle_00*.png", 0.08)
        self.lge.LoadImage("bird", resource_dir + "/images/BlueBird/frame-*.png", 0.04)
        self.lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.AddGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 420), (800, 20), "infobar")
        self.lge.AddGObjectGUI(infobar)

        # agregamos al heroe
        heroe = Sprite("heroe", (226, 142))
        heroe.UseColliders(True)
        self.lge.AddGObject(heroe, 1)

        # agregamos pajaros
        ww, wh = self.lge.GetCameraSize()
        for i in range(500):
            x = random.random()*ww
            y = random.random()*(wh - 40)
            bird = Bird("bird", (x, y))
            bird.UseColliders(True)
            self.lge.AddGObject(bird, 1)

    def MainUpdate(self, dt):
        # abortamos con la tecla Escape
        if(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_ESCAPE)):
            self.lge.Quit()

        # mostramos info
        fps = self.lge.GetFPS()
        fps = "FPS: %07.2f" % fps

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

    # main loop
    def Run(self):
        self.lge.Run(60)


class Bird(Sprite):
    def __init__(self, inames, position):
        super().__init__(inames, position)

        # acceso al motor de juegos
        self.lge = LittleGameEngine.GetLGE()

        # sus atributos
        self.SetOnEvents(LittleGameEngine.E_ON_UPDATE)

    def OnUpdate(self, dt):
        self.NextShape(dt, 0.1)


# ----
bird = Birds()
cProfile.run("bird.Run()")

import cv2

from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.GameObject import GameObject
from lge.Rectangle import Rectangle

from Betty import Betty
from WebCam import WebCam


class MiJuego():
    # inicializamos el juego
    def __init__(self):
        # creamos el juego
        win_size = (640, 480)

        self.lge = LittleGameEngine(win_size, "MiJuego", (255, 255, 0))
        self.lge.ShowColliders((255, 0, 0))
        self.lge.SetOnMainUpdate(self.OnMainUpdate)

        # cargamos recursos globales
        resource_dir = "../resources"

        self.lge.LoadImage("fondo", resource_dir + "/images/Backgrounds/FreeTileset/Fondo.png")
        self.lge.LoadImage("betty_idle", resource_dir + "/images/Betty/idle-0*.png")
        self.lge.LoadImage("betty_left", resource_dir + "/images/Betty/left-0*.png")
        self.lge.LoadImage("betty_right", resource_dir + "/images/Betty/right-0*.png")
        self.lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.AddGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 460), (640, 20), "infobar")
        self.lge.AddGObjectGUI(infobar)

        # agregamos colisionadores para el suelo
        self.AddColliders()

        # agregamos los personajes
        betty = Betty(10, 300)
        self.lge.AddGObject(betty, 2)

        # agregamos la webcam
        webcam = WebCam()
        self.lge.AddGObject(webcam, 1)

        # configuramos la camara
        self.lge.SetCameraBounds(Rectangle((0, 0), (1920, 1056)))
        self.lge.SetCameraTarget(betty, True)

    def AddColliders(self):
        gobj = GameObject((0, 247), (510, 9))
        gobj.SetTag("suelo")
        gobj.UseColliders(True)
        self.lge.AddGObject(gobj, 2)

        gobj = GameObject((484, 340), (250, 9))
        gobj.SetTag("suelo")
        gobj.UseColliders(True)
        self.lge.AddGObject(gobj, 2)

        gobj = GameObject((507, 210), (266, 9))
        gobj.SetTag("muerte")
        gobj.UseColliders(True)
        self.lge.AddGObject(gobj, 2)

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
        infobar.Fill((20, 20, 20, 10))
        infobar.DrawText(info, (70, 0), "monospace.16", (0, 0, 0))

    # main loop
    def Run(self):
        self.lge.Run(60)


# -- show time
game = MiJuego()
game.Run()

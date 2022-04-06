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
        self.lge.showColliders((255, 0, 0))
        self.lge.setOnMainUpdate(self.onMainUpdate)

        # cargamos recursos globales
        resourceDir = "../resources"

        self.lge.loadImage("fondo", resourceDir + "/images/Backgrounds/FreeTileset/Fondo.png")
        self.lge.loadImage("betty_idle", resourceDir + "/images/Betty/idle-0*.png")
        self.lge.loadImage("betty_left", resourceDir + "/images/Betty/left-0*.png")
        self.lge.loadImage("betty_right", resourceDir + "/images/Betty/right-0*.png")
        self.lge.loadTTFFont("monospace.16", resourceDir + "/fonts/FreeMono.ttf", 16)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.addGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 460), (640, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # agregamos colisionadores para el suelo
        self.addColliders()

        # agregamos los personajes
        betty = Betty(10, 300)
        self.lge.addGObject(betty, 2)

        # agregamos la webcam
        webcam = WebCam()
        self.lge.addGObject(webcam, 1)

        # configuramos la camara
        self.lge.setCameraBounds(Rectangle((0, 0), (1920, 1056)))
        self.lge.setCameraTarget(betty, True)

    def addColliders(self):
        gobj = GameObject((0, 247), (510, 9))
        gobj.setTag("suelo")
        gobj.useColliders(True)
        self.lge.addGObject(gobj, 2)

        gobj = GameObject((484, 340), (250, 9))
        gobj.setTag("suelo")
        gobj.useColliders(True)
        self.lge.addGObject(gobj, 2)

        gobj = GameObject((507, 210), (266, 9))
        gobj.setTag("muerte")
        gobj.useColliders(True)
        self.lge.addGObject(gobj, 2)

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
        infobar.fill((20, 20, 20, 10))
        infobar.drawText(info, (70, 0), "monospace.16", (0, 0, 0))

    # main loop
    def run(self):
        self.lge.run(60)


# -- show time
game = MiJuego()
game.run()

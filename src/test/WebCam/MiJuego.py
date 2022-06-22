import cv2

from lge.Canvas import Canvas
from lge.GameObject import GameObject
from lge.LittleGameEngine import LittleGameEngine
from lge.Rectangle import Rectangle
from lge.Sprite import Sprite

from Betty import Betty
from WebCam import WebCam


class MiJuego():

    # inicializamos el juego
    def __init__(self):
        # creamos el juego
        win_size = (640, 480)

        self.lge = LittleGameEngine(win_size, "MiJuego", (0, 0, 0))
        self.lge.onMainUpdate = self.onMainUpdate
        self.lge.showColliders((255, 0, 0))

        # cargamos recursos globales
        resourceDir = "../resources"

        self.lge.imageManager.loadImage("fondo", resourceDir + "/images/Backgrounds/FreeTileset/Fondo.png")
        self.lge.imageManager.loadImage("betty_idle", resourceDir + "/images/Betty/idle-0*.png")
        self.lge.imageManager.loadImage("betty_left", resourceDir + "/images/Betty/left-0*.png")
        self.lge.imageManager.loadImage("betty_right", resourceDir + "/images/Betty/right-0*.png")
        self.lge.fontManager.loadTTFont("monospace", resourceDir + "/fonts/FreeMono.ttf", (False, False), 16)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.addGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 0), (640, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # agregamos colisionadores para el suelo
        self.addColliders()

        # agregamos los personajes
        betty = Betty(10, 700)
        betty.setBounds(Rectangle((0, 0), (1920, 1056)))
        self.lge.addGObject(betty, 2)

        # agregamos la webcam
        webcam = WebCam()
        self.lge.addGObject(webcam, 1)

        # configuramos la camara
        self.lge.setCameraBounds(Rectangle((0, 0), (1920, 1056)))
        self.lge.setCameraTarget(betty, True)

    def addColliders(self):
        gobj = GameObject((0, 800), (510, 9))
        gobj.setTag("suelo")
        gobj.enableCollider(True)
        self.lge.addGObject(gobj, 2)

        gobj = GameObject((484, 707), (250, 9))
        gobj.setTag("suelo")
        gobj.enableCollider(True)
        self.lge.addGObject(gobj, 2)

        gobj = GameObject((507, 837), (266, 9))
        gobj.setTag("muerte")
        gobj.enableCollider(True)
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
        infobar.drawText(info, (70, 0), "monospace", (0, 0, 0))

    # main loop
    def run(self, fps):
        self.lge.run(fps)


# -- show time
game = MiJuego()
game.run(60)
print("Eso es todo!!!")

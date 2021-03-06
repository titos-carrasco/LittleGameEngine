from lge.Canvas import Canvas
from lge.LittleGameEngine import LittleGameEngine
from lge.Rectangle import Rectangle
from lge.Sprite import Sprite

from BlockHorizontal import BlockHorizontal
from Ninja import Ninja


class Platform():

    def __init__(self):
        # creamos el juego
        win_size = (800, 600)

        self.lge = LittleGameEngine(win_size, "Vulcano", (0, 0, 0))
        self.lge.onMainUpdate = self.onMainUpdate

        # cargamos algunos recursos
        resourceDir = "../resources"

        self.lge.imageManager.loadImages("fondo", resourceDir + "/images/Platform/Platform.png")
        self.lge.imageManager.loadImages("roca", resourceDir + "/images/Volcano_Pack_1.1/volcano_pack_alt_39.png")
        self.lge.imageManager.loadImages("ninja", resourceDir + "/images/Swordsman/Idle/Idle_0*.png", 0.16)
        self.lge.fontManager.loadTTFont("monospace", resourceDir + "/fonts/FreeMono.ttf", (False, False), 16)
        self.lge.fontManager.loadTTFont("cool", resourceDir + "/fonts/backlash.ttf", (False, False), 30)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.addGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 0), (800, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # agregamos el ninja
        ninja = Ninja((340, 180))
        self.lge.addGObjectGUI(ninja)

        # agregamos el bloque que se mueve vertical
        bloque = BlockHorizontal(13 * 64, 3 * 64)
        self.lge.addGObject(bloque, 1)

        # agregamos el mensaje
        pressbar = Canvas((200, 260), (400, 30), "pressbar")
        pressbar.drawText("Presiona la Barra Espaciadora", (0, 0), "cool", (255, 255, 255))
        self.lge.addGObjectGUI(pressbar)

        # configuramos la camara
        self.lge.setCameraBounds(Rectangle((0, 0), (2560, 704)))
        self.direction = 1

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
        infobar.drawText(info, (150, 2), "monospace", (255, 255, 255))

        # velocity = pixeles por segundo
        velocity = 240
        pixels = velocity * dt

        # movemos la camara
        x, y = self.lge.getCameraPosition()

        if(self.direction == 1 and x > 1700):
            self.direction = -1
        elif(self.direction == -1 and x <= 0):
            self.direction = 1

        x = x + pixels * self.direction
        self.lge.setCameraPosition(x, y)

        # verificamos si se ha presionada la barra espaciadora
        if(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_SPACE)):
            self.direction = 1
            self.lge.setCameraPosition(0, 0)

    # main loop
    def run(self, fps):
        self.lge.run(fps)


# -- show time
game = Platform()
game.run(60)
print("Eso es todo!!!")

from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle

from BlockHorizontal import BlockHorizontal
from Ninja import Ninja


class Platform():
    def __init__(self):
        # creamos el juego
        win_size = (800, 600)

        self.lge = LittleGameEngine(win_size, "Vulcano", (255, 255, 0))
        self.lge.SetOnMainUpdate(self.OnMainUpdate)

        # cargamos algunos recursos
        resource_dir = "../resources"

        self.lge.LoadImage("fondo", resource_dir + "/images/Platform/Platform.png")
        self.lge.LoadImage("roca", resource_dir + "/images/Volcano_Pack_1.1/volcano_pack_alt_39.png")
        self.lge.LoadImage("ninja", resource_dir + "/images/Swordsman/Idle/Idle_0*.png", 0.16)
        self.lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)
        self.lge.LoadTTFFont("cool.30", resource_dir + "/fonts/backlash.ttf", 30)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.AddGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 580), (800, 20), "infobar")
        self.lge.AddGObjectGUI(infobar)

        # agregamos el ninja
        ninja = Ninja((340, 300))
        self.lge.AddGObjectGUI(ninja)

        # agregamos el bloque que se mueve vertical
        bloque = BlockHorizontal(13*64, 1*64)
        self.lge.AddGObject(bloque, 1)

        # agregamos el mensaje
        pressbar = Canvas((200, 260), (400, 30), "pressbar")
        pressbar.DrawText("Presiona la Barra Espaciadora", (0, 0), "cool.30", (255, 255, 255))
        self.lge.AddGObjectGUI(pressbar)

        # configuramos la camara
        self.lge.SetCameraBounds(Rectangle((0, 0), (2560, 704)))
        self.direction = 1

    def OnMainUpdate(self, dt):
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
        infobar.Fill((80, 80, 80, 200))
        infobar.DrawText(info, (150, 2), "monospace.16", (255, 255, 255))

        # velocity = pixeles por segundo
        velocity = 240
        pixels = velocity*dt
        if(pixels < 1):
            pixels = 1

        # movemos la camara
        x, y = self.lge.GetCameraPosition()

        if(self.direction == 1 and x > 1700):
            self.direction = -1
        elif(self.direction == -1 and x <= 0):
            self.direction = 1

        x = x + pixels*self.direction
        self.lge.SetCameraPosition(x, y)

        # verificamos si se ha presionada la barra espaciadora
        if(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_SPACE)):
            self.direction = 1
            self.lge.SetCameraPosition(0, 0)

    # main loop

    def Run(self):
        self.lge.Run(60)


# -- show time
game = Platform()
game.Run()

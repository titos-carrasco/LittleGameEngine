from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas


class TheWorld():
    def __init__(self):
        # creamos el juego
        winSize = (800, 440)

        self.lge = LittleGameEngine(winSize, "The World", (255, 255, 0))
        self.lge.setOnMainUpdate(self.OnMainUpdate)

        # cargamos los recursos que usaremos
        resourceDir = "../resources"

        self.lge.loadImage("fondo", resourceDir + "/images/Backgrounds/FreeTileset/Fondo.png", winSize)
        self.lge.loadImage("heroe", resourceDir + "/images/Swordsman/Idle/Idle_000.png", 0.08)
        self.lge.loadImage("mute", resourceDir + "/images/icons/sound-*.png")
        self.lge.loadTTFFont("backlash.40", resourceDir + "/fonts/backlash.ttf", 40)
        self.lge.loadTTFFont("monospace.16", resourceDir + "/fonts/FreeMono.ttf", 16)
        self.lge.loadSound("fondo", resourceDir + "/sounds/happy-and-sad.wav")

        # activamos la musica de fondo
        self.lge.playSound("fondo", True, 50)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.addGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 420), (800, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # agregamos el icono del sonido
        mute = Sprite("mute", (8, 423), "mute")
        mute.setShape("mute", 1)
        self.lge.addGObjectGUI(mute)

        # agregamos al heroe
        heroe = Sprite("heroe", (226, 142), "Heroe")
        self.lge.addGObject(heroe, 1)

        # agregamos un texto con transparencia
        canvas = Canvas((200, 110), (400, 200))
        canvas.drawText("Little Game Engine", (30, 90), "backlash.40", (20, 20, 20))
        self.lge.addGObjectGUI(canvas)

    def OnMainUpdate(self, dt):
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
        infobar.drawText(info, (140, 0), "monospace.16", (0, 0, 0))

        # mute on/off
        mute = self.lge.getGObject("mute")
        r = mute.getRectangle()
        if(self.lge.getMouseClicked(0) and r.contains(mx, my)):
            idx = mute.getCurrentIdx()
            if(idx == 1):
                self.lge.setSoundVolume("fondo", 0)
            else:
                self.lge.setSoundVolume("fondo", 50)
            mute.nextShape()

    # main loop
    def run(self):
        self.lge.run(60)


# -- show time
game = TheWorld()
game.run()

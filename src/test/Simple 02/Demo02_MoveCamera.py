from lge.Canvas import Canvas
from lge.LittleGameEngine import LittleGameEngine
from lge.MouseClick import MouseClick
from lge.Rectangle import Rectangle
from lge.Sprite import Sprite


class MoveCamera():

    def __init__(self):
        # creamos el juego
        winSize = (640, 480)

        self.lge = LittleGameEngine(winSize, "Move Camera", (0, 0, 0))
        self.lge.onMainUpdate = self.onMainUpdate

        # cargamos los recursos que usaremos
        resourceDir = "../resources"

        self.lge.imageManager.loadImages("fondo", resourceDir + "/images/Backgrounds/FreeTileset/Fondo.png")
        self.lge.imageManager.loadImages("heroe", resourceDir + "/images/Swordsman/Idle/Idle_000.png", 0.16)
        self.lge.imageManager.loadImages("mute", resourceDir + "/images/icons/sound-*.png")
        self.lge.fontManager.loadTTFont("monospace", resourceDir + "/fonts/FreeMono.ttf", (False, False), 16)
        self.lge.soundManager.loadSound("fondo", resourceDir + "/sounds/happy-and-sad.wav")

        # activamos la musica de fondo
        self.lge.soundManager.playSound("fondo", True, 50)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.addGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 0), (640, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # agregamos el icono del sonido
        mute = Sprite("mute", (8, 3), "mute")
        mute.setImage("mute", 1)
        self.lge.addGObjectGUI(mute)
        self.isMute = False

        # agregamos al heroe
        heroe = Sprite("heroe", (550, 626), "Heroe")
        self.lge.addGObject(heroe, 1)

        # configuramos la camara
        self.lge.setCameraBounds(Rectangle((0, 0), (1920, 1056)))

        # posicionamos la camara
        x, y = heroe.getPosition()
        w, h = heroe.getSize()
        cw, ch = self.lge.getCameraSize()
        self.lge.setCameraPosition(x + w / 2 - cw / 2, y + h / 2 - ch / 2)

        # para manejar el clic del mouse
        self.leftMouseButton = MouseClick()

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
        infobar.drawText(info, (50, 0), "monospace", (0, 0, 0))

        # mute on/off
        if(self.leftMouseButton.isClicked(mb1, mx, my)):
            mute = self.lge.getGObject("mute")
            r = mute.getRectangle()
            if(r.contains(mx, my)):
                if(self.isMute):
                    self.lge.soundManager.setSoundVolume("fondo", 50)
                else:
                    self.lge.soundManager.setSoundVolume("fondo", 0)
                self.isMute = not self.isMute
                mute.nextImage()

        # velocity = pixeles por segundo
        velocity = 240
        pixels = velocity * dt

        # la posiciona actual de la camara
        x, y = self.lge.getCameraPosition()

        # cambiamos sus coordenadas segun la tecla presionada
        if(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
            x = x + pixels
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
            x = x - pixels
        if(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_UP)):
            y = y - pixels
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
            y = y + pixels

        # posicionamos la camara
        self.lge.setCameraPosition(x, y)

    # main loop
    def run(self, fps):
        self.lge.run(fps)


# --- show time
game = MoveCamera()
game.run(60)
print("Eso es todo!!!")

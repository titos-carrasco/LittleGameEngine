import random

from lge.Canvas import Canvas
from lge.LittleGameEngine import LittleGameEngine
from lge.MouseClick import MouseClick
from lge.Rectangle import Rectangle
from lge.Sprite import Sprite


class Colliders():

    def __init__(self):
        # creamos el juego
        winSize = (640, 480)

        self.lge = LittleGameEngine(winSize, "Colliders", (0, 0, 0))
        self.lge.onMainUpdate = self.onMainUpdate
        self.lge.showColliders((255, 0, 0))

        # cargamos los recursos que usaremos
        resourceDir = "../resources"

        self.lge.imageManager.loadImages("fondo", resourceDir + "/images/Backgrounds/FreeTileset/Fondo.png")
        self.lge.imageManager.loadImages("heroe_idle_right", resourceDir + "/images/Swordsman/Idle/Idle_0*.png", 0.16)
        self.lge.imageManager.loadImages("heroe_idle_left", resourceDir + "/images/Swordsman/Idle/Idle_0*.png", 0.16, (True, False))
        self.lge.imageManager.loadImages("heroe_run_right", resourceDir + "/images/Swordsman/Run/Run_0*.png", 0.16)
        self.lge.imageManager.loadImages("heroe_run_left", resourceDir + "/images/Swordsman/Run/Run_0*.png", 0.16, (True, False))
        self.lge.imageManager.loadImages("ninja", resourceDir + "/images/Swordsman/Idle/Idle_000.png", 0.16)
        self.lge.imageManager.loadImages("mute", resourceDir + "/images/icons/sound-*.png")
        self.lge.fontManager.loadTTFont("monospace", resourceDir + "/fonts/FreeMono.ttf", (False, False), 16)
        self.lge.soundManager.loadSound("fondo", resourceDir + "/sounds/happy-and-sad.wav")
        self.lge.soundManager.loadSound("aves", resourceDir + "/sounds/bird-thrush-nightingale.wav")
        self.lge.soundManager.loadSound("poing", resourceDir + "/sounds/cartoon-poing.wav")

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

        # agregamos un ninja
        ninja = Sprite("ninja", (350, 720), "ninja")
        ninja.setCollider([
            Rectangle((36, 8), (36, 36)),
            Rectangle((28, 44), (44, 36))
            ])
        ninja.enableCollider(True)
        self.lge.addGObject(ninja, 1)

        # agregamos al heroe
        heroe = MiHeroe()
        self.lge.addGObject(heroe, 1)

        # configuramos la camara
        self.lge.setCameraBounds(Rectangle((0, 0), (1920, 1056)))

        # establecemos que la camara siga al heroe
        self.lge.setCameraTarget(heroe, False)

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

        # de manera aleatorio activamos sonido de aves
        n = random.randint(0, 1000)
        if (n < 3):
            self.lge.soundManager.playSound("aves", False, 100)

    # main loop
    def run(self, fps):
        self.lge.run(fps)


class MiHeroe(Sprite):

    def __init__(self):
        # agregamos el heroe con diferentes imagenes
        super().__init__("heroe_idle_left", (550, 626), "Heroe")

        # acceso al motor de juegos
        self.lge = LittleGameEngine.getInstance()

        # sus atributos
        self.enableCollider(True)
        self.state = -1
        self.setBounds(Rectangle((0, 0), (1920, 1056)))
        self.ninja = self.lge.getGObject("ninja")

    # @Override
    def onUpdate(self, dt):
        # velocity = pixeles por segundo
        velocity = 240
        pixels = velocity * dt

        # la posiciona actual del heroe
        x, y = self.getPosition()
        self.last = x, y

        # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
        if (self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
            x = x + pixels
            if (self.state != 2):
                self.setImage("heroe_run_right")
                self.state = 2
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
            x = x - pixels
            if (self.state != -2):
                self.setImage("heroe_run_left")
                self.state = -2
        elif(self.state == 2):
            if (self.state != 1):
                self.setImage("heroe_idle_right")
                self.state = 1
        elif(self.state == -2):
            if (self.state != -1):
                self.setImage("heroe_idle_left")
                self.state = -1

        if (self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_UP)):
            y = y - pixels
        elif (self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
            y = y + pixels

        # siguiente imagen de la secuencia
        self.nextImage(dt, 0.050)

        # lo posicionamos asegurando que se encuentre dentro del mundo definido
        self.setPosition(x, y)

    # @Override
    def onPostUpdate(self, dt):
        if(self.collidesWith(self.ninja)):
            x, y = self.last
            self.lge.soundManager.playSound("poing", False, 10)
            self.setPosition(x, y)


# --- show time
game = Colliders()
game.run(60)
print("Eso es todo!!!")

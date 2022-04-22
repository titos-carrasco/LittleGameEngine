from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle
from lge.MouseClick import MouseClick


class Moveplayer():

    def __init__(self):
        # creamos el juego
        winSize = (640, 480)

        self.lge = LittleGameEngine(winSize, "Move player", (255, 255, 0))
        self.lge.setOnMainUpdate(self.onMainUpdate)

        # cargamos los recursos que usaremos
        resourceDir = "../resources"

        self.lge.loadImage("fondo", resourceDir + "/images/Backgrounds/FreeTileset/Fondo.png")
        self.lge.loadImage("heroe_right", resourceDir + "/images/Swordsman/Idle/Idle_000.png", 0.16)
        self.lge.loadImage("heroe_left", resourceDir + "/images/Swordsman/Idle/Idle_000.png", 0.16, (True, False))
        self.lge.loadImage("mute", resourceDir + "/images/icons/sound-*.png")
        self.lge.loadTTFFont("monospace.16", resourceDir + "/fonts/FreeMono.ttf", 16)
        self.lge.loadSound("fondo", resourceDir + "/sounds/happy-and-sad.wav")

        # activamos la musica de fondo
        self.lge.playSound("fondo", True, 50)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.addGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 0), (640, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # agregamos el icono del sonido
        mute = Sprite("mute", (8, 3), "mute")
        mute.setShape("mute", 1)
        self.lge.addGObjectGUI(mute)

        # agregamos al heroe
        heroe = MiHeroe()
        self.lge.addGObject(heroe, 1)

        # configuramos la camara
        self.lge.setCameraBounds(Rectangle((0, 0), (1920, 1056)))

        # establecemos que la camara siga al heroe
        self.lge.setCameraTarget(heroe, True)

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
        infobar.drawText(info, (50, 0), "monospace.16", (0, 0, 0))

        # mute on/off
        if(self.leftMouseButton.isClicked(mb1, mx, my)):
            mute = self.lge.getGObject("mute")
            r = mute.getRectangle()
            if(r.contains(mx, my)):
                idx = mute.getCurrentIdx()
                if(idx == 1):
                    self.lge.setSoundVolume("fondo", 0)
                else:
                    self.lge.setSoundVolume("fondo", 50)
                mute.nextShape()

    # main loop
    def run(self):
        self.lge.run(60)


class MiHeroe(Sprite):

    def __init__(self):
        super().__init__(["heroe_right", "heroe_left"], (550, 626), "Heroe")

        # acceso al motor de juegos
        self.lge = LittleGameEngine.getInstance()

        # sus atributos
        self.setOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.setShape("heroe_right")
        self.setBounds(Rectangle((0, 0), (1920, 1056)))

    def onUpdate(self, dt):
        # velocity = pixeles por segundo
        velocity = 240
        pixels = velocity * dt
        if(pixels < 1):
            pixels = 1

        # la posiciona actual del heroe
        x, y = self.getPosition()

        # cambiamos sus coordenadas y orientacion segun la tecla presionada
        if(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
            x = x + pixels
            self.setShape("heroe_right")
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
            x = x - pixels
            self.setShape("heroe_left")

        if(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_UP)):
            y = y - pixels
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
            y = y + pixels

        # lo posicionamos asegurando que se encuentre dentro de los limites
        self.setPosition(x, y)


# --- show time
game = Moveplayer()
game.run()

from lge.LittleGameEngine import LittleGameEngine
from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.Canvas import Canvas

from Betty import Betty
from Zombie import Zombie


class MiJuego():

    def __init__(self):
        # creamos el juego
        winSize = (608, 736)

        self.lge = LittleGameEngine(winSize, "Betty", (255, 255, 0))
        self.lge.setOnMainUpdate(self.onMainUpdate)
        # self.lge.ShowColliders((255, 0, 0))

        # cargamos algunos recursos
        resourceDir = "../resources"

        self.lge.loadImage("fondo", resourceDir + "/images/Betty/Fondo.png")
        self.lge.loadImage("betty_idle", resourceDir + "/images/Betty/idle-0*.png")
        self.lge.loadImage("betty_down", resourceDir + "/images/Betty/down-0*.png")
        self.lge.loadImage("betty_up", resourceDir + "/images/Betty/up-0*.png")
        self.lge.loadImage("betty_left", resourceDir + "/images/Betty/left-0*.png")
        self.lge.loadImage("betty_right", resourceDir + "/images/Betty/right-0*.png")
        self.lge.loadImage("zombie", resourceDir + "/images/Kenny/Zombie/zombie_walk*.png")
        self.lge.loadTTFFont("monospace.16", resourceDir + "/fonts/FreeMono.ttf", 16)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.addGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 0), (640, 20), "infobar")
        self.lge.addGObjectGUI(infobar)

        # cargamos el mapa en memoria
        mapa = []
        fname = resourceDir + "/images/Betty/Mapa.txt"
        f = open(fname)
        for line in f:
            line = [int(c) for c in line if c == '0' or c == '1']
            mapa.append(line)
        f.close()

        # agregamos a Betty
        betty = Betty("Betty", winSize)
        betty.setPosition(32 * 9, 32 * 9)
        self.lge.addGObject(betty, 1)

        # agregamos 3 zombies
        for i in range(3):
            zombie = Zombie("Zombie-%03d" % i, winSize)
            zombie.setPosition(32 + 32 * 4 + 32 * (i * 4), 32 * 21)
            self.lge.addGObject(zombie, 1)

        # agregamos los muros para las colisiones (segun el mapa)
        y = 1
        for row in mapa:
            x = 0
            for v in row:
                if(v == 1):
                    muro = GameObject((x * 32, y * 32), (32, 32))
                    muro.useColliders(True)
                    muro.setTag("muro")
                    self.lge.addGObject(muro, 1)
                x = x + 1
            y = y + 1

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
        infobar.fill((80, 80, 80, 80))
        infobar.drawText(info, (50, 0), "monospace.16", (255, 255, 255))

    # main loop
    def run(self):
        self.lge.run(60)


# -- show time
game = MiJuego()
game.run()

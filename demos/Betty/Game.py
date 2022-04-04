from lge.LittleGameEngine import LittleGameEngine
from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.Canvas import Canvas

from Betty import Betty
from Zombie import Zombie


class MiJuego():
    def __init__(self):
        # creamos el juego
        win_size = (608, 736)

        self.lge = LittleGameEngine(win_size, "Betty", (255, 255, 0))
        self.lge.SetOnMainUpdate(self.OnMainUpdate)
        #self.lge.ShowColliders((255, 0, 0))

        # cargamos algunos recursos
        resource_dir = "../resources"

        self.lge.LoadImage("fondo", resource_dir + "/images/Betty/Fondo.png")
        self.lge.LoadImage("betty_idle", resource_dir + "/images/Betty/idle-0*.png")
        self.lge.LoadImage("betty_down", resource_dir + "/images/Betty/down-0*.png")
        self.lge.LoadImage("betty_up", resource_dir + "/images/Betty/up-0*.png")
        self.lge.LoadImage("betty_left", resource_dir + "/images/Betty/left-0*.png")
        self.lge.LoadImage("betty_right", resource_dir + "/images/Betty/right-0*.png")
        self.lge.LoadImage("zombie", resource_dir + "/images/Kenny/Zombie/zombie_walk*.png")
        self.lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.AddGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 714), (640, 20), "infobar")
        self.lge.AddGObjectGUI(infobar)

        # cargamos el mapa en memoria
        mapa = []
        fname = resource_dir + "/images/Betty/Mapa.txt"
        f = open(fname)
        for line in f:
            line = [int(c) for c in line if c == '0' or c == '1']
            mapa.append(line)
        f.close()

        # agregamos a Betty
        betty = Betty("Betty", win_size)
        betty.SetPosition(32*9, 32*13)
        self.lge.AddGObject(betty, 1)

        # agregamos 3 zombies
        for i in range(3):
            zombie = Zombie("Zombie-%03d" % i, win_size)
            zombie.SetPosition(32 + 32*4 + 32*(i*4), 32*1)
            self.lge.AddGObject(zombie, 1)

        # agregamos los muros para las colisiones (segun el mapa)
        y = 21
        for row in mapa:
            x = 0
            for v in row:
                if(v == 1):
                    muro = GameObject((x*32, y*32), (32, 32))
                    muro.UseColliders(True)
                    muro.SetTag("muro")
                    self.lge.AddGObject(muro, 1)
                x = x + 1
            y = y - 1

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
        infobar.Fill((80, 80, 80, 80))
        infobar.DrawText(info, (50, 0), "monospace.16", (255, 255, 255))

    # main loop
    def Run(self):
        self.lge.Run(60)


# -- show time
game = MiJuego()
game.Run()

from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas


class TheWorld():
    def __init__(self):
        # creamos el juego
        win_size = (800, 440)

        self.lge = LittleGameEngine(win_size, "The World", (255, 255, 0))
        self.lge.SetOnMainUpdate(self.MainUpdate)

        # cargamos los recursos que usaremos
        resource_dir = "../resources"

        self.lge.LoadImage("fondo", resource_dir + "/images/Backgrounds/FreeTileset/Fondo.png", win_size)
        self.lge.LoadImage("heroe", resource_dir + "/images/Swordsman/Idle/Idle_000.png", 0.08)
        self.lge.LoadImage("mute", resource_dir + "/images/icons/sound-*.png")
        self.lge.LoadTTFFont("backlash.40", resource_dir + "/fonts/backlash.ttf", 40)
        self.lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)
        self.lge.LoadSound("fondo", resource_dir + "/sounds/happy-and-sad.wav")

        # activamos la musica de fondo
        self.lge.PlaySound("fondo", True, 50)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.AddGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 420), (800, 20), "infobar")
        self.lge.AddGObjectGUI(infobar)

        # agregamos el icono del sonido
        mute = Sprite("mute", (8, 423), "mute")
        mute.SetShape("mute", 1)
        self.lge.AddGObjectGUI(mute)

        # agregamos al heroe
        heroe = Sprite("heroe", (226, 142), "Heroe")
        self.lge.AddGObject(heroe, 1)

        # agregamos un texto con transparencia
        canvas = Canvas((200, 110), (400, 200))
        canvas.DrawText("Little Game Engine", (30, 90), "backlash.40", (20, 20, 20))
        self.lge.AddGObjectGUI(canvas)

    def MainUpdate(self, dt):
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
        infobar.Fill((20, 20, 20, 10))
        infobar.DrawText(info, (140, 0), "monospace.16", (0, 0, 0))

        # mute on/off
        mute = self.lge.GetGObject("mute")
        r = mute.GetRectangle()
        if(self.lge.GetMouseClicked(0) and r.Contains(mx, my)):
            idx = mute.GetCurrentIdx()
            if(idx == 1):
                self.lge.SetSoundVolume("fondo", 0)
            else:
                self.lge.SetSoundVolume("fondo", 50)
            mute.NextShape()

    # main loop
    def Run(self):
        self.lge.Run(60)


# -- show time
game = TheWorld()
game.Run()

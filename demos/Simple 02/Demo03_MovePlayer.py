from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle


class MovePlayer():
    def __init__(self):
        # creamos el juego
        win_size = (640, 480)

        self.lge = LittleGameEngine(win_size, "Move Player", (255, 255, 0))
        self.lge.SetOnMainUpdate(self.OnMainUpdate)

        # cargamos los recursos que usaremos
        resource_dir = "../resources"

        self.lge.LoadImage("fondo", resource_dir + "/images/Backgrounds/FreeTileset/Fondo.png")
        self.lge.LoadImage("heroe_right", resource_dir + "/images/Swordsman/Idle/Idle_000.png", 0.16)
        self.lge.LoadImage("heroe_left", resource_dir + "/images/Swordsman/Idle/Idle_000.png", 0.16, (True, False))
        self.lge.LoadImage("mute", resource_dir + "/images/icons/sound-*.png")
        self.lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)
        self.lge.LoadSound("fondo", resource_dir + "/sounds/happy-and-sad.wav")

        # activamos la musica de fondo
        self.lge.PlaySound("fondo", True, 50)

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        self.lge.AddGObject(fondo, 0)

        # agregamos la barra de info
        infobar = Canvas((0, 460), (640, 20), "infobar")
        self.lge.AddGObjectGUI(infobar)

        # agregamos el icono del sonido
        mute = Sprite("mute", (8, 463), "mute")
        mute.SetShape("mute", 1)
        self.lge.AddGObjectGUI(mute)

        # agregamos al heroe
        heroe = MiHeroe()
        self.lge.AddGObject(heroe, 1)

        # configuramos la camara
        self.lge.SetCameraBounds(Rectangle((0, 0), (1920, 1056)))

        # establecemos que la camara siga al heroe
        self.lge.SetCameraTarget(heroe, True)

    def OnMainUpdate(self, dt):
        # abortamos con la tecla Escape
        if(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_ESCAPE)):
            self.lge.Quit()

        # mostramos info
        mx, my = self.lge.GetMousePosition()
        mb1, mb2, mb3 = self.lge.GetMouseButtons()

        info = "FPS: %07.2f - gObjs: %03d - Mouse: (%3d,%3d) (%d,%d,%d)" % (
            self.lge.GetFPS(),
            self.lge.GetCountGObjects(), mx, my,
            mb1, mb2, mb3
        )
        infobar = self.lge.GetGObject("infobar")
        infobar.Fill((20, 20, 20, 10))
        infobar.DrawText(info, (50, 0), "monospace.16", (0, 0, 0))

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


class MiHeroe(Sprite):
    def __init__(self):
        super().__init__(["heroe_right", "heroe_left"], (550, 346), "Heroe")

        # acceso al motor de juegos
        self.lge = self.GetLGE()

        # sus atributos
        self.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.SetShape("heroe_right")
        self.SetBounds(Rectangle((0, 0), (1920, 1056)))

    def OnUpdate(self, dt):
        # velocity = pixeles por segundo
        velocity = 240
        pixels = velocity*dt
        if(pixels < 1):
            pixels = 1

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # cambiamos sus coordenadas y orientacion segun la tecla presionada
        if(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
            x = x + pixels
            self.SetShape("heroe_right")
        elif(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
            x = x - pixels
            self.SetShape("heroe_left")

        if(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_UP)):
            y = y + pixels
        elif(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
            y = y - pixels

        # lo posicionamos asegurando que se encuentre dentro de los limites
        self.SetPosition(x, y)


# --- show time
game = MovePlayer()
game.Run()

from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle


class MiJuego():
    def __init__(self):
        # creamos el juego
        Engine.Init((640, 480), "Move Player")
        Engine.SetOnUpdate(self.MainUpdate)

        # activamos la musica de fondo
        Engine.LoadSound("fondo", "../sounds/happy-and-sad.wav")
        Engine.SetSoundVolume("fondo", 0.5)
        Engine.PlaySound("fondo", loop=-1)

        # cargamos los recursos que usaremos
        Engine.LoadImage("fondo", "../images/Backgrounds/FreeTileset/Fondo.png")
        Engine.LoadImage("heroe_right", "../images/Swordsman/Idle/Idle_000.png", 0.16)
        Engine.LoadImage("heroe_left", "../images/Swordsman/Idle/Idle_000.png", 0.16, (True, False))
        Engine.LoadImage("mute", "../images/icons/sound-*.png")
        Engine.LoadTTFFont("monospace", 16, "../fonts/FreeMono.ttf")

        # agregamos el fondo
        fondo = Sprite("fondo", (0, 0))
        Engine.AddGObject(fondo, 0)

        # agregamos un Sprite
        heroe = MiHeroe()

        # agregamos la barra de info
        infobar = Canvas((0, 460), (640, 20), "infobar")
        Engine.AddGObjectGUI(infobar)

        mute = Sprite("mute", (8, 463), "mute")
        mute.SetShape("mute", 1)
        Engine.AddGObjectGUI(mute)

        # configuramos la camara
        camera = Engine.GetCamera()
        camera.SetBounds(Rectangle((0, 0), (1920, 1056)))

        # establecemos que la camara siga al heroe
        Engine.SetCameraTarget(heroe, True)

    def MainUpdate(self, dt):
        # abortamos con la tecla Escape
        if(Engine.KeyUp(Engine.CONSTANTS.K_ESCAPE)):
            Engine.Quit()

        # mostramos info
        fps = Engine.GetFPS()
        fps = "FPS: %07.2f" % fps

        ngobjs = len(Engine.GetGObject("*"))
        ngobjs = "gObjs: %03d" % ngobjs

        mx, my = Engine.GetMousePosition()
        mb1, mb2, mb3 = Engine.GetMouseButtons()
        minfo = "Mouse: (%3d,%3d) (%d,%d,%d)" % (mx, my, mb1, mb2, mb3)

        infobar = Engine.GetGObject("infobar")
        infobar.Fill((0, 0, 0, 20))
        infobar.DrawText(fps + " - " + ngobjs + " - " + minfo, (70, 0), "monospace", (0, 0, 0))

        mp = Engine.GetMousePressed(1)
        if(mp):
            mx, my = mp

            mute = Engine.GetGObject("mute")
            iname, idx = mute.GetCurrentShape()
            if(idx):
                Engine.SetSoundVolume("fondo", 0)
                mute.SetShape(iname, 0)
            else:
                Engine.SetSoundVolume("fondo", 0.5)
                mute.SetShape(iname, 1)

    # main loop
    def Run(self):
        Engine.Run(60)


class MiHeroe(Sprite):
    def __init__(self):
        super().__init__(["heroe_right", "heroe_left"], (550, 346), "Heroe")
        self.SetShape("heroe_right", 0)
        self.heading = 1
        Engine.AddGObject(self, 1)

    def OnUpdate(self, dt):
        # velocity = pixeles por segundo
        velocity = 240
        pixels = velocity*dt

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # cambiamos sus coordenadas y orientacion segun la tecla presionada
        if(Engine.KeyPressed(Engine.CONSTANTS.K_RIGHT)):
            x = x + pixels
            if(self.heading != 1):
                self.SetShape("heroe_right", 0)
                self.heading = 1
        elif(Engine.KeyPressed(Engine.CONSTANTS.K_LEFT)):
            x = x - pixels
            if(self.heading != -1):
                self.SetShape("heroe_left", 0)
                self.heading = -1
        if(Engine.KeyPressed(Engine.CONSTANTS.K_UP)):
            y = y + pixels
        elif(Engine.KeyPressed(Engine.CONSTANTS.K_DOWN)):
            y = y - pixels

        # lo posicionamos asegurando que se encuentre dentro de los limites
        camera = Engine.GetCamera()
        bounds = camera.GetBounds()
        self.SetPosition(x, y, bounds)


# --- show time
game = MiJuego()
game.Run()

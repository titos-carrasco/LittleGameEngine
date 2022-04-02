from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle


def main():
    global lge

    # creamos el juego
    win_size = (640, 480)
    lge = LittleGameEngine(win_size, "Move Player", 0xFFFF00)
    lge.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
    lge.SetOnMainUpdate(MainUpdate)

    # cargamos los recursos que usaremos
    resource_dir = "../resources"

    lge.LoadImage("fondo", resource_dir + "/images/Backgrounds/FreeTileset/Fondo.png")
    lge.LoadImage("heroe_right", resource_dir + "/images/Swordsman/Idle/Idle_000.png", 0.16)
    lge.LoadImage("heroe_left", resource_dir + "/images/Swordsman/Idle/Idle_000.png", 0.16, (True, False))
    lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)
    lge.LoadSound("fondo", resource_dir + "/sounds/happy-and-sad.wav")

    # activamos la musica de fondo
    lge.PlaySound("fondo", loop=-1)

    # agregamos el fondo
    fondo = Sprite("fondo", (0, 0), "fondo")
    lge.AddGObject(fondo, 0)

    # agregamos la barra de info
    infobar = Canvas((0, 460), (640, 20), "infobar")
    lge.AddGObjectGUI(infobar)

    # agregamos al heroe
    heroe = Sprite(["heroe_right", "heroe_left"], (550, 346), "Heroe")
    heroe.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
    heroe.SetShape("heroe_right", 0)
    heroe.heading = 1
    heroe.SetBounds(Rectangle((0, 0), (1920, 1056)))
    heroe.UseColliders(True)
    heroe.OnUpdate = HeroeUpdate
    lge.AddGObject(heroe, 1)

    # configuramos la camara
    lge.SetCameraBounds(Rectangle((0, 0), (1920, 1056)))

    # establecemos que la camara siga al heroe
    lge.SetCameraTarget(heroe, True)

    # main loop
    lge.Run(60)


def MainUpdate(dt):
    global lge

    # abortamos con la tecla Escape
    if(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_ESCAPE)):
        lge.Quit()

    # mostramos info
    fps = lge.GetFPS()
    fps = "FPS: %07.2f" % fps

    mx, my = lge.GetMousePosition()
    mb1, mb2, mb3 = lge.GetMouseButtons()

    info = "FPS: %07.2f - gObjs: %03d - Mouse: (%3d,%3d) (%d,%d,%d)" % (
        lge.GetFPS(),
        lge.GetCountGObjects(), mx, my,
        mb1, mb2, mb3
    )
    infobar = lge.GetGObject("infobar")
    infobar.Fill((20, 20, 20, 10))
    infobar.DrawText(info, (50, 0), "monospace.16", (0, 0, 0))


def HeroeUpdate(dt):
    global lge

    # el heroe
    heroe = lge.GetGObject("Heroe")

    # velocity = pixeles por segundo
    velocity = 240
    pixels = velocity*dt

    # la posiciona actual del heroe
    x, y = heroe.GetPosition()

    # cambiamos sus coordenadas y orientacion segun la tecla presionada
    if(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
        x = x + pixels
    elif(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
        x = x - pixels
    if(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_UP)):
        y = y + pixels
    elif(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
        y = y - pixels

    # lo posicionamos
    heroe.SetPosition(x, y)


# --- show time
main()

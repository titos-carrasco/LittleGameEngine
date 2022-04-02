from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle


def main():
    global lge

    # creamos el juego
    win_size = (640, 480)
    lge = LittleGameEngine(win_size, "Move Camera", 0xFFFF00)
    lge.ShowColliders((255, 0, 0))
    lge.SetOnMainUpdate(MainUpdate)

    # cargamos los recursos que usaremos
    resource_dir = "../resources"

    lge.LoadImage("fondo", resource_dir + "/images/Backgrounds/FreeTileset/Fondo.png")
    lge.LoadImage("heroe", resource_dir + "/images/Swordsman/Idle/Idle_0*.png", 0.16)
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
    heroe = Sprite("heroe", (550, 346), "Heroe")
    heroe.UseColliders(True)
    lge.AddGObject(heroe, 1)

    # configuramos la camara
    lge.SetCameraBounds(Rectangle((0, 0), (1920, 1056)))

    # posicionamos la camara
    x, y = heroe.GetPosition()
    w, h = heroe.GetSize()
    cw, ch = lge.GetCameraSize()
    lge.SetCameraPosition(x + w / 2 - cw / 2, y + h / 2 - ch / 2)

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

    # velocity = pixeles por segundo
    velocity = 240
    pixels = velocity*dt

    # la posiciona actual de la camara
    x, y = lge.GetCameraPosition()

    # cambiamos sus coordenadas segun la tecla presionada
    if(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
        x = x + pixels
    elif(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
        x = x - pixels
    if(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_UP)):
        y = y + pixels
    elif(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
        y = y - pixels

    # posicionamos la camara
    lge.SetCameraPosition(x, y)


# --- show time
main()

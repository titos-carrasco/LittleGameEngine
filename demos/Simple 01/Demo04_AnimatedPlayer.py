from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle


def main():
    # creamos el juego
    win_size = (640, 480)
    lge = LittleGameEngine(win_size, "Animated Player", (255, 255, 0))
    lge.SetOnMainUpdate(OnMainUpdate)

    # cargamos los recursos que usaremos
    resource_dir = "../resources"

    lge.LoadImage("fondo", resource_dir + "/images/Backgrounds/FreeTileset/Fondo.png")
    lge.LoadImage("heroe_idle_right", resource_dir + "/images/Swordsman/Idle/Idle_0*.png", 0.16)
    lge.LoadImage("heroe_idle_left", resource_dir + "/images/Swordsman/Idle/Idle_0*.png", 0.16, (True, False))
    lge.LoadImage("heroe_run_right", resource_dir + "/images/Swordsman/Run/Run_0*.png", 0.16)
    lge.LoadImage("heroe_run_left", resource_dir + "/images/Swordsman/Run/Run_0*.png", 0.16, (True, False))
    lge.LoadTTFFont("monospace.16", resource_dir + "/fonts/FreeMono.ttf", 16)
    lge.LoadSound("fondo", resource_dir + "/sounds/happy-and-sad.wav")

    # activamos la musica de fondo
    lge.PlaySound("fondo", True, 50)

    # agregamos el fondo
    fondo = Sprite("fondo", (0, 0))
    lge.AddGObject(fondo, 0)

    # agregamos la barra de info
    infobar = Canvas((0, 460), (640, 20), "infobar")
    lge.AddGObjectGUI(infobar)

    # agregamos al heroe
    heroe = Sprite(["heroe_idle_right", "heroe_idle_left", "heroe_run_right", "heroe_run_left"], (550, 346), "Heroe")
    heroe.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
    heroe.SetShape("heroe_idle_right")
    heroe.SetBounds(Rectangle((0, 0), (1920, 1056)))
    heroe.UseColliders(True)
    heroe.OnUpdate = HeroeUpdate
    heroe.state = 1
    lge.AddGObject(heroe, 1)

    # configuramos la camara
    lge.SetCameraBounds(Rectangle((0, 0), (1920, 1056)))

    # establecemos que la camara siga al heroe
    lge.SetCameraTarget(heroe, False)

    # main loop
    lge.Run(60)


def OnMainUpdate(dt):
    # acceso al motor de juegos
    lge = LittleGameEngine.GetLGE()

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
    # acceso al motor de juegos
    lge = LittleGameEngine.GetLGE()

    # el heroe
    heroe = lge.GetGObject("Heroe")

    # velocity = pixeles por segundo
    velocity = 240
    pixels = velocity * dt
    if(pixels < 1):
        pixels = 1

    # la posiciona actual del heroe
    x, y = heroe.GetPosition()

    # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
    if (lge.KeyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
        x = x + pixels
        if (heroe.state != 2):
            heroe.SetShape("heroe_run_right")
            heroe.state = 2
    elif (lge.KeyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
        x = x - pixels
        if (heroe.state != -2):
            heroe.SetShape("heroe_run_left")
            heroe.state = -2
    elif (heroe.state == 2):
        if (heroe.state != 1):
            heroe.SetShape("heroe_idle_right")
            heroe.state = 1
    elif (heroe.state == -2):
        if (heroe.state != -1):
            heroe.SetShape("heroe_idle_left")
            heroe.state = -1

    if(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_UP)):
        y = y + pixels
    elif(lge.KeyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
        y = y - pixels

    # siguiente imagen de la secuencia
    heroe.NextShape(dt, 0.050)

    # lo posicionamos
    heroe.SetPosition(x, y)


# --- show time
main()

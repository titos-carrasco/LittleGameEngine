from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle


def main():
    # creamos el juego
    winSize = (640, 480)
    lge = LittleGameEngine(winSize, "Animated player", (255, 255, 0))
    lge.setOnMainUpdate(onMainUpdate)

    # cargamos los recursos que usaremos
    resourceDir = "../resources"

    lge.loadImage("fondo", resourceDir + "/images/Backgrounds/FreeTileset/Fondo.png")
    lge.loadImage("heroe_idle_right", resourceDir + "/images/Swordsman/Idle/Idle_0*.png", 0.16)
    lge.loadImage("heroe_idle_left", resourceDir + "/images/Swordsman/Idle/Idle_0*.png", 0.16, (True, False))
    lge.loadImage("heroe_run_right", resourceDir + "/images/Swordsman/Run/Run_0*.png", 0.16)
    lge.loadImage("heroe_run_left", resourceDir + "/images/Swordsman/Run/Run_0*.png", 0.16, (True, False))
    lge.loadTTFFont("monospace.16", resourceDir + "/fonts/FreeMono.ttf", 16)
    lge.loadSound("fondo", resourceDir + "/sounds/happy-and-sad.wav")

    # activamos la musica de fondo
    lge.playSound("fondo", True, 50)

    # agregamos el fondo
    fondo = Sprite("fondo", (0, 0))
    lge.addGObject(fondo, 0)

    # agregamos la barra de info
    infobar = Canvas((0, 0), (640, 20), "infobar")
    lge.addGObjectGUI(infobar)

    # agregamos al heroe
    heroe = Sprite(["heroe_idle_right", "heroe_idle_left", "heroe_run_right", "heroe_run_left"], (550, 626), "Heroe")
    heroe.setOnEvents(LittleGameEngine.E_ON_UPDATE)
    heroe.setShape("heroe_idle_right")
    heroe.setBounds(Rectangle((0, 0), (1920, 1056)))
    heroe.useColliders(True)
    heroe.onUpdate = HeroeUpdate
    heroe.state = 1
    lge.addGObject(heroe, 1)

    # configuramos la camara
    lge.setCameraBounds(Rectangle((0, 0), (1920, 1056)))

    # establecemos que la camara siga al heroe
    lge.setCameraTarget(heroe, False)

    # main loop
    lge.run(60)


def onMainUpdate(dt):
    # acceso al motor de juegos
    lge = LittleGameEngine.getInstance()

    # abortamos con la tecla Escape
    if(lge.keyPressed(LittleGameEngine.CONSTANTS.K_ESCAPE)):
        lge.quit()

    # mostramos info
    mx, my = lge.getMousePosition()
    mb1, mb2, mb3 = lge.getMouseButtons()

    info = "FPS: %07.2f - gObjs: %03d - Mouse: (%3d,%3d) (%d,%d,%d)" % (
        lge.getFPS(),
        lge.getCountGObjects(), mx, my,
        mb1, mb2, mb3
    )
    infobar = lge.getGObject("infobar")
    infobar.fill((20, 20, 20, 10))
    infobar.drawText(info, (50, 0), "monospace.16", (0, 0, 0))


def HeroeUpdate(dt):
    # acceso al motor de juegos
    lge = LittleGameEngine.getInstance()

    # el heroe
    heroe = lge.getGObject("Heroe")

    # velocity = pixeles por segundo
    velocity = 240
    pixels = velocity * dt
    if(pixels < 1):
        pixels = 1

    # la posiciona actual del heroe
    x, y = heroe.getPosition()

    # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
    if (lge.keyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
        x = x + pixels
        if (heroe.state != 2):
            heroe.setShape("heroe_run_right")
            heroe.state = 2
    elif (lge.keyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
        x = x - pixels
        if (heroe.state != -2):
            heroe.setShape("heroe_run_left")
            heroe.state = -2
    elif (heroe.state == 2):
        if (heroe.state != 1):
            heroe.setShape("heroe_idle_right")
            heroe.state = 1
    elif (heroe.state == -2):
        if (heroe.state != -1):
            heroe.setShape("heroe_idle_left")
            heroe.state = -1

    if(lge.keyPressed(LittleGameEngine.CONSTANTS.K_UP)):
        y = y - pixels
    elif(lge.keyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
        y = y + pixels

    # siguiente imagen de la secuencia
    heroe.nextShape(dt, 0.050)

    # lo posicionamos
    heroe.setPosition(x, y)


# --- show time
main()

from lge.Canvas import Canvas
from lge.LittleGameEngine import LittleGameEngine
from lge.Rectangle import Rectangle
from lge.Sprite import Sprite


def main():
    # creamos el juego
    winSize = (640, 480)
    lge = LittleGameEngine(winSize, "Move Camera", (0, 0, 0))
    lge.onMainUpdate = onMainUpdate

    # cargamos los recursos que usaremos
    resourceDir = "../resources"

    lge.imageManager.loadImages("fondo", resourceDir + "/images/Backgrounds/FreeTileset/Fondo.png")
    lge.imageManager.loadImages("heroe", resourceDir + "/images/Swordsman/Idle/Idle_0*.png", 0.16)
    lge.fontManager.loadTTFont("monospace", resourceDir + "/fonts/FreeMono.ttf", (False, False), 16)
    lge.soundManager.loadSound("fondo", resourceDir + "/sounds/happy-and-sad.wav")

    # activamos la musica de fondo
    lge.soundManager.playSound("fondo", True, 50)

    # agregamos el fondo
    fondo = Sprite("fondo", (0, 0))
    lge.addGObject(fondo, 0)

    # agregamos la barra de info
    infobar = Canvas((0, 0), (640, 20), "infobar")
    lge.addGObjectGUI(infobar)

    # agregamos al heroe
    heroe = Sprite("heroe", (550, 626))
    lge.addGObject(heroe, 1)

    # configuramos la camara
    lge.setCameraBounds(Rectangle((0, 0), (1920, 1056)))

    # posicionamos la camara
    x, y = heroe.getPosition()
    w, h = heroe.getSize()
    cw, ch = lge.getCameraSize()
    lge.setCameraPosition(x + w / 2 - cw / 2, y + h / 2 - ch / 2)

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
    infobar.drawText(info, (50, 0), "monospace", (0, 0, 0))

    # velocity = pixeles por segundo
    velocity = 240
    pixels = velocity * dt

    # la posiciona actual de la camara
    x, y = lge.getCameraPosition()

    # cambiamos sus coordenadas segun la tecla presionada
    if(lge.keyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
        x = x + pixels
    elif(lge.keyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
        x = x - pixels
    if(lge.keyPressed(LittleGameEngine.CONSTANTS.K_UP)):
        y = y - pixels
    elif(lge.keyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
        y = y + pixels

    # posicionamos la camara
    lge.setCameraPosition(x, y)


# --- show time
main()
print("Eso es todo!!!")

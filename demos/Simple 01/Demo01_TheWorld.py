from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas

# creamos el juego
winSize = (800, 440)
lge = LittleGameEngine(winSize, "The World", (255, 255, 0))

# cargamos los recursos que usaremos
resourceDir = "../resources"

lge.loadImage("fondo", resourceDir + "/images/Backgrounds/FreeTileset/Fondo.png", winSize)
lge.loadImage("heroe", resourceDir + "/images/Swordsman/Idle/Idle_0*.png", 0.08)
lge.loadTTFFont("backlash.40", resourceDir + "/fonts/backlash.ttf", 40)
lge.loadSound("fondo", resourceDir + "/sounds/happy-and-sad.wav")

# activamos la musica de fondo
lge.playSound("fondo", True, 50)

# agregamos el fondo
fondo = Sprite("fondo", (0, 0))
lge.addGObject(fondo, 0)

# agregamos al heroe
heroe = Sprite("heroe", (226, 254))
lge.addGObject(heroe, 1)

# agregamos un texto con transparencia
canvas = Canvas((200, 110), (400, 200))
canvas.drawText("Little Game Engine", (30, 90), "backlash.40", (20, 20, 20))
lge.addGObjectGUI(canvas)

# main loop
lge.run(60)

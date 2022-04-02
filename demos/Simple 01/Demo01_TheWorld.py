from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite
from lge.Canvas import Canvas

# creamos el juego
win_size = (800, 440)
lge = LittleGameEngine(win_size, "The World", 0xFFFF00)

# cargamos los recursos que usaremos
resource_dir = "../resources"

lge.LoadImage("fondo", resource_dir + "/images/Backgrounds/FreeTileset/Fondo.png", win_size)
lge.LoadImage("heroe", resource_dir + "/images/Swordsman/Idle/Idle_0*.png", 0.08)
lge.LoadTTFFont("backlash.40", resource_dir + "/fonts/backlash.ttf", 40)
lge.LoadSound("fondo", resource_dir + "/sounds/happy-and-sad.wav")

# activamos la musica de fondo
lge.PlaySound("fondo", loop=-1)

# agregamos el fondo
fondo = Sprite("fondo", (0, 0), "fondo")
lge.AddGObject(fondo, 0)

# agregamos al heroe
heroe = Sprite("heroe", (226, 142), "Heroe")
heroe.UseColliders(True)
lge.AddGObject(heroe, 1)

# agregamos un texto con transparencia
canvas = Canvas((200, 110), (400, 200))
canvas.DrawText("Little Game Engine", (30, 90), "backlash.40", (20, 20, 20))
lge.AddGObjectGUI(canvas)

# un poco mas avanzado
lge.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
heroe.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
heroe.OnUpdate = lambda dt: heroe.NextShape(dt, 0.060)

# main loop
lge.Run(60)

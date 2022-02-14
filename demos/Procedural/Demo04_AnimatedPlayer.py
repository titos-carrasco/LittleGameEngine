from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.LGE import LGE


def HeroeControl( dt ):
    global engine

    # el heroe
    heroe = engine.GetGObjectByName( "Heroe" )

   # moveremos al heroe "ppm" pixeles por minuto
    ppm = 240
    pixels = (ppm*dt)/1000

    # la posiciona actual del heroe
    x, y = heroe.GetPosition()

    # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
    moving = False
    idx, name = heroe.GetCurrentShape()
    if( engine.IsKeyPressed( LGE.CONSTANTS.K_RIGHT ) ):
        x = x + pixels
        if( heroe.heading != 1 ):
            heroe.Flip( True, False )
            heroe.heading = 1
        if( name != "run" ):
            heroe.SetShape( 0, "run" )
        moving = True
    elif( engine.IsKeyPressed( LGE.CONSTANTS.K_LEFT ) ):
        x = x - pixels
        if( heroe.heading != -1 ):
            heroe.Flip( True, False )
            heroe.heading = -1
        if( name != "run" ):
            heroe.SetShape( 0, "run" )
        moving = True

    if( engine.IsKeyPressed( LGE.CONSTANTS.K_DOWN ) ):
        y = y - pixels
        moving = True
    elif( engine.IsKeyPressed( LGE.CONSTANTS.K_UP ) ):
        y = y + pixels
        moving = True

    if( not moving and name != "idle" ):
            heroe.SetShape( 0, "idle" )

    # siguiente imagen de la secuencia
    heroe.NextShape( dt, 50 )

    # lo posicionamos asegurando que se encuentre dentro del mundo definido
    pos = engine.KeepInsideWorld( heroe, (x,y) )
    heroe.SetPosition( pos )


def MainControl( dt ):
    global engine

    # abortamos con la tecla Escape
    if( engine.IsKeyPressed( LGE.CONSTANTS.K_ESCAPE ) ):
        engine.Quit()

    # mostramos los FPS actuales
    fps = engine.GetFPS()
    fps = "FPS: %07.2f" % fps
    engine.AddText( fps, (0,460), "consolas" )


def main():
    global engine

    # creamos el juego
    engine = LGE( (1920,1056), (640,480), "Animated Player", (0xFF,0xFF,0xFF) )
    engine.SetFPS( 60 )
    engine.SetMainTask( MainControl )

    # cargamos un font
    engine.LoadSysFont( "consolas", 20 )

    # agregamos el fondo
    fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0) )
    engine.AddGObject( fondo, 0 )

    # agregamos el heroe con diferentes imagenes
    fnames = {
        "idle": "../images/Swordsman/Idle/Idle_0*.png",
        "run" : "../images/Swordsman/Run/Run_0*.png"
    }
    heroe = Sprite( fnames, (550,346), "Heroe" )
    heroe.ScalePercent( 0.16 )
    heroe.SetShape( 0, "idle" )
    heroe.OnUpdate = HeroeControl
    heroe.heading = 1
    engine.AddGObject( heroe, 1 )

    # establecemos que la camara siga al heroe en su origen
    engine.SetCamTarget( heroe, False )

    # agregamos una música de fondo
    engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
    engine.PlaySound( "fondo", loop=-1 )

    # main loop
    engine.Run()


#--- show time
main()

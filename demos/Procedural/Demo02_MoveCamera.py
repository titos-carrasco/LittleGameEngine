from lge.Sprite import Sprite
from lge.LGE import LGE


def MainControl( dt ):
    global engine

    # abortamos con la tecla Escape
    if( engine.IsKeyPressed( LGE.CONSTANTS.K_ESCAPE ) ):
        engine.Quit()

    # mostramos los FPS actuales
    fps = engine.GetFPS()
    fps = "FPS: %07.2f" % fps
    engine.AddText( fps, (0,460), "consolas", 20 )

    # moveremos la camara "ppm" pixeles por minuto
    ppm = 240
    pixels = (ppm*dt)/1000

    # la posiciona actual de la camara
    x, y = engine.GetCamPosition()

    # cambiamos sus coordenadas segun la tecla presionada
    if( engine.IsKeyPressed( LGE.CONSTANTS.K_RIGHT ) ):
        x = x + pixels
    elif( engine.IsKeyPressed( LGE.CONSTANTS.K_LEFT ) ):
        x = x - pixels
    if( engine.IsKeyPressed( LGE.CONSTANTS.K_DOWN ) ):
        y = y - pixels
    elif( engine.IsKeyPressed( LGE.CONSTANTS.K_UP ) ):
        y = y + pixels

    # posicionamos la camara
    engine.SetCamPosition( (x,y) )


def main():
    global engine

    # creamos el juego
    engine = LGE( (1920,1056), (640,480), "Move Camera", (0xFF,0xFF,0xFF) )
    engine.SetFPS( 60 )
    engine.SetMainTask( MainControl )

    # cargamos un font
    engine.LoadSysFont( "consolas", 20 )

    # agregamos el fondo
    fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0) )
    engine.AddGObject( fondo, 0 )

    # agregamos un Sprite
    heroe = Sprite( "../images/Swordsman/Idle/Idle_000.png", (550,346), "Heroe" )
    heroe.ScalePercent( 0.16 )
    engine.AddGObject( heroe, 1 )

    # posicionamos la camara
    x, y = heroe.GetPosition()
    w, h = heroe.GetSize()
    engine.SetCamPosition( (x+w/2,y+h/2) )

    # main loop
    engine.Run()


#--- show time
main()

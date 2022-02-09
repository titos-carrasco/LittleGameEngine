from lge.Sprite import Sprite
from lge.LGE import LGE


def CamControl( dt ):
    global engine

    # abortamos con la tecla Escape
    if( engine.IsKeyDown( LGE.CONSTANTS.K_ESCAPE ) ):
        engine.Quit()

    # moveremos la camara "ppm" pixeles por minuto
    ppm = 240
    pixels = (ppm*dt)/1000

    # info de la camara
    x, y = engine.GetCamPosition()

    # cambiamos sus coordenadas segun la tecla presionada
    if( engine.IsKeyDown( LGE.CONSTANTS.K_RIGHT ) ):
        x = x + pixels
    elif( engine.IsKeyDown( LGE.CONSTANTS.K_LEFT ) ):
        x = x - pixels
    if( engine.IsKeyDown( LGE.CONSTANTS.K_DOWN ) ):
        y = y - pixels
    elif( engine.IsKeyDown( LGE.CONSTANTS.K_UP ) ):
        y = y + pixels

    # la reposicionamos
    engine.SetCamPosition( (x,y) )


def main():
    global engine

    # creamos el juego
    engine = LGE( (1920,1056), (640,480), "Move Camera", (0xFF,0xFF,0xFF), CamControl )
    engine.SetFPS( 60 )

    # agregamos el fondo
    fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0), 0 )
    engine.AddGObject( fondo )

    # agregamos un Sprite
    heroe = Sprite( "../images/Swordsman/Idle/Idle_000.png", (550,346), 1, "Heroe" )
    heroe.ScalePercent( 0.16 )
    engine.AddGObject( heroe )

    # posicionamos la camara
    engine.SetCamPosition( (280,200) )

    # main loop
    engine.Run()


#--- show time
main()

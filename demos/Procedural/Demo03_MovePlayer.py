from lge.Sprite import Sprite
from lge.LGE import LGE


def HeroeControl( dt ):
    global engine

    # el heroe
    heroe = engine.GetGObject( "Heroe" )

    # abortamos con la tecla Escape
    if( engine.IsKeyPressed( LGE.CONSTANTS.K_ESCAPE ) ):
        return engine.Quit()

   # moveremos al heroe "ppm" pixeles por minuto
    ppm = 240
    pixels = (ppm*dt)/1000

    # la posiciona actual del heroe
    x, y = heroe.GetPosition()

    # cambiamos sus coordenadas y orientacion segun la tecla presionada
    if( engine.IsKeyPressed( LGE.CONSTANTS.K_RIGHT ) ):
        x = x + pixels
        if( heroe.heading != 1 ):
            heroe.Flip( True, False )
            heroe.heading = 1
    elif( engine.IsKeyPressed( LGE.CONSTANTS.K_LEFT ) ):
        x = x - pixels
        if( heroe.heading != -1 ):
            heroe.Flip( True, False )
            heroe.heading = -1
    if( engine.IsKeyPressed( LGE.CONSTANTS.K_DOWN ) ):
        y = y - pixels
    elif( engine.IsKeyPressed( LGE.CONSTANTS.K_UP ) ):
        y = y + pixels

    # lo posicionamos asegurando que se encuentre dentro del mundo definido
    pos = engine.KeepInsideWorld( heroe, (x,y) )
    heroe.SetPosition( pos )


def main():
    global engine

    # creamos el juego
    engine = LGE( (1920,1056), (640,480), "Move Player", (0xFF,0xFF,0xFF) )
    engine.SetFPS( 60 )

    # agregamos el fondo
    fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0) )
    engine.AddGObject( fondo, 0 )

    # agregamos un Sprite
    heroe = Sprite( "../images/Swordsman/Idle/Idle_000.png", (550,346), "Heroe" )
    heroe.ScalePercent( 0.16 )
    heroe.OnUpdate = HeroeControl
    heroe.heading = 1
    engine.AddGObject( heroe, 1 )

    # establecemos que la camara siga al centro del heroe
    engine.SetCamTarget( heroe, True )

    # main loop
    engine.Run()


#--- show time
main()

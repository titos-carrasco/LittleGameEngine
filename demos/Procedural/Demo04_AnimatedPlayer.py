from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.LGE import LGE


def HeroeControl( dt ):
    global engine, heroe, point

    # abortamos con la tecla Escape
    if( engine.IsKeyDown( LGE.CONSTANTS.K_ESCAPE ) ):
        return engine.Quit()

   # moveremos al heroe "ppm" pixeles por minuto
    ppm = 240
    pixels = (ppm*dt)/1000

    # la posiciona actual del heroe
    x, y = heroe.GetPosition()

    # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
    moving = False
    idx, name = heroe.GetCurrentShape()
    if( engine.IsKeyDown( LGE.CONSTANTS.K_RIGHT ) ):
        x = x + pixels
        if( heroe.heading != 1 ):
            heroe.Flip( True, False )
            heroe.heading = 1
        if( name != "run" ):
            heroe.SetShape( 0, "run" )
        moving = True
    elif( engine.IsKeyDown( LGE.CONSTANTS.K_LEFT ) ):
        x = x - pixels
        if( heroe.heading != -1 ):
            heroe.Flip( True, False )
            heroe.heading = -1
        if( name != "run" ):
            heroe.SetShape( 0, "run" )
        moving = True

    if( engine.IsKeyDown( LGE.CONSTANTS.K_DOWN ) ):
        y = y - pixels
        moving = True
    elif( engine.IsKeyDown( LGE.CONSTANTS.K_UP ) ):
        y = y + pixels
        moving = True

    if( not moving and name != "idle" ):
            heroe.SetShape( 0, "idle" )

    # siguiente imagen de la secuencia
    t = heroe.elapsed + dt
    if( t >= 50 ):
        heroe.NextShape()
        t = 0
    heroe.elapsed = t

    # lo posicionamos asegurando que se encuentre dentro del mundo definido
    pos = engine.KeepInsideWorld( heroe, (x,y) )
    heroe.SetPosition( pos )
    point.SetPosition( pos )


def main():
    global engine, heroe, point

    # creamos el juego
    engine = LGE( (1920,1056), (640,480), "Animated Player", (0xFF,0xFF,0xFF) )
    engine.SetFPS( 60 )

    # agregamos el fondo
    fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0), 0 )
    engine.AddGObject( fondo )

    # agregamos el heroe con diferentes imagenes
    fnames = {
        "idle": "../images/Swordsman/Idle/Idle_0*.png",
        "run" : "../images/Swordsman/Run/Run_0*.png"
    }
    heroe = Sprite( fnames, (550,346), 1, "Heroe" )
    heroe.ScalePercent( 0.16 )
    heroe.SetShape( 0, "idle" )
    heroe.OnUpdate = HeroeControl
    heroe.heading = 1
    heroe.elapsed = 0
    engine.AddGObject( heroe )

    # establecemos que la camara siga al heroe a traves de un punto
    point = GameObject( (550,346), (0,0), 0 )
    engine.SetCamTarget( point )

    # main loop
    engine.Run()


#--- show time
main()

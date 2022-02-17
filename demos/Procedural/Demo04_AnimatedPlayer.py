from lge.Sprite import Sprite
from lge.Text import Text
from lge.Engine import Engine


def HeroeControl( dt ):
    # el heroe
    heroe = Engine.GetGObject( "Heroe" )

   # moveremos al heroe "ppm" pixeles por minuto
    ppm = 240
    pixels = (ppm*dt)/1000

    # la posiciona actual del heroe
    x, y = heroe.GetPosition()

    # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
    moving = False
    idx, name = heroe.GetCurrentShape()
    if( Engine.IsKeyPressed( Engine.CONSTANTS.K_RIGHT ) ):
        x = x + pixels
        if( heroe.heading != 1 ):
            heroe.Flip( True, False )
            heroe.heading = 1
        if( name != "run" ):
            heroe.SetShape( 0, "run" )
        moving = True
    elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_LEFT ) ):
        x = x - pixels
        if( heroe.heading != -1 ):
            heroe.Flip( True, False )
            heroe.heading = -1
        if( name != "run" ):
            heroe.SetShape( 0, "run" )
        moving = True

    if( Engine.IsKeyPressed( Engine.CONSTANTS.K_DOWN ) ):
        y = y - pixels
        moving = True
    elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_UP ) ):
        y = y + pixels
        moving = True

    if( not moving and name != "idle" ):
            heroe.SetShape( 0, "idle" )

    # siguiente imagen de la secuencia
    heroe.NextShape( dt, 50 )

    # lo posicionamos asegurando que se encuentre dentro del mundo definido
    pos = Engine.KeepInsideWorld( heroe, (x,y) )
    heroe.SetPosition( pos )


def MainControl( dt ):
    # abortamos con la tecla Escape
    if( Engine.IsKeyPressed( Engine.CONSTANTS.K_ESCAPE ) ):
        Engine.Quit()

    # mostramos los FPS actuales y datos del mouse
    fps = Engine.GetFPS()
    fps = "FPS: %07.2f" % fps

    mx, my = Engine.GetMousePos()
    mb1, mb2, mb3 = Engine.GetMousePressed()
    minfo = "Mouse: (%4d,%4d) (%d,%d,%d)" % ( mx, my, mb1, mb2, mb3 )

    info = Engine.GetGObject( "infobar" )
    info.SetText( fps + " "*15 + minfo )


def main():
    # creamos el juego
    Engine.Init( (1920,1056), (640,480), "Animated Player", (0xFF,0xFF,0xFF) )
    Engine.SetMainTask( MainControl )

    # activamos la musica de fondo
    Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
    Engine.PlaySound( "fondo", loop=-1 )

    # cargamos los recursos que usaremos
    Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
    Engine.LoadImage( "idle", "../images/Swordsman/Idle/Idle_0*.png" )
    Engine.LoadImage( "run", "../images/Swordsman/Run/Run_0*.png" )
    Engine.LoadTTFFont( "monospace", 20, "../fonts/FreeMono.ttf" )

    # agregamos el fondo
    fondo = Sprite( "fondo", (0,0) )
    Engine.AddGObject( fondo, 0 )

    heroe = Sprite( ["idle","run"], (550,346), "Heroe" )
    heroe.Scale( 0.16 )
    heroe.SetShape( 0, "idle" )
    heroe.OnUpdate = HeroeControl
    heroe.heading = 1
    Engine.AddGObject( heroe, 1 )

    # agregamos la barra de info
    infobar = Text( None, (0,460), "monospace", (0,0,0), None, "infobar" )
    Engine.AddGObject( infobar, Engine.CAM_LAYER )

    # establecemos que la camara siga al heroe en su origen
    Engine.SetCamTarget( heroe, False )

    # main loop
    Engine.Run( 60 )


#--- show time
main()

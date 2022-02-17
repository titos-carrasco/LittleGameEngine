from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Text import Text
from lge.Rect import Rect


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

    # moveremos la camara "ppm" pixeles por minuto
    ppm = 240
    pixels = (ppm*dt)/1000

    # la posiciona actual de la camara
    x, y = Engine.GetCamPosition()

    # cambiamos sus coordenadas segun la tecla presionada
    if( Engine.IsKeyPressed( Engine.CONSTANTS.K_RIGHT ) ):
        x = x + pixels
    elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_LEFT ) ):
        x = x - pixels
    if( Engine.IsKeyPressed( Engine.CONSTANTS.K_DOWN ) ):
        y = y - pixels
    elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_UP ) ):
        y = y + pixels

    # posicionamos la camara
    Engine.SetCamPosition( (x,y) )


def main():
    # creamos el juego
    Engine.Init( (640,480), "Move Camera" )
    Engine.SetWorldBounds( Rect( (0,0), (1920,1056) ) )
    Engine.SetMainTask( MainControl )

    # activamos la musica de fondo
    Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
    Engine.PlaySound( "fondo", loop=-1 )

    # cargamos los recursos que usaremos
    Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
    Engine.LoadImage( "heroe", "../images/Swordsman/Idle/Idle_000.png" )
    Engine.LoadTTFFont( "monospace", 20, "../fonts/FreeMono.ttf" )

    # agregamos el fondo
    fondo = Sprite( "fondo", (0,0) )
    Engine.AddGObject( fondo, 0 )

    # agregamos un Sprite
    heroe = Sprite( "heroe", (550,346), "Heroe" )
    heroe.Scale( 0.16 )
    Engine.AddGObject( heroe, 1 )

    # agregamos la barra de info
    infobar = Text( None, (0,460), "monospace", (0,0,0), None, "infobar" )
    Engine.AddGObject( infobar, Engine.CAM_LAYER )

    # posicionamos la camara
    x, y = heroe.GetPosition()
    w, h = heroe.GetSize()
    cw, ch = Engine.GetCamSize()
    Engine.SetCamPosition( (x+w/2-cw/2,y+h/2-ch/2) )

    # main loop
    Engine.Run( 60 )


#--- show time
main()

from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rect import Rect


def MainUpdate( dt ):
    global key_pressed

    # abortamos con la tecla Escape
    if( Engine.IsKeyDown( Engine.CONSTANTS.K_ESCAPE ) ):
        Engine.Quit()

    # mostramos info
    fps = Engine.GetFPS()
    fps = "FPS: %07.2f" % fps

    ngobjs = len( Engine.GetGObject( "*") )
    ngobjs = "gObjs: %03d" % ngobjs

    mx, my = Engine.GetMousePos()
    mb1, mb2, mb3 = Engine.GetMousePressed()
    minfo = "Mouse: (%3d,%3d) (%d,%d,%d)" % ( mx, my, mb1, mb2, mb3 )

    infobar = Engine.GetGObject( "infobar" )
    infobar.Fill( (0,0,0,20) )
    infobar.DrawText( fps + " - " + ngobjs + " - " + minfo, (50,0), "monospace", (0,0,0) )

    # velocity = pixeles por segundo
    velocity = 240
    pixels = velocity*dt

    # la posiciona actual de la camara
    camera = Engine.GetCamera()
    x, y = camera.GetPosition()

    # la tecla presionada
    if( key_pressed == -1 ):
        if( Engine.IsKeyDown( Engine.CONSTANTS.K_RIGHT ) ): key_pressed = Engine.CONSTANTS.K_RIGHT
        elif( Engine.IsKeyDown( Engine.CONSTANTS.K_LEFT ) ): key_pressed = Engine.CONSTANTS.K_LEFT
        elif( Engine.IsKeyDown( Engine.CONSTANTS.K_DOWN ) ): key_pressed = Engine.CONSTANTS.K_DOWN
        elif( Engine.IsKeyDown( Engine.CONSTANTS.K_UP ) ): key_pressed = Engine.CONSTANTS.K_UP
    else:
        if( Engine.IsKeyUp( key_pressed ) ):
            key_pressed = -1

    # cambiamos sus coordenadas segun la tecla presionada
    if( key_pressed == Engine.CONSTANTS.K_RIGHT ):
        x = x + pixels
    elif( key_pressed == Engine.CONSTANTS.K_LEFT  ):
        x = x - pixels
    elif( key_pressed == Engine.CONSTANTS.K_DOWN  ):
        y = y - pixels
    elif( key_pressed == Engine.CONSTANTS.K_UP  ):
        y = y + pixels

    # posicionamos la camara
    camera.SetPosition( (x,y) )


def main():
    global key_pressed

    # creamos el juego
    Engine.Init( (640,480), "Move Camera" )
    Engine.SetOnUpdate( MainUpdate )

    # activamos la musica de fondo
    Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
    Engine.PlaySound( "fondo", loop=-1 )

    # cargamos los recursos que usaremos
    Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
    Engine.LoadImage( "heroe", "../images/Swordsman/Idle/Idle_000.png", 0.16 )
    Engine.LoadTTFFont( "monospace", 16, "../fonts/FreeMono.ttf" )

    # agregamos el fondo
    fondo = Sprite( "fondo", (0,0) )
    Engine.AddGObject( fondo, 0 )

    # agregamos un Sprite
    heroe = Sprite( "heroe", (550,346), "Heroe" )
    Engine.AddGObject( heroe, 1 )

    # agregamos la barra de info
    infobar = Canvas( (0,460), (640,20), "infobar" )
    Engine.AddGObjectGUI( infobar )

    # configuramos la camara
    camera = Engine.GetCamera()
    camera.SetBounds( Rect( (0,0), (1920,1056) ) )

    # posicionamos la camara
    x, y = heroe.GetPosition()
    w, h = heroe.GetSize()
    cw, ch = camera.GetSize()
    camera.SetPosition( (x+w/2-cw/2,y+h/2-ch/2) )

    # main loop
    key_pressed = -1
    Engine.Run( 60 )


#--- show time
main()

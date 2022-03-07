from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.GameObject import GameObject
from lge.Rectangle import Rectangle

from Betty import Betty


class MiJuego():
    # inicializamos el juego
    def __init__( self ):
        # creamos el juego
        Engine.Init( (640,480), "MiJuego" )
        Engine.SetOnUpdate( self.MainUpdate )
        Engine.EnableOnEvent( Engine.E_ON_COLLISION )
        Engine.ShowColliders( (255,0,0) )

        # cargamos recursos globales
        Engine.LoadTTFFont( "monospace", 16, "./fonts/FreeMono.ttf" )

        # agregamos la barra de info
        infobar = Canvas( (0, 460), (640, 20), "infobar" )
        Engine.AddGObjectGUI( infobar )

        # agregamos la imagen del mundo
        Engine.LoadImage( "mundo", "./images/Mundo.png" )
        mundo = Sprite( "mundo", (0,0) )
        Engine.AddGObject( mundo, 0 )

        # agregamos colisionadores para el suelo
        self.AddColliders()

        # agregamos los personajes
        betty = Betty( 10, 300 )
        Engine.AddGObject( betty, 1 )

        # configuramos la camara
        camera = Engine.GetCamera()
        camera.SetBounds( Rectangle( (0,0), (1920,1056) ) )
        Engine.SetCameraTarget( betty, True )

    def AddColliders( self ):
        gobj = GameObject( (0,247), (510,9) )
        gobj.SetTag( "suelo" )
        gobj.SetColliders( True )
        Engine.AddGObject( gobj, 1 )

        gobj = GameObject( (484,340), (250,9) )
        gobj.SetTag( "suelo" )
        gobj.SetColliders( True )
        Engine.AddGObject( gobj, 1 )

        gobj = GameObject( (507,210), (266,9) )
        gobj.SetTag( "muerte" )
        gobj.SetColliders( True )
        Engine.AddGObject( gobj, 1 )

    # llamado justo antes del despliegue
    def MainUpdate( self, dt ):
        # abortamos con la tecla Escape
        if( Engine.KeyUp( Engine.CONSTANTS.K_ESCAPE ) ):
            Engine.Quit()

        # mostramos info
        fps = Engine.GetFPS()
        fps = "FPS: %07.2f" % fps

        ngobjs = len( Engine.GetGObject( "*") )
        ngobjs = "gObjs: %03d" % ngobjs

        mx, my = Engine.GetMousePosition()
        mb1, mb2, mb3 = Engine.GetMouseButtons()
        minfo = "Mouse: (%3d,%3d) (%d,%d,%d)" % ( mx, my, mb1, mb2, mb3 )

        infobar = Engine.GetGObject( "infobar" )
        infobar.Fill( (0,0,0,20) )
        infobar.DrawText( fps + " - " + ngobjs + " - " + minfo, (70,0), "monospace", (0,0,0) )

    # main loop
    def Run( self ):
        Engine.Run( 60 )

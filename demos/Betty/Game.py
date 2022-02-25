import uuid

from lge.Engine import Engine
from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rectangle import Rectangle

from Betty import Betty
from Zombie import Zombie

class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (608,736), "Betty" )
        Engine.GetCamera().SetBounds( Rectangle( (0,0), (608,736) ) )

        # cargamos algunos recursos
        Engine.LoadImage( "fondo", "../images/Betty/Fondo.png" )
        Engine.LoadImage( "betty_idle" , "../images/Betty/idle-0*.png" )
        Engine.LoadImage( "betty_down" , "../images/Betty/down-0*.png" )
        Engine.LoadImage( "betty_up"   , "../images/Betty/up-0*.png" )
        Engine.LoadImage( "betty_left" , "../images/Betty/left-0*.png" )
        Engine.LoadImage( "betty_right", "../images/Betty/right-0*.png" )
        Engine.LoadImage( "zombie", "../images/Kenny/Zombie/zombie_walk*.png" )
        Engine.LoadTTFFont( "monospace", 16, "../fonts/LiberationMono-Regular.ttf" )
        Engine.LoadTTFFont( "cool", 30, "../fonts/backlash.ttf" )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0), "fondo" )
        Engine.AddGObject( fondo, 0 )

        # agregamos los muros para las colisiones
        # 1. fue creado con Tiled
        # 2  exportado desde Tiled como .png y editado para dejar sus contornos
        # 2. exportaddo desde Tiled como .csv para conocer las coordenadas de los muros
        f = open( "../images/Betty/Fondo.csv", "r" )
        data = list( f )
        f.close()
        mapa = [ e.strip("\n").strip("\n").split(",") for e in data ]
        w, h = Engine.GetCamera().GetSize()
        y = h - 32
        for r in mapa:
            x = 0
            for tid in r:
                if( tid == "muro" ):
                    gobj = GameObject( (x,y), (32,32), "Bloque-" + uuid.uuid4().hex )
                    gobj.SetTag( "muro" )
                    gobj.SetColliders( True )
                    Engine.AddGObject( gobj, 1 )
                x = x + 32
            y = y - 32

        # agregamos a Betty
        betty = Betty( "Betty" )
        betty.SetPosition( (32*9, 32*13) )
        betty.SetColliders( True )
        Engine.AddGObject( betty, 1 )

        # agregamos 3 zombies
        for i in range(3):
            zombie = Zombie( "Zombie-" + uuid.uuid4().hex )
            zombie.SetPosition( (32 + 32*4 + 32*(i*4), 32*1) )
            zombie.SetColliders( True )
            Engine.AddGObject( zombie, 1 )

        # agregamos la barra de info
        infobar = Canvas( (0,710), (640,20), "infobar" )
        Engine.AddGObjectGUI( infobar )

        # agregamos el mensaje de la barra espaciadora
        pressbar = Canvas( (120,340), (400, 30), "pressbar" )
        pressbar.DrawText( "Presiona la Barra Espaciadora", (0,0), "cool", (255,255,255) )
        Engine.AddGObjectGUI( pressbar )

        # posicionamos la camara
        Engine.GetCamera().SetPosition( (0,0) )

        # agregamos el control
        Engine.SetOnUpdate( self.IntroControl )

    # la barra de info y chequeo de fin del juego
    def _InfoBar( self ):
        # abortamos con la tecla Escape
        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_ESCAPE ) ):
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
        infobar.Fill( (0,0,0,0) )
        infobar.DrawText( fps + " - " + ngobjs + " - " + minfo, (50,0), "monospace", (255,255,255) )

    def IntroControl( self, dt ):
        # infobar
        self._InfoBar()

        # esperamos que presionen la barra espaciadora
        if( not Engine.IsKeyDown( Engine.CONSTANTS.K_SPACE ) ): return

        # ocultamos mensaje
        pressbar = Engine.GetGObject( "pressbar" )
        pressbar.SetVisible( False )

        # cambiamos el control
        Engine.SetOnUpdate( self.GameControl )

        # activamos los actores
        Engine.GetGObject( "Betty" ).SetAlive()
        for zombie in Engine.GetGObject( "Zombie-*" ):
            print(zombie)
            zombie.SetActive( True )

        # mostramos los bordes
        Engine.ShowColliders( (255,0,0) )

    def GameControl( self, dt ):
        # infobar
        self._InfoBar()

        # finaliza cuando Betty muere
        betty = Engine.GetGObject( "Betty" )
        if( betty.IsAlive() ): return

        # activamos el mensaje
        pressbar = Engine.GetGObject( "pressbar" )
        if( not pressbar.IsVisible() ):
            pressbar.SetVisible( True )

        # esperamos por la barra espaciadora para continuar
        if( not Engine.IsKeyDown( Engine.CONSTANTS.K_SPACE ) ): return

        # reinicializamos
        pressbar.SetVisible( False )
        betty.SetAlive()
        betty.SetPosition( (32*9, 32*13) )
        zombies = Engine.GetGObject( "Zombie-*" )
        for i in range( len(zombies) ):
            zombie = zombies[i]
            zombie.SetPosition( (32 + 32*4 + 32*(i*4), 32*1) )

    # main loop
    def Run( self ):
        Engine.Run( 60 )


# -- show time
game = MiJuego()
game.Run()

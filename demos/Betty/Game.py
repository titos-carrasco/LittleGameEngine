from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.Text import Text
from lge.Engine import Engine

from Betty import Betty
from Zombie import Zombie

class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (608,736), (608,736), "Betty", (0xFF, 0xFF, 0xFF) )

        # cargamos algunos recursos
        Engine.LoadImage( "fondo", "../images/Betty/Fondo.png" )
        Engine.LoadImage( "betty_idle" , "../images/Betty/idle-0*.png" )
        Engine.LoadImage( "betty_down" , "../images/Betty/down-0*.png" )
        Engine.LoadImage( "betty_up"   , "../images/Betty/up-0*.png" )
        Engine.LoadImage( "betty_left" , "../images/Betty/left-0*.png" )
        Engine.LoadImage( "betty_right", "../images/Betty/right-0*.png" )
        Engine.LoadImage( "zombie", "../images/Kenny/Zombie/zombie_walk*.png" )
        Engine.LoadTTFFont( "Monospace 20", 20, "../fonts/LiberationMono-Regular.ttf" )
        Engine.LoadTTFFont( "Cool 30", 30, "../fonts/backlash.ttf" )

        # agregamos la barra de info
        infobar = Text( None, (0,706), "Monospace 20", (255,255,255), None, "infobar" )
        Engine.AddGObject( infobar, Engine.CAM_LAYER )

        # inicializamos la escena introductoria
        self.IntroInit()

    # main loop
    def Run( self ):
        Engine.Run( 60 )

    # --- la barra de info y chequeo de fin del juego
    def _InfoBar( self ):
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
        info.SetText( fps + " "*12 + minfo )

    # --- escena introductoria
    def IntroInit( self ):
        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0), "fondo" )
        Engine.AddGObject( fondo, 0 )

        # agregamos un mensaje
        pressbar = Text( "Presiona la Barra Espaciadora", (120,340), "Cool 30", (255,255,255), None, "pressbar" )
        Engine.AddGObject( pressbar, Engine.CAM_LAYER )

        # posicionamos la camara
        Engine.SetCamPosition( (0,0) )

        # agregamos el control
        Engine.SetMainTask( self.IntroControl )

    def IntroControl( self, dt ):
        # infobar
        self._InfoBar()

        # esperamos que presionen la barra espaciadora
        if( not Engine.IsKeyDown( Engine.CONSTANTS.K_SPACE ) ): return

        # borramos todo lo que hemos creado
        Engine.DelGObject( "fondo" )
        Engine.DelGObject( "pressbar" )

        # inicializamos el juego
        self.GameInit()

    def GameInit( self ):
        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0), "fondo" )
        Engine.AddGObject( fondo, 0 )

        # agregamos un mensaje
        pressbar = Text( "Presiona la Barra Espaciadora", (120,340), "Cool 30", (255,255,255), None, "pressbar" )
        pressbar.SetVisible( False )
        Engine.AddGObject( pressbar, Engine.CAM_LAYER )

        # agregamos a Betty
        betty = Betty( "Betty" )
        Engine.AddGObject( betty, 1 )
        betty.SetPosition( (32*9, 32*13) )

        # agregamos 3 zombies
        for i in range(3):
            zombie = Zombie( "Zombie-%03d" % i )
            zombie.SetPosition( (32 + 32*4 + 32*(i*4), 32*1) )
            Engine.AddGObject( zombie, 1 )

        # agregamos los muros para las colisiones
        # 1. fue creado con Tiled
        # 2  exportado desde Tiled como .png y editado para dejar sus contornos
        # 2. exportaddo desde Tiled como .csv para conocer las coordenadas de los muros
        f = open( "../images/Betty/Fondo.csv", "r" )
        data = list( f )
        f.close()
        mapa = [ e.strip("\n").strip("\n").split(",") for e in data ]
        w, h = Engine.GetWorldSize()
        y = h - 32
        for r in mapa:
            x = 0
            for tid in r:
                if( tid == "muro" ):
                    gobj = GameObject( (x,y), (32,32), "Bloque-%03d-%03d" % (x,y) )
                    gobj.tag = "muro"
                    Engine.AddGObject( gobj, 1 )
                x = x + 32
            y = y - 32

        Engine.ShowColliders( (255,0,0) )

        # agregamos el control del juego
        Engine.SetMainTask( self.GameControl )

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

# -- show time
game = MiJuego()
game.Run()

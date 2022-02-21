from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Text import Text
from lge.Rect import Rect


class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (640,480), "Move Player" )
        Engine.SetUpdate( self.MainUpdate )

        # activamos la musica de fondo
        Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        Engine.PlaySound( "fondo", loop=-1 )

        # cargamos los recursos que usaremos
        Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
        Engine.LoadImage( "heroe_right", "../images/Swordsman/Idle/Idle_000.png", 0.16 )
        Engine.LoadImage( "heroe_left", "../images/Swordsman/Idle/Idle_000.png", 0.16, (True,False) )
        Engine.LoadTTFFont( "monospace", 20, "../fonts/FreeMono.ttf" )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        Engine.AddGObject( fondo, 0 )

        # agregamos un Sprite
        heroe = MiHeroe()

        # agregamos la barra de info
        infobar = Text( None, (0,460), "monospace", (0,0,0), None, "infobar" )
        Engine.AddGObject( infobar, Engine.CAM_LAYER )

        # configuramos la camara
        camera = Engine.GetCamera()
        camera.SetBounds( Rect( (0,0), (1920,1056) ) )

        # establecemos que la camara siga al centro del heroe
        Engine.SetCameraTarget( heroe, True )

    def MainUpdate( self, dt ):
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

        info = Engine.GetGObject( "infobar" )
        info.SetText( fps + " - " + ngobjs + " - " + minfo )

    # main loop
    def Run( self ):
        Engine.Run( 60 )


class MiHeroe( Sprite ):
    def __init__( self ):
        super().__init__( ["heroe_right","heroe_left"], (550,346), "Heroe" )
        self.SetShape( "heroe_right", 0 )
        self.heading = 1
        Engine.AddGObject( self, 1 )

    def OnUpdate( self, dt ):
        # moveremos al heroe "pps" pixeles por segundo
        pps = 240
        pixels = round( (pps*dt)/1000 )

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # cambiamos sus coordenadas y orientacion segun la tecla presionada
        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_RIGHT ) ):
            x = x + pixels
            if( self.heading != 1 ):
                self.SetShape( "heroe_right", 0 )
                self.heading = 1
        elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_LEFT ) ):
            x = x - pixels
            if( self.heading != -1 ):
                self.SetShape( "heroe_left", 0 )
                self.heading = -1
        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_DOWN ) ):
            y = y - pixels
        elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_UP ) ):
            y = y + pixels

        # lo posicionamos asegurando que se encuentre dentro de los limites
        camera = Engine.GetCamera()
        bounds = camera.GetBounds()
        self.SetPosition( (x,y), bounds )


#--- show time
game = MiJuego()
game.Run()

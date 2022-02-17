from lge.Sprite import Sprite
from lge.Text import Text
from lge.Engine import Engine


class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (1920,1056), (640,480), "Animated Player", (0xFF,0xFF,0xFF) )
        Engine.SetMainTask( self.MainControl )

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

        # agregamos al heroe con sus animaciones
        heroe = MiHeroe()
        Engine.AddGObject( heroe, 1 )

        # agregamos la barra de info
        infobar = Text( None, (0,460), "monospace", (0,0,0), None, "infobar" )
        Engine.AddGObject( infobar, Engine.CAM_LAYER )

        # establecemos que la camara siga al heroe en su origen
        Engine.SetCamTarget( heroe, False )

    def MainControl( self, dt ):
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

    # main loop
    def Run( self ):
        Engine.Run( 60 )


class MiHeroe( Sprite ):
    def __init__( self ):
        # agregamos el heroe con diferentes imagenes
        super().__init__( ["idle","run"], (550,346), "Heroe" )
        self.Scale( 0.16 )
        self.SetShape( 0, "idle" )
        self.heading = 1

    def OnUpdate( self, dt ):
        # moveremos al heroe "ppm" pixeles por minuto
        ppm = 240
        pixels = (ppm*dt)/1000

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
        moving = False
        idx, name = self.GetCurrentShape()
        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_RIGHT ) ):
            x = x + pixels
            if( self.heading != 1 ):
                self.Flip( True, False )
                self.heading = 1
            if( name != "run" ):
                self.SetShape( 0, "run" )
            moving = True
        elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_LEFT ) ):
            x = x - pixels
            if( self.heading != -1 ):
                self.Flip( True, False )
                self.heading = -1
            if( name != "run" ):
                self.SetShape( 0, "run" )
            moving = True

        if( Engine.IsKeyPressed( Engine.CONSTANTS.K_DOWN ) ):
            y = y - pixels
            moving = True
        elif( Engine.IsKeyPressed( Engine.CONSTANTS.K_UP ) ):
            y = y + pixels
            moving = True

        if( not moving and name != "idle" ):
                self.SetShape( 0, "idle" )

        # siguiente imagen de la secuencia
        self.NextShape( dt, 50 )

        # lo posicionamos asegurando que se encuentre dentro del mundo definido
        x, y = Engine.KeepInsideWorld( self, (x,y) )
        self.SetPosition( (x,y) )


#--- show time
game = MiJuego()
game.Run()

from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Canvas import Canvas
from lge.Rect import Rect

class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (640,480), "Animated Player" )
        Engine.SetOnUpdate( self.MainUpdate )

        # activamos la musica de fondo
        Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        Engine.PlaySound( "fondo", loop=-1 )

        # cargamos los recursos que usaremos
        Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png" )
        Engine.LoadImage( "heroe_idle_right", "../images/Swordsman/Idle/Idle_0*.png", 0.16 )
        Engine.LoadImage( "heroe_idle_left", "../images/Swordsman/Idle/Idle_0*.png", 0.16, (True,False) )
        Engine.LoadImage( "heroe_run_right", "../images/Swordsman/Run/Run_0*.png", 0.16 )
        Engine.LoadImage( "heroe_run_left", "../images/Swordsman/Run/Run_0*.png", 0.16, (True,False) )
        Engine.LoadTTFFont( "monospace", 16, "../fonts/FreeMono.ttf" )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        Engine.AddGObject( fondo, 0 )

        # agregamos al heroe con sus animaciones
        heroe = MiHeroe()
        Engine.AddGObject( heroe, 1 )

        # agregamos la barra de info
        infobar = Canvas( (0,460), (640,20), "infobar" )
        Engine.AddGObjectGUI( infobar )

        # configuramos la camara
        camera = Engine.GetCamera()
        camera.SetBounds( Rect( (0,0), (1920,1056) ) )

        # establecemos que la camara siga al heroe
        Engine.SetCameraTarget( heroe )

    def MainUpdate( self, dt ):
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

    # main loop
    def Run( self ):
        Engine.Run( 60 )


class MiHeroe( Sprite ):
    def __init__( self ):
        # agregamos el heroe con diferentes imagenes
        super().__init__( ["heroe_idle_right","heroe_idle_left","heroe_run_right","heroe_run_left"], (550,346), "Heroe" )
        self.SetShape( "heroe_idle_right", 0 )
        self.heading = 1
        self.key_pressed = -1

    def OnUpdate( self, dt ):
        # velocity = pixeles por segundo
        velocity = 240
        pixels = velocity*dt

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # la tecla presionada
        if( self.key_pressed == -1 ):
            if( Engine.IsKeyDown( Engine.CONSTANTS.K_RIGHT ) ): self.key_pressed = Engine.CONSTANTS.K_RIGHT
            elif( Engine.IsKeyDown( Engine.CONSTANTS.K_LEFT ) ): self.key_pressed = Engine.CONSTANTS.K_LEFT
            elif( Engine.IsKeyDown( Engine.CONSTANTS.K_DOWN ) ): self.key_pressed = Engine.CONSTANTS.K_DOWN
            elif( Engine.IsKeyDown( Engine.CONSTANTS.K_UP ) ): self.key_pressed = Engine.CONSTANTS.K_UP
        else:
            if( Engine.IsKeyUp( self.key_pressed ) ):
                self.key_pressed = -1

        # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
        name, idx = self.GetCurrentShape()
        if( self.key_pressed == Engine.CONSTANTS.K_RIGHT ):
            x = x + pixels
            if( self.heading != 1 ):
                self.heading = 1
            if( name[:9] != "heroe_run" ):
                self.SetShape( "heroe_run_right", 0 )
        elif( self.key_pressed == Engine.CONSTANTS.K_LEFT ):
            x = x - pixels
            if( self.heading != -1 ):
                self.heading = -1
            if( name[:9] != "heroe_run" ):
                self.SetShape( "heroe_run_left", 0 )
        elif( self.key_pressed == Engine.CONSTANTS.K_DOWN ):
            y = y - pixels
        elif( self.key_pressed == Engine.CONSTANTS.K_UP ):
            y = y + pixels

        if( self.key_pressed == -1 and name[:10] != "heroe_idle" ):
            if( self.heading == 1 ): self.SetShape( "heroe_idle_right", 0 )
            else: self.SetShape( "heroe_idle_left", 0 )

        # siguiente imagen de la secuencia
        self.NextShape( dt, 0.050 )

        # lo posicionamos asegurando que se encuentre dentro del mundo definido
        camera = Engine.GetCamera()
        bounds = camera.GetBounds()
        self.SetPosition( (x,y), bounds )


#--- show time
game = MiJuego()
game.Run()

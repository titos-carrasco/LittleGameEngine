from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.LGE import LGE

from Betty import Betty
from Zombie import Zombie

class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (608,736), (608,736), "Betty", (0xFF, 0xFF, 0xFF) )

        # cargamos algunos recursos
        LGE.LoadImage( "fondo", "../images/Betty/Fondo.png" )
        LGE.LoadImage( "betty_idle" , "../images/Betty/idle-0*.png" )
        LGE.LoadImage( "betty_down" , "../images/Betty/down-0*.png" )
        LGE.LoadImage( "betty_up"   , "../images/Betty/up-0*.png" )
        LGE.LoadImage( "betty_left" , "../images/Betty/left-0*.png" )
        LGE.LoadImage( "betty_right", "../images/Betty/right-0*.png" )
        LGE.LoadImage( "zombie", "../images/Kenny/Zombie/zombie_walk*.png" )
        LGE.LoadTTFFont( "Monospace 20", 20, "../fonts/LiberationMono-Regular.ttf" )
        LGE.LoadTTFFont( "Cool 30", 30, "../fonts/backlash.ttf" )

        # posicionamos la camara
        self.engine.SetCamPosition( (0,0) )

        # la escena introductoria
        self.EscenaInicio()

    # control principal
    def CheckEscape( self ):
        # abortamos con la tecla Escape
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_ESCAPE ) ):
            self.engine.Quit()

        # mostramos los FPS
        fps = self.engine.GetFPS()
        fps = "FPS: %07.2f" % fps
        self.engine.AddText( fps, (0,706), "Monospace 20", (255,255,255) )

    # escena de inicio
    def EscenaInicio( self ):
        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        self.engine.AddGObject( fondo, 0 )

        # agregamos el control de esta escena
        self.engine.SetMainTask( self.EscenaInicioControl )

    def EscenaInicioControl( self, dt ):
        self.CheckEscape()
        self.engine.AddText( "Presiona la Barra Espaciadora", (106,286), "Cool 30", (255,255,255) )

        if( not self.engine.IsKeyDown( LGE.CONSTANTS.K_SPACE ) ): return
        self.engine.DelAllGObjects()
        self.engine.SetMainTask()
        self.EscenaJuego()

    def EscenaJuego( self ):
        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0) )
        self.engine.AddGObject( fondo, 0 )

        # agregamos a Betty
        betty = Betty( self.engine, "Betty" )
        self.engine.AddGObject( betty, 1 )
        betty.SetPosition( (32*9, 32*13) )

        # agregamos 3 zombies
        for i in range(3):
            zombie = Zombie( self.engine )
            zombie.SetPosition( (32 + 32*4 + 32*(i*4), 32*1) )
            self.engine.AddGObject( zombie, 1 )

        # agregamos los muros para las colisiones
        # 1. fue creado con Tiled
        # 2  exportado desde Tiled como .png y editado para dejar sus contornos
        # 2. exportaddo desde Tiled como .csv para conocer las coordenadas de los muros
        f = open( "../images/Betty/Fondo.csv", "r" )
        data = list( f )
        f.close()
        mapa = [ e.strip("\n").strip("\n").split(",") for e in data ]
        w, h = self.engine.GetWorldSize()
        y = h - 32
        for r in mapa:
            x = 0
            for tid in r:
                if( tid == "muro" ):
                    gobj = GameObject( (x,y), (32,32) )
                    gobj.tag = "muro"
                    self.engine.AddGObject( gobj, 1 )
                x = x + 32
            y = y - 32

        # agregamos el control de esta escena
        self.engine.SetMainTask( self.EscenaJuegoControl )

    def EscenaJuegoControl( self, dt ):
        self.CheckEscape()

        betty = self.engine.GetGObjectByName( "Betty" )
        if( not betty.IsAlive() ):
            self.engine.AddText( "Presiona la Barra Espaciadora", (106,286), "Cool 30", (255,255,255) )
            if( not self.engine.IsKeyDown( LGE.CONSTANTS.K_SPACE ) ): return
            self.engine.DelAllGObjects()
            self.engine.SetMainTask()
            self.EscenaJuego()


    # main loop
    def Run( self ):
        self.engine.Run( 60 )



# -- show time
game = MiJuego()
game.Run()

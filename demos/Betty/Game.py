from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.LGE import LGE

from Betty import Betty

class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (608,736), (608,736), "Betty", (0xFF, 0xFF, 0xFF) )
        self.engine.SetFPS( 60 )
        self.engine.SetMainTask( self.mainControl )

        # agregamos el fondo
        fondo = Sprite( "../images/Betty/Fondo.png", (0,0) )
        self.engine.AddGObject( fondo, 0 )

        # agregamos a Betty
        betty = Betty( self.engine )
        self.engine.AddGObject( betty, 1 )
        betty.SetPosition( (32*9, 32*13) )

        # agregamos gobjects como colliders
        w, h = self.engine.GetWorldSize()
        y = h - 32
        f = open( "../images/Betty/Fondo.csv", "r" )
        while( True ):
            x = 0
            line = f.readline()
            if( line == "" ): break
            line = [ int( c ) for c in line.replace( "\r", "" ).replace( "\n", "" ).split( "," ) ]
            for c in line:
                if( c != -1 ):
                    gobj = GameObject( (x,y), (32,32) )
                    self.engine.AddGObject( gobj, 1 )
                x = x + 32
            y = y - 32

        # posicionamos la camara
        self.engine.SetCamPosition( (0,0) )

        # cargamos algunos fonts
        self.engine.LoadSysFont( "consolas", 20 )

        # mostramos los colliders
        #self.engine.ShowColliders( (0xF0,0x00,0x00) )

    # main loop
    def Run( self ):
        self.engine.Run()

    # control principal
    def mainControl( self, dt ):
        # abortamos con la tecla Escape
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_ESCAPE ) ):
            self.engine.Quit()

        # mostramos los FPS
        fps = self.engine.GetFPS()
        fps = "FPS: %07.2f" % fps
        self.engine.AddText( fps, (0,706), "consolas", 20, (255,255,255) )

# -- show time
game = MiJuego()
game.Run()

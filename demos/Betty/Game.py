from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.LGE import LGE

from Betty import Betty
from Zombie import Zombie

class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (608,736), (608,736), "Betty", (0xFF, 0xFF, 0xFF) )
        self.engine.SetFPS( 60 )

        # cargamos algunos fonts
        # self.engine.LoadSysFont( "consolas", 20 )
        self.engine.LoadTTFFont( "Monospace 20", 20, "../fonts/LiberationMono-Regular.ttf" )
        self.engine.LoadTTFFont( "Cool 30", 30, "../fonts/backlash.ttf" )

        # posicionamos la camara
        self.engine.SetCamPosition( (0,0) )

        # mostramos los colliders
        #self.engine.ShowColliders( (0xF0,0x00,0x00) )

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
        fondo = Sprite( "../images/Betty/FondoInicio.png", (0,0) )
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
        fondo = Sprite( "../images/Betty/Fondo.png", (0,0) )
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
                    gobj.tag = "muro"
                    self.engine.AddGObject( gobj, 1 )
                x = x + 32
            y = y - 32

        # agregamos el control de esta escena
        self.engine.SetMainTask( self.EscenaJuegoControl )

    def EscenaJuegoControl( self, dt ):
        self.CheckEscape()

        collisions = self.engine.GetCollisions( "Betty" )
        zombies = [ True for gobj, layer in collisions if gobj.tag == "zombie" ]
        if( len( zombies ) > 0 ):
            self.engine.AddText( "Presiona la Barra Espaciadora", (106,286), "Cool 30", (255,255,255) )
            if( not self.engine.IsKeyDown( LGE.CONSTANTS.K_SPACE ) ): return
            self.engine.DelAllGObjects()
            self.engine.SetMainTask()
            self.EscenaJuego()


    # main loop
    def Run( self ):
        self.engine.Run()



# -- show time
game = MiJuego()
game.Run()

from lge.Sprite import Sprite
from lge.LGE import LGE


class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (1920,1056), (640,480), "Move Camera", (0xFF,0xFF,0xFF) )
        self.engine.SetFPS( 60 )
        self.engine.SetMainTask( self.MainControl )

        # cargamos un font
        self.engine.LoadSysFont( "consolas", 20 )

        # agregamos el fondo
        fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0) )
        self.engine.AddGObject( fondo, 0 )

        # agregamos un Sprite
        heroe = Sprite( "../images/Swordsman/Idle/Idle_000.png", (550,346), "Heroe" )
        heroe.ScalePercent( 0.16 )
        self.engine.AddGObject( heroe, 1 )

        # posicionamos la camara
        x, y = heroe.GetPosition()
        w, h = heroe.GetSize()
        self.engine.SetCamPosition( (x+w/2,y+h/2) )

    def MainControl( self, dt ):
        # abortamos con la tecla Escape
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_ESCAPE ) ):
            self.engine.Quit()

        # mostramos los FPS actuales
        fps = self.engine.GetFPS()
        fps = "FPS: %07.2f" % fps
        self.engine.AddText( fps, (0,460), "consolas", 20 )

        # moveremos la camara "ppm" pixeles por minuto
        ppm = 240
        pixels = (ppm*dt)/1000

        # la posiciona actual de la camara
        x, y = self.engine.GetCamPosition()

        # cambiamos sus coordenadas segun la tecla presionada
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_RIGHT ) ):
            x = x + pixels
        elif( self.engine.IsKeyPressed( LGE.CONSTANTS.K_LEFT ) ):
            x = x - pixels
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_DOWN ) ):
            y = y - pixels
        elif( self.engine.IsKeyPressed( LGE.CONSTANTS.K_UP ) ):
            y = y + pixels

        # posicionamos la camara
        self.engine.SetCamPosition( (x,y) )

    # main loop
    def Run( self ):
        self.engine.Run()


#--- show time
game = MiJuego()
game.Run()

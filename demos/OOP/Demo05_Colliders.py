from lge.GameObject import GameObject
from lge.Sprite import Sprite
from lge.LGE import LGE


class MiJuego():
    def __init__( self ):
        # creamos el juego
        self.engine = LGE( (1920,1056), (640,480), "Colliders", (0,0,0) )
        self.engine.SetFPS( 60 )
        self.engine.SetMainTask( self.MainControl )

        # cargamos un font
        self.engine.LoadSysFont( "consolas", 20 )

        # agregamos el fondo
        fondo = Sprite( "../images/Backgrounds/FreeTileset/Fondo.png", (0,0) )
        self.engine.AddGObject( fondo, 0 )

        # agregamos al heroe
        heroe = MiHeroe( self.engine )
        self.engine.AddGObject( heroe, 1 )

        # agregamos otro objeto
        gobj = Sprite( "../images/Swordsman/Idle/Idle_000.png", (350,250) )
        gobj.ScalePercent( 0.16 )
        self.engine.AddGObject( gobj, 1 )

        # establecemos que la camara siga al heroe en su origen
        self.engine.SetCamTarget( heroe, False )

        # para vosualizar el despliegue de los contornos de los objetos
        self.engine.ShowColliders( (0xFF,0x00,0x00) )
        self.showColliders = True

    def MainControl( self, dt ):
        # abortamos con la tecla Escape
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_ESCAPE ) ):
            self.engine.Quit()

        # mostramos los FPS actuales
        fps = self.engine.GetFPS()
        fps = "FPS: %07.2f" % fps
        self.engine.AddText( fps, (0,460), "consolas", 20 )

        # mostramos los bordes
        if( self.engine.IsKeyUp( LGE.CONSTANTS.K_c) ):
            self.showColliders = not self.showColliders
            if( self.showColliders ):
                self.engine.ShowColliders( (0xFF, 0x00, 0x00) )
            else:
                self.engine.ShowColliders()

    # main loop
    def Run( self ):
        self.engine.Run()


class MiHeroe( Sprite ):
    def __init__( self, engine ):
        # agregamos el heroe con diferentes imagenes
        fnames = {
            "idle": "../images/Swordsman/Idle/Idle_0*.png",
            "run" : "../images/Swordsman/Run/Run_0*.png"
        }
        super().__init__( fnames, (550,346), "Heroe" )
        self.engine = engine
        self.ScalePercent( 0.16 )
        self.SetShape( 0, "idle" )
        self.heading = 1
        self.elapsed = 0

    def TestCollisions( self, dt ):
        crops = self.engine.GetCollisions( self.name )
        if( len(crops) == 0 ): return

        obj, r = crops[0]
        xr, yr, wr,hr = r
        x, y = self.GetPosition()
        w, h = self.GetSize()

        # viene horizontal
        if( hr > wr ):
            if( xr == x ):
                x = xr + wr + 1
            else:
                x = xr - w
        else:
            if( yr == y ):
                y = yr + hr + 1
            else:
                y = yr - h

        self.SetPosition( (x,y) )

    def OnUpdate( self, dt ):
        # moveremos al heroe "ppm" pixeles por minuto
        ppm = 240
        pixels = (ppm*dt)/1000

        # la posiciona actual del heroe
        x, y = self.GetPosition()

        # cambiamos sus coordenadas, orientacion e imagen segun la tecla presionada
        moving = False
        idx, name = self.GetCurrentShape()
        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_RIGHT ) ):
            x = x + pixels
            if( self.heading != 1 ):
                self.Flip( True, False )
                self.heading = 1
            if( name != "run" ):
                self.SetShape( 0, "run" )
            moving = True
        elif( self.engine.IsKeyPressed( LGE.CONSTANTS.K_LEFT ) ):
            x = x - pixels
            if( self.heading != -1 ):
                self.Flip( True, False )
                self.heading = -1
            if( name != "run" ):
                self.SetShape( 0, "run" )
            moving = True

        if( self.engine.IsKeyPressed( LGE.CONSTANTS.K_DOWN ) ):
            y = y - pixels
            moving = True
        elif( self.engine.IsKeyPressed( LGE.CONSTANTS.K_UP ) ):
            y = y + pixels
            moving = True

        if( not moving and name != "idle" ):
                self.SetShape( 0, "idle" )

        # siguiente imagen de la secuencia
        t = self.elapsed + dt
        if( t >= 50 ):
            self.NextShape()
            t = 0
        self.elapsed = t

        # lo posicionamos asegurando que se encuentre dentro del mundo definido
        x, y = self.engine.KeepInsideWorld( self, (x,y) )
        self.SetPosition( (x,y) )

        # vemos las colisiones
        self.TestCollisions( dt )


#--- show time
game = MiJuego()
game.Run()

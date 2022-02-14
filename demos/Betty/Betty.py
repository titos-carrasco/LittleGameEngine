from lge.Sprite import Sprite
from lge.LGE import LGE


class Betty( Sprite ):
    def __init__( self, engine, name ):
        anim = {
            "idle" : "../images/Betty/idle-0*.png",
            "down" : "../images/Betty/down-0*.png",
            "up"   : "../images/Betty/up-0*.png",
            "left" : "../images/Betty/left-0*.png",
            "right": "../images/Betty/right-0*.png",
        }
        super().__init__( anim, (32,32), name )
        self.engine = engine
        self.SetShape( 0, "idle" )
        self.tag = "Betty"
        self.alive = True

    def IsAlive( self ):
        return self.alive

    def OnUpdate( self, dt ):
        # solo si estoy viva
        if( not self.alive ): return

        # nos movemnos a "ppm" pixeles por minuto
        #ppm = 120
        #pixels = (ppm*dt)/1000
        pixels = 2

        # nuestra posicion actual y tamano
        x, y = self.GetPosition()
        w, h = self.GetSize()
        xori, yori = x, y

        # cambiamos sus coordenadas, imagen segun la tecla presionada
        idx, action = self.GetCurrentShape()
        new_action = action
        if( action == "idle"):
            if( self.engine.IsKeyDown( LGE.CONSTANTS.K_RIGHT ) ):
                new_action = "right"
            elif( self.engine.IsKeyDown( LGE.CONSTANTS.K_LEFT) ):
                new_action = "left"
            elif( self.engine.IsKeyDown( LGE.CONSTANTS.K_UP ) ):
                new_action = "up"
            elif( self.engine.IsKeyDown( LGE.CONSTANTS.K_DOWN ) ):
                new_action = "down"
        elif( action == "right" ):
            if( self.engine.IsKeyUp( LGE.CONSTANTS.K_RIGHT ) ): new_action = "idle"
            else: x = x + pixels
        elif( action == "left" ):
            if( self.engine.IsKeyUp( LGE.CONSTANTS.K_LEFT ) ): new_action = "idle"
            else: x = x - pixels
        elif( action == "up" ):
            if( self.engine.IsKeyUp( LGE.CONSTANTS.K_UP ) ): new_action = "idle"
            else: y = y + pixels
        elif( action == "down" ):
            if( self.engine.IsKeyUp( LGE.CONSTANTS.K_DOWN ) ): new_action = "idle"
            else: y = y - pixels

        if( action != new_action ):
            self.SetShape( 0, new_action )
            if( new_action == "idle" ):
                if( x%32 < 8 or x%32 > 23 ): x = round( x/32 )*32
                if( y%32 < 8 or y%32 > 23 ): y = round( y/32 )*32

        # siguiente imagen de la secuencia
        self.NextShape( dt, 100 )

        # lo posicionamos
        self.SetPosition( (x,y) )
        collisions = self.engine.GetCollisions( self.name )
        if( len( collisions ) > 0 ):
            self.SetPosition( (xori, yori) )

        # tunel?
        x, y = self.GetPosition()
        w, h = self.engine.GetWorldSize()
        if( x < -16 ): x = w - 16
        elif( x > w - 16 ): x = -16
        self.SetPosition( (x,y) )

        # dead?
        zombies = [ gobj for gobj, layer in collisions if gobj.tag == "zombie" ]
        if( len( zombies) > 0 ):
            self.alive = False

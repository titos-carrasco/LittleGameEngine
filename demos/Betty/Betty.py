from lge.Sprite import Sprite
from lge.Engine import Engine


class Betty( Sprite ):
    def __init__( self, name ):
        super().__init__( ["betty_idle","betty_down", "betty_up", "betty_left", "betty_right"], (0,0), name )
        self.SetShape( 0, "betty_idle" )
        self.tag = "Betty"
        self.alive = True

    def IsAlive( self ):
        return self.alive

    def SetAlive( self ):
        self.alive = True
        self.SetShape( 0, "betty_idle" )

    def OnUpdate( self, dt ):
        # solo si estoy viva
        if( not self.alive ): return

        # nos movemos a "pps" pixeles por segundo
        pps = 120
        pixels = round( (pps*dt)/1000 )

        # nuestra posicion actual y tamano
        x, y = self.GetPosition()
        w, h = self.GetSize()
        xori, yori = x, y

        # cambiamos sus coordenadas e imagen segun la tecla presionada
        idx, action = self.GetCurrentShape()
        new_action = action
        if( action == "betty_idle"):
            if( Engine.IsKeyDown( Engine.CONSTANTS.K_RIGHT ) ):
                new_action = "betty_right"
            elif( Engine.IsKeyDown( Engine.CONSTANTS.K_LEFT) ):
                new_action = "betty_left"
            elif( Engine.IsKeyDown( Engine.CONSTANTS.K_UP ) ):
                new_action = "betty_up"
            elif( Engine.IsKeyDown( Engine.CONSTANTS.K_DOWN ) ):
                new_action = "betty_down"
        elif( action == "betty_right" ):
            if( Engine.IsKeyUp( Engine.CONSTANTS.K_RIGHT ) ): new_action = "betty_idle"
            else: x = x + pixels
        elif( action == "betty_left" ):
            if( Engine.IsKeyUp( Engine.CONSTANTS.K_LEFT ) ): new_action = "betty_idle"
            else: x = x - pixels
        elif( action == "betty_up" ):
            if( Engine.IsKeyUp( Engine.CONSTANTS.K_UP ) ): new_action = "betty_idle"
            else: y = y + pixels
        elif( action == "betty_down" ):
            if( Engine.IsKeyUp( Engine.CONSTANTS.K_DOWN ) ): new_action = "betty_idle"
            else: y = y - pixels

        if( action != new_action ):
            self.SetShape( 0, new_action )
            if( new_action == "betty_idle" ):
                if( x%32 < 8 or x%32 > 23 ): x = round( x/32 )*32
                if( y%32 < 8 or y%32 > 23 ): y = round( y/32 )*32

        # siguiente imagen de la secuencia
        self.NextShape( dt, 100 )

        # lo posicionamos
        self.SetPosition( (x,y) )
        collisions = Engine.GetCollisions( self.name )
        if( len( collisions ) > 0 ):
            self.SetPosition( (xori, yori) )

        # tunel?
        x, y = self.GetPosition()
        w, h = Engine.GetWorldBounds().GetSize()
        if( x < -16 ): x = w - 16
        elif( x > w - 16 ): x = -16
        self.SetPosition( (x,y) )

        # dead?
        zombies = [ gobj for gobj, layer in collisions if gobj.tag == "zombie" ]
        if( len( zombies) > 0 ):
            self.alive = False

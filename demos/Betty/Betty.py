from lge.Sprite import Sprite
from lge.Engine import Engine


class Betty( Sprite ):
    def __init__( self, name ):
        super().__init__( ["betty_idle","betty_down", "betty_up", "betty_left", "betty_right"], (0,0), name )
        self.SetShape( "betty_idle", 0 )
        self.SetTag( "Betty" )
        self.alive = False

    def IsAlive( self ):
        return self.alive

    def SetAlive( self ):
        self.alive = True
        self.SetShape( "betty_idle", 0 )

    def OnUpdate( self, dt ):
        # solo si estoy viva
        if( not self.alive ): return

        # velocity = pixeles por segundo
        velocity = 120
        #pixels = velocity*dt
        pixels = 2

        # nuestra posicion actual y tamano
        x, y = self.GetPosition()
        w, h = self.GetSize()
        xori, yori = x, y

        # cambiamos sus coordenadas e imagen segun la tecla presionada
        action, idx = self.GetCurrentShape()
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
            self.SetShape( new_action, 0 )
            if( new_action == "betty_idle" ):
                if( x%32 < 8 or x%32 > 23 ): x = round( x/32 )*32
                if( y%32 < 8 or y%32 > 23 ): y = round( y/32 )*32

        # siguiente imagen de la secuencia
        self.NextShape( dt, 0.100 )

        # lo posicionamos
        self.SetPosition( (x,y) )
        collisions = Engine.GetCollisions( self.name )
        if( collisions ):
            # zombi?
            zombies = [ gobj for gobj, collider in collisions if gobj.GetTag() == "zombie" ]
            if( zombies ):
                self.alive = False
                return

            # es un muro
            self.SetPosition( (xori, yori) )
            return

        # tunel?
        x, y = self.GetPosition()
        w, h = Engine.GetCamera().GetSize()
        if( x < -16 ): x = w - 16
        elif( x > w - 16 ): x = -16
        self.SetPosition( (x,y) )

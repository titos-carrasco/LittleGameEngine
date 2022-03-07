from lge.Engine import Engine
from lge.Sprite import Sprite

class Betty(Sprite):
    def __init__( self, x, y ):
        Engine.LoadImage( "idle", "./images/Betty-idle-001.png" )
        Engine.LoadImage( "left", "./images/Betty-left-0*.png" )
        Engine.LoadImage( "right", "./images/Betty-right-0*.png" )

        images = ["idle","left","right"]

        super().__init__( images, (x, y), "Betty" )
        self.vx = 240           # velocidad en x
        self.vy = 0             # velocidad en y
        self.vs = 240           # velocidad en y en el salto
        self.ay = 480           # aceleracion en y
        self.SetColliders( True )

    def OnUpdate( self, dt ):
        # los datos actuales
        x, y = self.GetPosition()
        action, idx = self.GetCurrentShape()

        # cambiamos sus coordenadas y orientacion segun la tecla presionada
        if( Engine.KeyUp(  Engine.CONSTANTS.K_SPACE ) ):
            self.vy = self.vs

        if( Engine.KeyPressed(  Engine.CONSTANTS.K_RIGHT ) ):
            x = x + self.vx*dt
            if( action != "right" ):
                self.SetShape( "right", 0 )
        elif( Engine.KeyPressed( Engine.CONSTANTS.K_LEFT ) ):
            x = x - self.vx*dt
            if( action != "left" ):
                self.SetShape( "left", 0 )
        else:
            if( action != "idle" ):
                self.SetShape( "idle", 0 )
        self.NextShape( dt, 0.050 )

        # caida por gravedad
        y = y + self.vy*dt
        self.vy = self.vy - self.ay*dt

        # lo posicionamos asegurando que se encuentre dentro de los limites
        camera = Engine.GetCamera()
        bounds = camera.GetBounds()
        self.SetPosition( x, y, bounds )

    def OnCollision( self, dt, collisions ):
        x1, y1, x2, y2 = self.GetRectangle().GetPoints()
        for o, r in collisions:
            rx1, ry1, rx2, ry2 = r.GetPoints()
            tag = o.GetTag()
            if( tag == "suelo" ):
                if( y1 > ry1 ):
                    self.vy = 0
                    self.SetPosition( x1, ry2 + 1 )
            elif( tag == "muerte" ):
                print( "he muerto" )


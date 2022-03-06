from lge.Sprite import Sprite
from lge.Engine import Engine


class BlockHorizontal( Sprite ):
    def __init__( self, x, y ):
        super().__init__( "roca", (128,128), "roca"  )
        self.x, self.y = x, y
        self.SetShape( "roca", 0 )
        self.SetTag( "ground" )
        self.dir = "up"
        self.SetPosition( x, y )

    def OnUpdate( self, dt ):
        # velocity = pixeles por segundo
        velocity = 120
        pixels = velocity*dt

        ww, wh = Engine.GetCamera().GetSize()
        if( self.dir == "up" ):
            self.y = self.y + pixels
        else:
            self.y = self.y - pixels
        self.SetPosition( self.x, self.y )

        if( self.y >= wh - 64*4 ): self.dir = "down"
        elif( self.y < 64*1 ): self.dir = "up"

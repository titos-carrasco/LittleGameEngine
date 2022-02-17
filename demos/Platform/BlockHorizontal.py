from lge.Sprite import Sprite
from lge.Engine import Engine


class BlockHorizontal( Sprite ):
    def __init__( self, pos ):
        super().__init__( "roca", (128,128), "roca"  )
        self.x, self.y = pos
        self.SetShape( 0, "roca" )
        self.tag = "ground"
        self.dir = "up"
        self.SetPosition( pos )

    def OnUpdate( self, dt ):
        # nos movemnos a "ppm" pixeles por minuto
        ppm = 120
        pixels = round( (ppm*dt)/1000 )

        ww, wh = Engine.GetWorldBounds().GetSize()
        if( self.dir == "up" ):
            self.y = self.y + pixels
        else:
            self.y = self.y - pixels
        self.SetPosition( (self.x,self.y) )

        if( self.y >= wh - 64*4 ): self.dir = "down"
        elif( self.y < 64*1 ): self.dir = "up"

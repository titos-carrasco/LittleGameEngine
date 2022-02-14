from lge.Sprite import Sprite
from lge.LGE import LGE


class BlockHorizontal( Sprite ):
    def __init__( self, engine, pos, layer ):
        super().__init__( "../images/Volcano_Pack_1.1/volcano_pack_alt_39.png", (128,128)  )
        self.engine = engine
        self.x, self.y = pos
        self.SetShape( 0 )
        self.tag = "ground"
        self.dir = "up"
        self.SetPosition( pos )
        self.engine.AddGObject( self, layer )

    def OnUpdate( self, dt ):
        # nos movemnos a "ppm" pixeles por minuto
        ppm = 120
        pixels = round( (ppm*dt)/1000 )

        ww, wh = self.engine.GetWorldSize()
        if( self.dir == "up" ):
            self.y = self.y + pixels
        else:
            self.y = self.y - pixels
        self.SetPosition( (self.x,self.y) )

        if( self.y >= wh - 64*4 ): self.dir = "down"
        elif( self.y < 64*1 ): self.dir = "up"

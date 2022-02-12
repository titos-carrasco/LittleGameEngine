from lge.Sprite import Sprite
from lge.LGE import LGE


class Zombie( Sprite ):
    def __init__( self, engine ):
        super().__init__( "../images/Kenny/Zombie/zombie_walk*.png", (32,32)  )
        self.engine = engine
        self.elapsed = 0
        self.SetShape( 0 )
        self.tag = "zombie"
        self.dir = "R"

    def OnUpdate( self, dt ):
        # nos movemnos a "ppm" pixeles por minuto
        ppm = 240
        pixels = (ppm*dt)/1000
        pixels = 2

        # las coordenadas de Betty
        betty = self.engine.GetGObject( "Betty" )
        bx, by = betty.GetPosition()

        # nuestra posicion actual
        x, y = self.GetPosition()
        xori, yori = x, y

        # nuevas coordenadas
        orden = ""
        dx = abs(x - bx)
        dy = abs(y - by)

        primeroY = dy > dx
        abajo = y < by
        arriba = y > by
        izquierda = x < bx
        derecha = x > bx
        if( self.dir == "R" ):
            if( abajo and izquierda ): orden ="URDL"
            elif( abajo and derecha ): orden ="UDRL"
            elif( arriba and izquierda ): orden = "DRUL"
            elif( arriba and derecha ): orden ="DURL"
            elif( arriba ): orden = "DRUL"
            elif( abajo ): orden = "URDL"
            elif( izquierda ): orden = "RUDL"
            elif( derecha ): orden = "UDRL"
        elif( self.dir == "L" ):
            if( abajo and izquierda ): orden ="UDLR"
            elif( abajo and derecha ): orden ="LUDR"
            elif( arriba and izquierda ): orden = "DULR"
            elif( arriba and derecha ): orden ="DLUR"
            elif( arriba ): orden = "DLUR"
            elif( abajo ): orden = "ULDR"
            elif( izquierda ): orden = "LUDR"
            elif( derecha ): orden = "UDLR"
        elif( self.dir == "U" ):
            if( abajo and izquierda ): orden ="URLD"
            elif( abajo and derecha ): orden ="ULRD"
            elif( arriba and izquierda ): orden = "RLUD"
            elif( arriba and derecha ): orden ="LRUD"
            elif( arriba ): orden = "LRUD"
            elif( abajo ): orden = "ULRD"
            elif( izquierda ): orden = "RULD"
            elif( derecha ): orden = "LURD"
        elif( self.dir == "D" ):
            if( abajo and izquierda ): orden ="RLDU"
            elif( abajo and derecha ): orden ="LRDU"
            elif( arriba and izquierda ): orden = "RDLU"
            elif( arriba and derecha ): orden ="LDRU"
            elif( arriba ): orden = "DLRU"
            elif( abajo ): orden = "LRDU"
            elif( izquierda ): orden = "RDLU"
            elif( derecha ): orden = "LDRU"

        for c in orden:
            if( c == "R" ): x = x + pixels
            elif( c == "L" ): x = x - pixels
            elif( c == "U" ): y = y + pixels
            elif( c == "D" ): y = y - pixels
            self.SetPosition( (x,y) )
            collisions = self.engine.GetCollisions( self.name )
            bloqueos = [ gobj for gobj, layer in collisions if gobj.tag == "muro" or gobj.tag == "zombie" ]
            if( len( bloqueos ) == 0 ):
                self.dir = c
                break
            x, y = xori, yori
            self.SetPosition( (x,y) )

        # tunel?
        x, y = self.GetPosition()
        w, h = self.engine.GetWorldSize()
        if( x < -16 ): x = w - 16
        elif( x > w - 16 ): x = -16
        self.SetPosition( (x,y) )

        # siguiente imagen de la secuencia
        t = self.elapsed + dt
        if( t >= 100 ):
            self.NextShape()
            t = 0
        self.elapsed = t
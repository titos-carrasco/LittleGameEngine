import random

from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class Zombie(Sprite):
    def __init__(self, name, win_size):
        super().__init__("zombie", (0, 0), name)

        self.lge = self.GetLGE()

        self.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.SetShape("zombie")
        self.SetTag("zombie")
        self.UseColliders(True)
        self.active = True
        self.win_size = win_size

        # direccion inicial - Right, Down, Left, Up
        self.dir = "RDLU"[int(random.random() * 4)]

    def SetActive(self, state):
        self.active = state

    def OnUpdate(self, dt):
        if(not self.active):
            return

        # velocity = pixeles por segundo
        #velocity = 120
        #pixels = velocity*dt
        pixels = 2

        # las coordenadas de Betty
        betty = self.lge.GetGObject("Betty")
        bx, by = betty.GetPosition()

        # nuestra posicion actual
        x, y = self.GetPosition()

        # posicion respecto a Betty
        abajo = y < by
        arriba = y > by
        izquierda = x < bx
        derecha = x > bx

        # estrategia de movimiento
        estrategia = ""

        if (self.dir == 'R'):
            if (abajo and izquierda):
                estrategia = "URDL"
            elif (abajo and derecha):
                estrategia = "UDRL"
            elif (arriba and izquierda):
                estrategia = "DRUL"
            elif (arriba and derecha):
                estrategia = "DURL"
            elif (arriba):
                estrategia = "DRUL"
            elif (abajo):
                estrategia = "URDL"
            elif (izquierda):
                estrategia = "RUDL"
            elif (derecha):
                estrategia = "UDRL"
        elif (self.dir == 'L'):
            if (abajo and izquierda):
                estrategia = "UDLR"
            elif (abajo and derecha):
                estrategia = "LUDR"
            elif (arriba and izquierda):
                estrategia = "DULR"
            elif (arriba and derecha):
                estrategia = "DLUR"
            elif (arriba):
                estrategia = "DLUR"
            elif (abajo):
                estrategia = "ULDR"
            elif (izquierda):
                estrategia = "LUDR"
            elif (derecha):
                estrategia = "UDLR"
        elif (self.dir == 'U'):
            if (abajo and izquierda):
                estrategia = "URLD"
            elif (abajo and derecha):
                estrategia = "ULRD"
            elif (arriba and izquierda):
                estrategia = "RLUD"
            elif (arriba and derecha):
                estrategia = "LRUD"
            elif (arriba):
                estrategia = "LRUD"
            elif (abajo):
                estrategia = "ULRD"
            elif (izquierda):
                estrategia = "RULD"
            elif (derecha):
                estrategia = "LURD"
        elif (self.dir == 'D'):
            if (abajo and izquierda):
                estrategia = "RLDU"
            elif (abajo and derecha):
                estrategia = "LRDU"
            elif (arriba and izquierda):
                estrategia = "RDLU"
            elif (arriba and derecha):
                estrategia = "LDRU"
            elif (arriba):
                estrategia = "DLRU"
            elif (abajo):
                estrategia = "LRDU"
            elif (izquierda):
                estrategia = "RDLU"
            elif (derecha):
                estrategia = "LDRU"

        # probamos cada movimiento de la estrategia
        for c in estrategia:
            nx, ny = x, y

            if (c == 'R'):
                nx += pixels
            elif (c == 'L'):
                nx -= pixels
            elif (c == 'U'):
                ny += pixels
            elif (c == 'D'):
                ny -= pixels

            # verificamos que no colisionemos con un muro u otro zombie
            self.SetPosition(nx, ny)
            gobjs = self.lge.IntersectGObjects(self)
            collision = False
            for gobj in gobjs:
                tag = gobj.GetTag()
                if(tag == "zombie" or tag == "muro"):
                    collision = True
                    break

            if(not collision):
                self.dir = c

                # tunel?
                if (nx < -16):
                    nx = self.win_size[0] - 16
                elif (nx > self.win_size[0] - 16):
                    nx = -16
                self.SetPosition(nx, ny)
                break

            # otro intento
            self.SetPosition(x, y)

        # siguiente imagen de la secuencia
        self.NextShape(dt, 0.100)

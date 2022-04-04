from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class BlockHorizontal(Sprite):
    def __init__(self, x, y):
        super().__init__("roca", (128, 128), "roca")

        # acceso al motor de juegos
        self.lge = LittleGameEngine.GetLGE()

        self.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.SetPosition(x, y)
        self.SetShape("roca")
        self.SetTag("ground")
        self.x, self.y = x, y
        self.dir = "up"
        self.limit_top = y + 64*4
        self.limit_bottom = y - 64

    def OnUpdate(self, dt):
        # velocity = pixeles por segundo
        velocity = 120
        pixels = velocity*dt
        if(pixels < 1):
            pixels = 1

        if(self.dir == "up"):
            self.y = self.y + pixels
        else:
            self.y = self.y - pixels
        self.SetPosition(self.x, self.y)

        if(self.y >= self.limit_top):
            self.dir = "down"
        elif(self.y < self.limit_bottom):
            self.dir = "up"

from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class BlockHorizontal(Sprite):
    def __init__(self, x, y):
        super().__init__("roca", (128, 128), "roca")

        self.setOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.setPosition(x, y)
        self.setShape("roca")
        self.setTag("ground")
        self.x, self.y = x, y
        self.dir = "up"
        self.limitTop = y + 64*4
        self.limitBottom = y - 64

    def onUpdate(self, dt):
        # velocity = pixeles por segundo
        velocity = 120
        pixels = velocity*dt
        if(pixels < 1):
            pixels = 1

        if(self.dir == "up"):
            self.y = self.y + pixels
        else:
            self.y = self.y - pixels
        self.setPosition(self.x, self.y)

        if(self.y >= self.limitTop):
            self.dir = "down"
        elif(self.y < self.limitBottom):
            self.dir = "up"

from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class BlockHorizontal(Sprite):

    def __init__(self, x, y):
        super().__init__("roca", (128, 128), "roca")

        self.setPosition(x, y)
        self.setTag("ground")
        self.x, self.y = x, y
        self.dir = "up"
        self.limitTop = y - 64
        self.limitBottom = y + 64 * 4

    # @Override
    def onUpdate(self, dt):
        # velocity = pixeles por segundo
        velocity = 120
        pixels = velocity * dt

        if(self.dir == "up"):
            self.y = self.y - pixels
        else:
            self.y = self.y + pixels
        self.setPosition(self.x, self.y)

        if(self.y < self.limitTop):
            self.dir = "down"
        elif(self.y > self.limitBottom):
            self.dir = "up"

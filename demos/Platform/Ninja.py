from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class Ninja(Sprite):
    def __init__(self, position):
        super().__init__("ninja", position)

        self.setOnEvents(LittleGameEngine.E_ON_UPDATE)

    def onUpdate(self, dt):
        self.nextShape(dt, 0.050)

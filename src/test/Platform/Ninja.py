from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class Ninja(Sprite):

    def __init__(self, position):
        super().__init__("ninja", position)

    # @Override
    def onUpdate(self, dt):
        self.nextImage(dt, 0.050)

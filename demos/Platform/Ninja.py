from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class Ninja(Sprite):
    def __init__(self, position):
        super().__init__("ninja", position)

        # acceso al motor de juegos
        self.lge = self.GetLGE()

        self.SetOnEvents(LittleGameEngine.E_ON_UPDATE)

    def OnUpdate(self, dt):
        self.NextShape(dt, 0.050)

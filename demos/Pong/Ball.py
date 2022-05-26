from lge.LittleGameEngine import LittleGameEngine
from lge.Canvas import Canvas


class Ball(Canvas):

    def __init__(self, position, size, name):
        super().__init__(position, size, name)

        self.lge = LittleGameEngine.getInstance()
        self.enableCollider(True)
        self.fill((255, 255, 255))
        self.initX, self.initY = position
        self.speedX = 180
        self.speedY = 180

    # @Override
    def onUpdate(self, dt):
        x, y = self.getPosition()
        dx = self.speedX * dt
        dy = self.speedY * dt

        self.setPosition(x + dx, y + dy)

    # @Override
    def onPostUpdate(self, dt):
        gobjs = self.lge.collidesWith(self)
        if(gobjs):
            x, y = self.getPosition()
            dx = self.speedX * dt
            dy = self.speedY * dt

            for gobj in gobjs:
                if(gobj.getTag() == "wall-horizontal"):
                    self.speedY = -self.speedY
                    dy = -dy
                if(gobj.getTag() == "paddle"):
                    self.speedX = -self.speedX
                    dx = -dx
                if(gobj.getTag() == "wall-vertical"):
                    x, y = self.initX, self.initY
            self.setPosition(x + dx, y + dy)

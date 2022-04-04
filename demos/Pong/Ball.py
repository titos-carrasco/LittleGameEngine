from lge.LittleGameEngine import LittleGameEngine
from lge.Canvas import Canvas


class Ball(Canvas):

    def __init__(self, position, size, name):
        super().__init__(position, size, name)

        self.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.SetOnEvents(LittleGameEngine.E_ON_COLLISION)
        self.UseColliders(True)
        self.Fill((255, 255, 255))
        self.init_x, self.init_y = position
        self.speed_x = 180
        self.speed_y = -180

    def OnUpdate(self, dt):
        x, y = self.GetPosition()
        dx = self.speed_x*dt
        dy = self.speed_y*dt

        self.SetPosition(x+dx, y+dy)

    def OnCollision(self, dt, gobjs):
        x, y = self.GetPosition()
        dx = self.speed_x*dt
        dy = self.speed_y*dt

        for gobj in gobjs:
            if(gobj.GetTag() == "wall-horizontal"):
                self.speed_y = -self.speed_y
                dy = -dy
            if(gobj.GetTag() == "paddle"):
                self.speed_x = -self.speed_x
                dx = -dx
            if(gobj.GetTag() == "wall-vertical"):
                x, y = self.init_x, self.init_y
        self.SetPosition(x+dx, y+dy)

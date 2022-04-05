from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class Betty(Sprite):
    def __init__(self, x, y):
        images = ["betty_idle", "betty_left", "betty_right"]

        super().__init__(images, (x, y), "Betty")

        # acceso al motor de juegos
        self.lge = self.GetLGE()

        self.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.SetOnEvents(LittleGameEngine.E_ON_COLLISION)
        self.UseColliders(True)

        self.vx = 240           # velocidad en x
        self.vy = 0             # velocidad en y
        self.vs = 360           # velocidad en y en el salto
        self.ay = 480           # aceleracion en y
        self.jumping = False

    def OnUpdate(self, dt):
        # los datos actuales
        x, y = self.GetPosition()
        action = self.GetCurrentIName()
        idx = self.GetCurrentIdx()

        # cambiamos sus coordenadas y orientacion segun la tecla presionada
        if(not self.jumping and self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_SPACE)):
            self.vy = self.vs
            self.jumping = True

        if(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
            x = x + self.vx*dt
            if(action != "betty_right"):
                self.SetShape("betty_right", 0)
        elif(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
            x = x - self.vx*dt
            if(action != "betty_left"):
                self.SetShape("betty_left", 0)
        else:
            if(action != "betty_idle"):
                self.SetShape("betty_idle", 0)
        self.NextShape(dt, 0.050)

        # caida por gravedad
        y = y + self.vy*dt
        self.vy = self.vy - self.ay*dt

        # nueva posicion
        self.SetPosition(x, y)

    def OnCollision(self, dt, gobjs):
        for gobj in gobjs:
            tag = gobj.GetTag()
            if(tag == "suelo"):
                self.jumping = False
                self.vy = 0
                self.SetPosition(self.GetX(), gobj.GetY() + gobj.GetHeight())
            elif(tag == "muerte"):
                self.lge.DelGObject(self)
                print("he muerto")

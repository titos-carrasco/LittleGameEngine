from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class Betty(Sprite):
    def __init__(self, name, win_size):
        super().__init__(["betty_idle", "betty_down", "betty_up", "betty_left", "betty_right"], (0, 0), name)

        self.lge = self.GetLGE()

        self.SetOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.SetOnEvents(LittleGameEngine.E_ON_COLLISION)
        self.SetShape("betty_idle")
        self.SetTag("Betty")
        self.UseColliders(True)
        self.alive = True
        self.win_size = win_size

    def IsAlive(self):
        return self.alive

    def SetAlive(self, alive):
        self.alive = alive
        self.SetShape("betty_idle")

    def OnUpdate(self, dt):
        # solo si estoy viva
        if(not self.alive):
            return

        # velocity = pixeles por segundo
        #velocity = 120
        #pixels = velocity*dt
        pixels = 2

        # nuestra posicion actual y tamano
        x, y = self.GetPosition()
        w, h = self.GetSize()
        self.last_point = x, y

        # cambiamos sus coordenadas e imagen segun la tecla presionada
        idx = self.GetCurrentIdx()
        if (self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
            self.SetShape("betty_right", idx)
            x = x + pixels
        elif(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
            self.SetShape("betty_left", idx)
            x = x - pixels
        elif(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_UP)):
            self.SetShape("betty_up", idx)
            y = y + pixels
        elif(self.lge.KeyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
            self.SetShape("betty_down", idx)
            y = y - pixels
        else:
            self.SetShape("betty_idle", idx)
            if (x % 32 < 4):
                x = round(x / 32) * 32
            elif (x % 32 > 28):
                x = round((x + 32) / 32) * 32
            if (y % 32 < 4):
                y = round(y / 32) * 32
            elif (y % 32 > 28):
                y = round((y + 32) / 32) * 32

        # tunel?
        if (x < -16):
            x = self.win_size[0] - 16
        elif (x > self.win_size[0] - 16):
            x = -16

        # siguiente imagen de la secuencia
        self.SetPosition(x, y)
        self.NextShape(dt, 0.1)

    def OnCollision(self, dt, gobjs):
        if(not self.alive):
            return

        for gobj in gobjs:
            if(gobj.GetTag() == "zombie"):
                self.alive = False
                print("Un zombie me mato!!!")
                return

        x, y = self.last_point
        self.SetPosition(x, y)

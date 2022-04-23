from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class Betty(Sprite):

    def __init__(self, name, winSize):
        super().__init__(["betty_idle", "betty_down", "betty_up", "betty_left", "betty_right"], (0, 0), name)

        self.lge = LittleGameEngine.getInstance()

        self.setOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.setOnEvents(LittleGameEngine.E_ON_COLLISION)
        self.setShape("betty_idle")
        self.setTag("Betty")
        self.useColliders(True)
        self.alive = True
        self.winSize = winSize

    def IsAlive(self):
        return self.alive

    def setAlive(self, alive):
        self.alive = alive
        self.setShape("betty_idle")

    def onUpdate(self, dt):
        # solo si estoy viva
        if(not self.alive):
            return

        # velocity = pixeles por segundo
        # velocity = 120
        # pixels = velocity*dt
        pixels = 2

        # nuestra posicion actual y tamano
        x, y = self.getPosition()
        w, h = self.getSize()
        self.lastPoint = x, y

        # cambiamos sus coordenadas e imagen segun la tecla presionada
        idx = self.getCurrentIdx()
        if (self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
            self.setShape("betty_right", idx)
            x = x + pixels
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
            self.setShape("betty_left", idx)
            x = x - pixels
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_UP)):
            self.setShape("betty_up", idx)
            y = y - pixels
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
            self.setShape("betty_down", idx)
            y = y + pixels
        else:
            self.setShape("betty_idle", idx)
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
            x = self.winSize[0] - 16
        elif (x > self.winSize[0] - 16):
            x = -16

        # siguiente imagen de la secuencia
        self.setPosition(x, y)
        self.nextShape(dt, 0.1)

    def onCollision(self, dt, gobjs):
        if(not self.alive):
            return

        for gobj in gobjs:
            if(gobj.getTag() == "zombie"):
                self.alive = False
                print("Un zombie me mato!!!")
                return

        x, y = self.lastPoint
        self.setPosition(x, y)

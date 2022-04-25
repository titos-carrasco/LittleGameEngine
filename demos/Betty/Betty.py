from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class Betty(Sprite):

    def __init__(self, name, winSize):
        super().__init__("betty_idle", (0, 0), name)

        self.lge = LittleGameEngine.getInstance()

        self.setOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.setOnEvents(LittleGameEngine.E_ON_COLLISION)
        self.setTag("Betty")
        self.enableCollider(True)
        self.alive = True
        self.winSize = winSize
        self.state = "I"

    def IsAlive(self):
        return self.alive

    def setAlive(self, alive):
        self.alive = alive
        self.setImage("betty_idle")

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
        if (self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
            if( self.state != "R" ):
                self.state="R"
                self.setImage("betty_right")
            x = x + pixels
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
            if( self.state != "L" ):
                self.state="L"
                self.setImage("betty_left")
            x = x - pixels
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_UP)):
            if( self.state != "U" ):
                self.state="U"
                self.setImage("betty_up")
            y = y - pixels
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_DOWN)):
            if( self.state != "D" ):
                self.state="D"
                self.setImage("betty_down")
            y = y + pixels
        else:
            if( self.state != "I" ):
                self.state="I"
                self.setImage("betty_idle")
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
        self.nextImage(dt, 0.1)

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

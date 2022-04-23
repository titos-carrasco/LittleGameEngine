from lge.LittleGameEngine import LittleGameEngine
from lge.Sprite import Sprite


class Betty(Sprite):

    def __init__(self, x, y):
        super().__init__("betty_idle", (x, y), "Betty")

        # acceso al motor de juegos
        self.lge = LittleGameEngine.getInstance()

        self.setOnEvents(LittleGameEngine.E_ON_UPDATE)
        self.setOnEvents(LittleGameEngine.E_ON_COLLISION)
        self.useColliders(True)

        self.vx = 240  # velocidad en x
        self.vy = 0  # velocidad en y
        self.vs = 360  # velocidad en y en el salto
        self.ay = 480  # aceleracion en y

        self.jumping = False

    def onUpdate(self, dt):
        # los datos actuales
        x, y = self.getPosition()
        action = self.getImagesName()

        # cambiamos sus coordenadas y orientacion segun la tecla presionada
        if(not self.jumping and self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_SPACE)):
            self.vy = -self.vs
            self.jumping = True

        if(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_RIGHT)):
            x = x + self.vx * dt
            if(action != "betty_right"):
                self.setImage("betty_right", 0)
        elif(self.lge.keyPressed(LittleGameEngine.CONSTANTS.K_LEFT)):
            x = x - self.vx * dt
            if(action != "betty_left"):
                self.setImage("betty_left", 0)
        else:
            if(action != "betty_idle"):
                self.setImage("betty_idle", 0)
        self.nextImage(dt, 0.050)

        # caida por gravedad
        y = y + self.vy * dt
        self.vy = self.vy + self.ay * dt

        # nueva posicion
        self.setPosition(x, y)

    def onCollision(self, dt, gobjs):
        for gobj in gobjs:
            tag = gobj.getTag()
            if(tag == "suelo"):
                self.jumping = False
                self.vy = 0
                self.setPosition(self.getX(), gobj.getY() - self.getHeight())
            elif(tag == "muerte"):
                self.lge.delGObject(self)
                print("he muerto")

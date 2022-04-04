import uuid
from lge.Rectangle import Rectangle


class GameObject():
    def __init__(self, position, size, name=None):
        """
        Crea un objeto del juego en la posicion y dimensiones especificadas

        - position: (x, y)
        - size: (width, height)
        - name: (opcional) nombre de este objeto
        """
        self.rect = Rectangle(position, size)
        self.name = "__noname__-" + uuid.uuid4().hex if name is None else name
        self.surface = None
        self.bounds = None
        self.tag = ""
        self.use_colliders = False
        self.layer = -1
        self.on_events_enabled = 0x00

    def GetPosition(self):
        """
        Retorna la posicion (x, y) de este objeto
        """
        return self.rect.x, self.rect.y

    def GetX(self):
        """
        Retorna la coordenada X de este objeto
        """
        return self.rect.x

    def GetY(self):
        """
        Retorna la coordenada Y de este objeto
        """
        return self.rect.y

    def GetSize(self):
        """
        Retorna la dimension (width, height) de este objeto
        """
        return self.rect.width, self.rect.height

    def GetWidth(self):
        """
        Retorna el ancho de este objeto
        """
        return self.rect.width

    def GetHeight(self):
        """
        Retorna el alto de este objeto
        """
        return self.rect.height

    def GetRectangle(self):
        """
        Retorna el rectangulo que rodea a este objeto
        """
        return self.rect.Copy()

    def GetName(self):
        """
        Retorna el nombre de este objeto
        """
        return self.name

    def GetTag(self):
        """
        Retorna el TAG de este objeto
        """
        return self.tag

    def SetBounds(self, bounds):
        """
        Establece el rectangulo que limita el movimiento de este objeto
        """
        self.bounds = bounds.Copy()

    def SetPosition(self, x, y):
        """
        Establece la posicion (x, y) de este objeto
        """
        self.rect.SetOrigin(x, y)
        if (self.bounds == None):
            return

        if (self.rect.width <= self.bounds.width and self.rect.height <= self.bounds.height):
            if (self.rect.x < self.bounds.x):
                self.rect.x = self.bounds.x
            elif (self.rect.x + self.rect.width >= self.bounds.x + self.bounds.width):
                self.rect.x = self.bounds.x + self.bounds.width - self.rect.width
            if (self.rect.y < self.bounds.y):
                self.rect.y = self.bounds.y
            elif (self.rect.y + self.rect.height >= self.bounds.y + self.bounds.height):
                self.rect.y = self.bounds.y + self.bounds.height - self.rect.height

    def SetTag(self, tag):
        """
        Establece el TAG para este objeto
        """
        self.tag = tag

    def UseColliders(self, enabled):
        """
        Establece si este objeto participara o no del procesamiento de colisiones
        """
        self.use_colliders = enabled

    # manejo de eventos
    def SetOnEvents(self, on_events_enabled):
        """
        Establece los eventos que recibira este objeto
        """
        self.on_events_enabled |= on_events_enabled

    def OnDelete(self):
        """
        Redefinir si es que se procesara este evento
        """
        pass

    def OnStart(self):
        """
        Redefinir si es que se procesara este evento
        """
        pass

    def OnPreUpdate(self, dt):
        """
        Redefinir si es que se procesara este evento
        """
        pass

    def OnUpdate(self, dt):
        """
        Redefinir si es que se procesara este evento
        """
        pass

    def OnPostUpdate(self, dt):
        """
        Redefinir si es que se procesara este evento
        """
        pass

    def OnCollision(self, dt, gobjs):
        """
        Redefinir si es que se procesara este evento
        """
        pass

    def OnPreRender(self, dt):
        """
        Redefinir si es que se procesara este evento
        """
        pass

    def OnQuit(self):
        """
        Redefinir si es que se procesara este evento
        """
        pass

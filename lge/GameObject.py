import uuid
from lge.Rectangle import Rectangle


class GameObject():
    def __init__(self, position, size, name=None):
        self.rect = Rectangle(position, size)
        self.name = "__noname__-" + uuid.uuid4().hex if name is None else name
        self.surface = None
        self.bounds = None
        self.tag = ""
        self.use_colliders = False
        self.layer = -1
        self.on_events_enabled = 0x00

    def GetPosition(self):
        return self.rect.x, self.rect.y

    def GetX(self):
        return self.rect.x

    def GetY(self):
        return self.rect.y

    def GetSize(self):
        return self.rect.width, self.rect.height

    def GetWidth(self):
        return self.rect.width

    def GetHeight(self):
        return self.rect.height

    def GetRectangle(self):
        return self.rect.Copy()

    def GetName(self):
        return self.name

    def GetTag(self):
        return self.tag

    def SetBounds(self, bounds):
        self.bounds = bounds.Copy()

    def SetPosition(self, x, y):
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
        self.tag = tag

    def UseColliders(self, enabled):
        self.use_colliders = enabled

    # manejo de eventos
    def SetOnEvents(self, on_events_enabled):
        self.on_events_enabled = on_events_enabled

    def OnDelete(self):
        pass

    def OnStart(self):
        pass

    def OnPreUpdate(self, dt):
        pass

    def OnUpdate(self, dt):
        pass

    def OnPostUpdate(self, dt):
        pass

    def OnCollision(self, dt, gobjs):
        pass

    def OnPreRender(dt):
        pass

    def OnQuit():
        pass

from lge.GameObject import GameObject
from lge.LittleGameEngine import LittleGameEngine


class Sprite(GameObject):
    def __init__(self, inames, position, name=None):
        super().__init__(position, (1, 1), name)

        self.surfaces = {}
        if(not isinstance(inames, list)):
            inames = [inames]
        for iname in inames:
            self.surfaces[iname] = LittleGameEngine.GetLGE().GetImages(iname)

        self.iname = list(self.surfaces.keys())[0]
        self.idx = 0
        self.elapsed = 0

        self.surface = self.surfaces[iname][0]
        width, height = self.surface.get_rect().size
        self.rect.SetSize(width, height)

    def GetCurrentIName(self):
        return self.iname

    def GetCurrentIdx(self):
        return self.idx

    def NextShape(self, dt, delay=0):
        self.elapsed = self.elapsed + dt
        if(self.elapsed < delay):
            return

        self.elapsed = 0
        self.idx = self.idx + 1
        if(self.idx >= len(self.surfaces[self.iname])):
            self.idx = 0

        self.surface = self.surfaces[self.iname][self.idx]
        width, height = self.surface.get_rect().size
        self.rect.SetSize(width, height)

    def SetShape(self, iname, idx):
        self.iname = iname
        if(idx >= len(self.surfaces[iname])):
            idx = 0
        self.idx = 0
        self.surface = self.surfaces[iname][idx]
        width, height = self.surface.get_rect().size
        self.rect.SetSize(width, height)

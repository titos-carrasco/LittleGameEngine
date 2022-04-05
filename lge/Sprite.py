from lge.LittleGameEngine import LittleGameEngine
from lge.GameObject import GameObject


class Sprite(GameObject):
    def __init__(self, inames, position, name=None):
        """
        Crea un objeto animado en la posicion (x, y) especificadas

        - `iname`: nombre o nombres de las secuencias de imagenes a utilizar con este Sprite.
          Las secuencias de imagenes son cargadas con el metodo **LoadImage** de **LittleGameMachine**.
            - **"nombre"**: identificador de la secuencia de imagenes de la animacion
            - **[ "nombre", "nombre", ... ]**: lista de identificador de secuencias de imagenes a utilizar en la animacion
        - `position`: posicion en donde se encontrara este Sprite
        - `name`: nombre de este Sprite
        """
        super().__init__(position, (1, 1), name)

        self.surfaces = {}
        if(not isinstance(inames, list)):
            inames = [inames]
        for iname in inames:
            self.surfaces[iname] = self._lge.GetImages(iname)

        self.iname = list(self.surfaces.keys())[0]
        self.idx = 0
        self.elapsed = 0

        self.surface = self.surfaces[iname][0]
        width, height = self.surface.get_rect().size
        self.rect.SetSize(width, height)

    def GetCurrentIName(self):
        """
        Retorna el nombre de la secuencia actual de imagenes que utiliza este Sprite
        """
        return self.iname

    def GetCurrentIdx(self):
        """
        Retorna el indice de la secuencia actual de imagenes que utiliza este Sprite
        """
        return self.idx

    def NextShape(self, dt=0, delay=0):
        """
        Avanza automaticamente a la siguiente imagen de la secuencia de este Sprite

        - dt: es el tiempo transcurrido desde la ultima invocacion
        - delay: es el tiempo que debe transcurrir antes de pasar a la siguiente imagen de la secuencia
        """
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

    def SetShape(self, iname, idx=0):
        """
        Establece la secuencia (iname) a utilizar en este Sprite

        - idx: es el indice de la secuencia a utilizar
        """
        self.iname = iname
        if(idx >= len(self.surfaces[iname])):
            idx = 0
        self.idx = idx
        self.surface = self.surfaces[iname][idx]
        width, height = self.surface.get_rect().size
        self.rect.SetSize(width, height)

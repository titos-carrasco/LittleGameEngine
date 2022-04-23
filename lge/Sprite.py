"""
Clase para manejar GameObjects animados

@author Roberto carrasco (titos.carrasco@gmail.com)
"""

from lge.LittleGameEngine import LittleGameEngine
from lge.GameObject import GameObject


class Sprite(GameObject):

    def __init__(self, iname, position:tuple, name:str=None):
        """
        Crea un GameObject con la secuencia de imagenes a utilizar

        **Parametros**
        : *iname* : nombre de la secuencia de imagenes a utilizar (puede ser None)
        : *position* : posicion inicial (x, y) del este Sprite
        : *name* : nombre a asignar a este Sprite (opcional)
        """
        super().__init__(position, (1, 1), name)

        self.surface = None
        self.surfaces = None
        self.iname = None
        self.idx = 0
        self.elapsed = 0

        self.setImage(iname)

    def getImagesName(self):
        """
        retorna el nombre de la secuencia de imagenes en uso

        **Retorna**
        : *str* : el nombre de la secuencia actual
        """
        return self.iname

    def nextImage(self, dt:float=0, delay:float=0):
        """
        Avanza a la siguiente imagen de la secuencia
        
        nextImage() avanza a la siguiente imagen
        nextImage(dt, 0.10) avanza a la siguiente imagen cuando la suma de los dt supere a delay

        **Parametros**
        : *dt* : tiempo transcurrido desde la ultima invocacion a este metodo
        : *delay* : tiempo que debe transcurrir antes de pasar a la siguiente imagen de la secuencia
        """
        self.elapsed = self.elapsed + dt
        if(self.elapsed < delay):
            return
        self.elapsed = 0

        self.idx = self.idx + 1
        if(self.idx >= len(self.surfaces)):
            self.idx = 0

        self.surface = self.surfaces[self.idx]
        width, height = self.surface.get_rect().size
        self.rect.setSize(width, height)

    def setImage(self, iname:str, idx:int=0):
        """
        Establece la secuencia de imagenes a utilizar

        **Parametros**
        : *iname* : nombre de la secuencia de imagenes a utilizar
        : *idx* : indice dentro de la secuencia de imagenes para especificar que imagen utilizar
        """
        if(not iname is None):
            if(self.iname != iname):
                self.surfaces = LittleGameEngine.getInstance().getImages(iname)
                self.iname = iname

            if(idx >= len(self.surfaces)):
                idx = 0
            self.idx = idx

            self.surface = self.surfaces[idx]
            width, height = self.surface.get_rect().size
            self.rect.setSize(width, height)

            self.elapsed = 0


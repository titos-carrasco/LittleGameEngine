"""
Clase para manejar GameObjects animados

@author Roberto carrasco (titos.carrasco@gmail.com)
"""

from lge.LittleGameEngine import LittleGameEngine
from lge.GameObject import GameObject


class Sprite(GameObject):

    def __init__(self, inames, position, name=None):
        """
        Crea un GameObject animado con las secuencias de imagenes cargadas con LittleGameEngine.LoadImage()

        Parametros:
            - string inames : si es un string corresponde al nombre de la secuencia a utilizar
            - list inames : si es una lista corresponde a los nombres de las secuencias a utilizar (seleccionable con SetShape() )
            - tuple position : posicion inicial (x, y) del este Sprite
            - string name : nombre a asignar a este objeto (opcional)77
        """
        super().__init__(position, (1, 1), name)

        self.surfaces = {}
        if(not isinstance(inames, list)):
            inames = [inames]
        for iname in inames:
            self.surfaces[iname] = LittleGameEngine.getInstance().getImages(iname)

        self.iname = list(self.surfaces.keys())[0]
        self.idx = 0
        self.elapsed = 0

        self.surface = self.surfaces[iname][0]
        width, height = self.surface.get_rect().size
        self.rect.setSize(width, height)

    def getCurrentIName(self):
        """
        Retorna el nombre de la secuencia actual de imagenes que utiliza este Sprite

        Retorna:
            - string : el nombre de la secuencia
        """
        return self.iname

    def getCurrentIdx(self):
        """
        Retorna el indice de la secuencia actual de imagenes que utiliza este Sprite

        Retorna:
            - int : el numero de la imagen dentro de la secuencia actual
        """
        return self.idx

    def nextShape(self, dt=0, delay=0):
        """
        Avanza automaticamente a la siguiente imagen de la secuencia de este Sprite

        Parametros:
            - double dt: tiempo transcurrido desde la ultima invocacion a este metodo
            - double delay: tiempo que debe transcurrir antes de pasar a la siguiente imagen de la secuencia
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
        self.rect.setSize(width, height)

    def setShape(self, iname, idx=0):
        """
        Establece la secuencia de imagenes a utilizar en este Sprite

        Parametros:
            - string iname : el nombre de la secuencia (cargada con LoadImage y especificada al crear este Sprite)
            - int idx: el numero de la secuencia a utilizar
        """
        self.iname = iname
        if(idx >= len(self.surfaces[iname])):
            idx = 0
        self.idx = idx
        self.surface = self.surfaces[iname][idx]
        width, height = self.surface.get_rect().size
        self.rect.setSize(width, height)

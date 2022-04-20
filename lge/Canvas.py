"""
GameObject para trazar formas en LittleGameObject

@autor oberto carrasco (titos.carrasco@gmail.com)
"""

import pygame

from lge.LittleGameEngine import LittleGameEngine
from lge.GameObject import GameObject


class Canvas(GameObject):

    def __init__(self, position, size, name=None):
        """
        Crea un canvas, para dibujar, en la posicion y dimensiones dadas

        Parametros:
            - tupla position : posicion (x, y) del canvas
            - tupla size : dimension (width, height) del canvas
            - string name : nombre para esta GameObject (opcional)
        """
        super().__init__(position, size, name)
        width, height = size
        self.surface = LittleGameEngine.getInstance().createTranslucentImage(width, height)

    def fill(self, color):
        """
        Colorea el canvas con el color especificado

        Parametros:
            - tupla color : color de relleno (r,g,b,a). El alpha es opcional
        """
        self.surface.fill(color)

    def drawText(self, text, position, fname, fcolor):
        """
        Traza un texto en este canvas en la posicion, tipo de letra y color especificados

        Parametros:
            - string text : el texto a trazar
            - tuple position : coordenada (x, y) en donde se trazara el texto dentro del canvas
            - string fname : nombre del font (cargado con LoadFont) a utilizar para trazar el texto
            - tuple fcolor : color a utilizar (r,g,b) para trazar el texto
        """
        x, y = position

        s = LittleGameEngine.getInstance().fonts[fname].render(text, True, fcolor)
        self.surface.blit(s, (x, self.rect.height - s.get_height() - y))

    def drawPoint(self, position, color):
        """
        Traza un punto en este canvas en la posicion y color especificados

        Parametros:
            - tuple position : coordenada (x, y) en donde se trazara el punto dentro del canvas
            - tuple color : color a utilizar (r,g,b) para trazar el punto
        """
        x, y = position
        y = self.rect.height - y

        pygame.draw.circle(self.surface, color, (x, y), 0, 0)

    def drawCircle(self, position, radius, color, thickness=False):
        """
        Traza un circulo en este canvas en la posicion, de radio y color especificado

        Parametros:
            - tuple position : coordenada (x, y) en donde se trazara el circulo dentro del canvas
            - int radio : radio del circulo a trazar
            - tuple color : color a utilizar (r,g,b) para trazar el circulo
            - bool thickness : si es True se mostrara el borde del circulo
        """
        x, y = position
        y = self.rect.height - y
        thickness = 1 if thickness else 0

        pygame.draw.circle(self.surface, color, (x, y), radius, thickness)

    def drawRectangle(self, position, size, color, thickness=False):
        """
        Traza un rectangulo en este canvas en la posicion, dimensiones y color especificado

        Parametros:
            - tuple position : coordenada (x, y) en donde se trazara el circulo dentro del canvas
            - tuple size : dimension (width, height) del rectangulo
            - tuple color : color a utilizar (r,g,b) para trazar el rectangulo
            - bool thickness : si es True se mostrara el borde del rectangulo
        """
        x, y = position
        w, h = size
        y = self.rect.height - h - y
        thickness = 1 if thickness else 0

        pygame.draw.rect(self.surface, color, pygame.Rect((x, y), (w, h)), thickness)

    def drawSurface(self, position, surface):
        """
        Traza una superficie en este canvas en la posicion dada

        Parametros:
            - tuple position : coordenada (x, y) en donde se trazara la superfice dentro del canvas
            - surface surface : superficie (imagen) a trazar. Puede ser creada con pygame.surfarray.make_surface()
        """
        x, y = position
        w, h = surface.get_size()
        y = self.rect.height - h - y

        self.surface.blit(surface, (x, y))

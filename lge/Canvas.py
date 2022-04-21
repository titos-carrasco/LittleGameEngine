"""
GameObject para trazar formas en Little Game Engine

@autor Roberto carrasco (titos.carrasco@gmail.com)
"""

import pygame

from lge.LittleGameEngine import LittleGameEngine
from lge.GameObject import GameObject


class Canvas(GameObject):

    def __init__(self, position:tuple, size:tuple, name:str=None):
        """
        Crea un canvas, para dibujar, en la posicion y de dimensiones dadas

        **Parametros**
        : *position* : posicion (x, y) del canvas
        : *size* : dimension (width, height) del canvas
        : *name* : nombre para esta GameObject (opcional)
        """
        super().__init__(position, size, name)
        width, height = size
        self.surface = LittleGameEngine.getInstance().createTranslucentImage(width, height)

    def fill(self, color:tuple):
        """
        Colorea el canvas con el color especificado

        **Parametros**
        : *color* : color de relleno (r,g,b,a). El alpha es opcional
        """
        self.surface.fill(color)

    def drawText(self, text:str, position:tuple, fname:str, fcolor:tuple):
        """
        Traza un texto en este canvas en la posicion, tipo de letra y color especificados

        **Parametros:**
        : *text* : el texto a trazar
        : *position* : coordenada (x, y) en donde se trazara el texto dentro del canvas
        : *fname* : nombre del font (cargado con LoadFont) a utilizar para trazar el texto
        : *fcolor* : color a utilizar (r,g,b) para trazar el texto
        """
        x, y = position

        s = LittleGameEngine.getInstance().fonts[fname].render(text, True, fcolor)
        self.surface.blit(s, (x, self.rect.height - s.get_height() - y))

    def drawPoint(self, position:tuple, color:tuple):
        """
        Traza un punto en este canvas en la posicion y color especificados

        **Parametros:**
        : *position* : coordenada (x, y) en donde se trazara el punto dentro del canvas
        : *color* : color a utilizar (r,g,b) para trazar el punto
        """
        x, y = position
        y = self.rect.height - y

        pygame.draw.circle(self.surface, color, (x, y), 0, 0)

    def drawCircle(self, position:tuple, radius:float, color:tuple, thickness:bool=False):
        """
        Traza un circulo en este canvas en la posicion, de radio y color especificado

        **Parametros:**
        : *position* : coordenada (x, y) en donde se trazara el circulo dentro del canvas
        : *radio* : radio del circulo a trazar
        : *color* : color a utilizar (r,g,b) para trazar el circulo
        : *thickness* : si es True se mostrara el borde del circulo
        """
        x, y = position
        y = self.rect.height - y
        thickness = 1 if thickness else 0

        pygame.draw.circle(self.surface, color, (x, y), radius, thickness)

    def drawRectangle(self, position:tuple, size:tuple, color:tuple, thickness:bool=False):
        """
        Traza un rectangulo en este canvas en la posicion, dimensiones y color especificado

        **Parametros**
        : *position* : coordenada (x, y) en donde se trazara el circulo dentro del canvas
        : *size* : dimension (width, height) del rectangulo
        : *color* : color a utilizar (r,g,b) para trazar el rectangulo
        : *thickness* : si es True se mostrara el borde del rectangulo
        """
        x, y = position
        w, h = size
        y = self.rect.height - h - y
        thickness = 1 if thickness else 0

        pygame.draw.rect(self.surface, color, pygame.Rect((x, y), (w, h)), thickness)

    def drawSurface(self, position, surface):
        """
        Traza una superficie en este canvas en la posicion dada

        **Parametros**
        : *position* : coordenada (x, y) en donde se trazara la superfice dentro del canvas
        : *surface* : superficie (imagen) a trazar. Puede ser creada con pygame.surfarray.make_surface()
        """
        x, y = position
        w, h = surface.get_size()
        y = self.rect.height - h - y

        self.surface.blit(surface, (x, y))

import pygame

from lge.LittleGameEngine import LittleGameEngine
from lge.GameObject import GameObject


class Canvas(GameObject):
    def __init__(self, position, size, name=None):
        """
        Crea un objeto, para dibujar, en la posicion (x, y) y dimensiones(width, height) especificadas
        """
        super().__init__(position, size, name)
        width, height = size
        self.surface = self._lge.CreateTranslucentImage(width, height)

    def Fill(self, color):
        """
        Colorea este canvas con el color (r,g,b,[a]) especificados
        """
        self.surface.fill(color)

    def DrawText(self, text, position, fname, fcolor):
        """
        Traza un texto en este canvas en la posicion (x, y), tipo de letra y color especificados
        """
        x, y = position

        s = self._lge.fonts[fname].render(text, True, fcolor)
        self.surface.blit(s, (x, self.rect.height - s.get_height() - y))

    def DrawPoint(self, position, color):
        """
        Traza un punto en este canvas en la posicion (x, y) y color especificados
        """
        x, y = position
        y = self.rect.height - y

        pygame.draw.circle(self.surface, color, (x, y), 0, 0)

    def DrawCircle(self, position, radius, color, thickness=False):
        """
        Traza un circulo en este canvas en la position (x, y), de radio y color especificado

        Si 'thickness' es True se mostrara el borde del circulo
        """
        x, y = position
        y = self.rect.height - y
        thickness = 1 if thickness else 0

        pygame.draw.circle(self.surface, color, (x, y), radius, thickness)

    def DrawRectangle(self, position, size, color, thickness=False):
        """
        Traza un rectangulo en este canvas en la posicion (x, y), de dimensiones (width, height) y color especificado

        Si 'thickness' es True se mostrara el borde del rectangulo
        """
        x, y = position
        w, h = size
        y = self.rect.height - h - y
        thickness = 1 if thickness else 0

        pygame.draw.rect(self.surface, color, pygame.Rect((x, y), (w, h)), thickness)

    def DrawSurface(self, position, surface):
        """
        Traza una superficie en este canvas en la posicion (x, y ) dada
        """
        x, y = position
        w, h = surface.get_size()
        y = self.rect.height - h - y

        self.surface.blit(surface, (x, y))

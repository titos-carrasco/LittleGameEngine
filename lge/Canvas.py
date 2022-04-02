import pygame
from lge.LittleGameEngine import LittleGameEngine
from lge.GameObject import GameObject


class Canvas(GameObject):
    def __init__(self, position, size, name=None):
        super().__init__(position, size, name)
        self.lge = LittleGameEngine.GetLGE()
        width, height = size
        self.surface = self.lge.CreateTranslucentImage(width, height)

    def Fill(self, color):
        self.surface.fill(color)

    def DrawText(self, text, position, fname, fcolor):
        x, y = position

        s = self.lge.fonts[fname].render(text, True, fcolor)
        self.surface.blit(s, (x, self.rect.height - s.get_height() - y))

    def DrawPoint(self, position, color):
        x, y = position
        y = self.rect.height - y

        pygame.draw.circle(self.surface, color, (x, y), 0, 0)

    def DrawCircle(self, position, radius, color, thickness=False):
        x, y = position
        y = self.rect.height - y
        thickness = 1 if thickness else 0

        pygame.draw.circle(self._surface, color, (x, y), radius, thickness)

    def DrawRectangle(self, position, size, color, thickness=False):
        x, y = position
        w, h = size
        y = self.rect.height - h - y
        thickness = 1 if thickness else 0

        pygame.draw.rect(self.surface, color, pygame.Rect((x, y), (w, h)), thickness)

    def DrawSurface(self, position, surface):
        x, y = position
        w, h = surface.get_size()
        y = self.rect.height - h - y

        self._surface.blit(surface, (x, y))

"""
Manejador de Tipos de Letras en memoria

@author Roberto carrasco (titos.carrasco@gmail.com)
"""
import pygame


class FontManager():

    def __init__(self):
        self.fonts = {}
        pygame.font.init()

    # ------ fonts ------
    def loadSysFont(self, name:str, fname:str, fstyle:tuple, fsize:int):
        """
         Carga un tipo de letra para ser utilizado en el juego

        **Parametros**
        : *name* : nombre interno a asignar
        : *fname* : nombre del tipo de letra
        : *fstyle* : estilo de letra (bold, italic)
        : *fsize* : tamano del tipo de letra
        """
        if(not name in self.fonts):
            bold, italic = fstyle
            font = pygame.font.SysFont(fname, fsize, bold, italic)
            self.fonts[name] = font

    def loadTTFont(self, name:str, fname:str, fstyle:tuple, fsize:int):
        """
         Carga un tipo de letra True Type para ser utilizado en el juego

        **Parametros**
        : *name* : nombre interno a asignar
        : *fname* : nombre del archivo que contiene la fuente TTF
        : *fstyle* : estilo de letra (bold, italic)
        : *fsize* : tamano del tipo de letra
        """
        if(not name in self.fonts):
            bold, italic = fstyle
            font = pygame.font.Font(fname, fsize)
            self.fonts[name] = font

    def getFont(self, fname:str):
        """
        Recupera un tipo de letra previamente cargado

        **Parametros**
        : *fname* : el nombre del tipo de letra a recuperar

        **Retorna**
        : *pygame.Font* : el tipo de letra
        """
        return self.fonts[fname]

    def getSysFonts(self) -> list:
        """
        Obtiene los tipos de letra del sistema

        **Retorna**
        : *list* : los tipos de letra
        """
        return pygame.font.get_fonts()

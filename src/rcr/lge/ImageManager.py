"""
La camara de Little Game Engine

@author Roberto carrasco (titos.carrasco@gmail.com)
"""
from glob import glob
import pygame


class ImageManager():

    def __init__(self):
        self.images = {}

    def getImages(self, iname) -> list:
        """
        Recupera un grupo de imagenes previamente cargadas

        **Parametros**
        : *iname* : el nombre asignado al grupo de imagenes

        **Retorna**
        : *list* : las imagenes
        """
        return [image for image in self.images[iname]]

    def loadImages(self, iname:str, pattern:str, scale=None, flip:list=None):
        """
        Cara una imagen o grupo de imagenes desde archivos para ser utilizadas en el
        juego

        **Parametros**
        : *iname* : nombre a asignar a la imagen o grupo de imagenes cargados
        : *pattern* : nombre del archivo de imagenes a cargar. Si contiene un '\*' se
                      cargaran todas las imagenes con igual nombre utilizando dicho
                      caracter como caracter comodin de busqueda (ej.imagen_0*.png)
        : *scale* : si es un float corresponde al factor de escala a aplicar a la imagen cargada
        : *scale* : si es una tupla (width, height) corresponde al nuevo tamano de la imagen cargada
        : *flip* : (true, true) para invertir la imagen en el eje X e Y
        """
        if("*" in pattern):
            fnames = sorted(glob(pattern))
        else:
            fnames = [pattern]

        if(flip):
            fx, fy = flip

        surfaces = []
        for fname in fnames:
            surface = pygame.image.load(fname).convert_alpha()
            if(scale):
                if(not isinstance(scale, tuple)):
                    w, h = surface.get_size()
                    scale = (int(w * scale), int(h * scale))
                surface = pygame.transform.smoothscale(surface, scale)
            if(flip):
                surface = pygame.transform.flip(surface, fx, fy)
            surfaces.append(surface)
        self.images[iname] = surfaces

    def createOpaqueImage(width:int, height:int) -> pygame.Surface:
        """
        Crea una imagen sin transparencia de dimensiones dadas

        **Parametros**
        : *width* : ancho deseado
        : *height* : alto deseado

        **Retorna**
        : *pygame.Surface* : la imagen creada
        """
        return pygame.Surface((width, height))

    def createTranslucentImage(width, height):
        """
        Crea una imagen con transparencia de dimensiones dadas

        **Parametros**
        : *width* : ancho deseado
        : *height* : alto deseado

        **Retorna**
        : *pygame.Surface* : la imagen creada
        """
        return pygame.Surface((width, height), pygame.SRCALPHA)

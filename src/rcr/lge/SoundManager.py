"""
La camara de Little Game Engine

@author Roberto carrasco (titos.carrasco@gmail.com)
"""
import pygame


class SoundManager():

    def __init__(self):
        self.sounds = {}
        pygame.mixer.init()

    def loadSound(self, name:str, fname:str):
        """
        Carga un archivo de sonido para ser utilizado durante el juego

        **Parametros**
        : *name* :  nombre a asignar al sonido
        : *fname* : nombre del archivo que contiene el sonido
        """
        self.sounds[name] = pygame.mixer.Sound(fname)

    def playSound(self, name:str, loop:int, level:float=50):
        """
        Inicia la reproduccion de un sonido

        **Parametros**
        :  *name* : el sonido (previamente cargado) a reproducir
        : *loop* : el numero de veces a repetirlo
        : *level* : el nivel de volumen (0-100)
        """
        if(loop): loop = -1
        else: loop = 0

        if(level < 0): level = 0
        elif(level > 100): level = 100

        self.sounds[name].set_volume(level / 100)
        self.sounds[name].play(loop)

    def stopSound(self, name:str):
        """
        Detiene la reproduccion de un sonido

        **Parametros**
        : *name* : el nombre del sonido a detener
        """
        self.sounds[name].stop()

    def setSoundVolume(self, name:str, level:float):
        """
        Establece el volumen de un sonido previamente cargado

        **Paranmetros**
        : *name* :  el nombre del sonido
        : *level* : el nivel de volumen
        """
        if(level < 0): level = 0
        elif(level > 100): level = 100

        self.sounds[name].set_volume(level / 100)

    def getSoundVolume(self, name:str) -> float:
        """
        Obtiene el volumen de un sonido previamente cargado

        **Paranmetros**
        : *name* : el nombre del sonido


        **Retorna**
        : *float* : el nivel de volumen
        """
        return self.sounds[name].get_volume() * 100

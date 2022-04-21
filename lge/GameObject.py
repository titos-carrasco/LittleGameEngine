"""
Objeto base del juego. En Little Game Engine casi todo es un GameObject

@author Roberto carrasco (titos.carrasco@gmail.com)
"""

import uuid

from lge.Rectangle import Rectangle


class GameObject():

    def __init__(self, position:tuple, size:tuple, name:str=None):
        """
        Crea un objeto del juego en la posicion y dimensiones especificadas

        **Parametros**
        : *position* : posicion (x, y) inicial de este GameObject
        : *size* : dimension (width, height)de este GameObject
        : *name* : nombre (opcional) a asignar a este GameObject
        """
        self.rect = Rectangle(position, size)
        self.name = "__noname__-" + uuid.uuid4().hex if name is None else name
        self.surface = None
        self.bounds = None
        self.tag = ""
        self._useColliders = False
        self.layer = -1
        self.onEventsEnabled = 0x00

    def getPosition(self) -> tuple:
        """
        Retorna la posicion de este objeto

        **Retorna**
        : *tuple* : la posicion (x, y)
        """
        return self.rect.x, self.rect.y

    def getX(self) -> float:
        """
        Obtiene la coordenada X del GameObject

        **Retorna**
        : *float* : la coordenada X
        """
        return self.rect.x

    def getY(self) -> float:
        """
        Obtiene la coordenada Y del GameObject

        **Retorna**
        : *float* : la coordenada Y
        """
        return self.rect.y

    def getSize(self) -> tuple:
        """
        Retorna la dimension de este objeto

        **Retorna**
        : *tuple* : la dimension (width, height)
        """
        return self.rect.width, self.rect.height

    def getWidth(self) -> float:
        """
        Retorna el ancho de este objeto

        **Retorna**
        : *float* : el ancho
        """
        return self.rect.width

    def getHeight(self) -> float:
        """
        Retorna el alto de este objeto

        **Retorna**
        : *float* : el alto
        """
        return self.rect.height

    def getRectangle(self) -> Rectangle:
        """
        Retorna una copia del rectangulo que rodea a este objeto

        **Retorna**
        : *Rectangle* : el rectangulo
        """
        return self.rect.copy()

    def getName(self) -> str:
        """
        Retorna el nombre de este objeto

        **Retorna**
        : *str* : el nombre
        """
        return self.name

    def getTag(self) -> str:
        """
        Retorna el TAG de este objeto

        **Retorna**
        : *str* : el tag
        """
        return self.tag

    def setBounds(self, bounds:Rectangle):
        """
        Establece el rectangulo que limita el movimiento de este objeto

        **Parametros**
        : *bounds* : el rectangulo en donde se permitira mover al objeto
        """
        self.bounds = bounds.copy()

    def setPosition(self, x:float, y:float):
        """
        Establece la posicion de este objeto

        **Parametros**
        : *x* : la coordenada x
        : *y* : la coordenada y
        """
        self.rect.setOrigin(x, y)
        if (self.bounds == None):
            return

        if (self.rect.width <= self.bounds.width and self.rect.height <= self.bounds.height):
            if (self.rect.x < self.bounds.x):
                self.rect.x = self.bounds.x
            elif (self.rect.x + self.rect.width >= self.bounds.x + self.bounds.width):
                self.rect.x = self.bounds.x + self.bounds.width - self.rect.width
            if (self.rect.y < self.bounds.y):
                self.rect.y = self.bounds.y
            elif (self.rect.y + self.rect.height >= self.bounds.y + self.bounds.height):
                self.rect.y = self.bounds.y + self.bounds.height - self.rect.height

    def setTag(self, tag:str):
        """
        Establece el TAG para este objeto

        **Parametros**
        : *tag* : el tag a asignar
        """
        self.tag = tag

    def useColliders(self, enabled:bool):
        """
        Establece si este objeto participara o no del procesamiento de colisiones

        **Parametros**
        : *enabled* : si es verdadero participara del procesamiento de colisiones
        """
        self._useColliders = enabled

    # manejo de eventos
    def setOnEvents(self, onEventsEnabled:int):
        """
        Establece los eventos que recibira este objeto

        **Parametros**
        : *onEventsEnabled* : el evento que se sumara a los eventos que recibira
        
        >>
            LittleGameEngine.E_ON_DELETE
            LittleGameEngine.E_ON_START
            LittleGameEngine.E_ON_PRE_UPDATE
            LittleGameEngine.E_ON_UPDATE
            LittleGameEngine.E_ON_POST_UPDATE
            LittleGameEngine.E_ON_COLLISION
            LittleGameEngine.E_ON_PRE_RENDER
            LittleGameEngine.E_ON_QUIT

        Se deben agregar los siguientes metodos segun se habiliten los eventos:
        >>
            onDelete(self)
            onStart(self)
            onPreUpdate(self, dt:float)
            onUpdate(self, dt:float)
            onPostUpdate(self, dt:float)
            onCollision(self, dt:float, gobjs:GameObject[])
            onPreRender(self, dt:float)
            onQuit(self)
        """
        self.onEventsEnabled |= onEventsEnabled

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
        self.setCollider(Rectangle((0, 0), size))
        self.name = "__noname__-" + uuid.uuid4().hex if name is None else name
        self.surface = None
        self.bounds = None
        self.tag = ""
        self.useCollider = False
        self.callOnCollision = False
        self.layer = -1

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

    def getLayer(self) -> int:
        """
        Retorna el layer de este objeto

        **Retorna**
        : *int* : el layer
        """
        return self.layer

    def getTag(self) -> str:
        """
        Retorna el TAG de este objeto

        **Retorna**
        : *str* : el tag
        """
        return self.tag

    def getCollider(self) -> list:
        """
        Retorna la lista de rectangulos que componen el colisionador ajustada a las coordenadas de LGE

        **Retorna**
        : *list* : la lista de rectangulos
        """
        collider = []
        for r in self.collider:
            r = r.copy()
            r.x += self.rect.x
            r.y += self.rect.y
            collider.append(r)
        return collider

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

    def setCollider(self, rects):
        """
        Establece el colisionador para este objeto

        **Parametros**
        : *rects* : puede ser un Rectangulo o una lista de Rectangulos
        """
        if(isinstance(rects, Rectangle)):
            rects = [rects]
        collider = [ r.copy() for r in rects if isinstance(r, Rectangle) ]
        if(collider):
            self.collider = collider

    def enableCollider(self, enabled:bool, oncollision:bool=False):
        """
        Establece si este objeto participara o no del procesamiento de colisiones

        **Parametros**
        : *enabled* : si es verdadero participara del procesamiento de colisiones
        : *oncollision* : si es verdadero se generara el evento OnCillision para este objeto
        """
        self.useCollider = enabled
        self.callOnCollision = oncollision

    def collidesWith(self, gobj) -> bool:
        """
        Determina si este objeto colisiona con uno dado

        **Parametros**
        : *gobj* : el GameObject contra el cual se determinara la colision

        **Retorna**
        : *bool* : True si ambos objetos colisionan
        """
        if(self.layer == gobj.layer):
            for r1 in self.getCollider():
                for r2 in gobj.getCollider():
                    if(r1.intersects(r2)):
                        return True
        return False

    # manejo de eventos
    def onDelete(self):
        """
        Invocado justo despues de ser eliminado de LGE
        """

    def onStart(self):
        """
        Invocado justo despues de ser agregado a LGE
        """

    def onPreUpdate(self, dt:float):
        """
        Primera invocacion para actualizar el estado interno

        **Parametros**
        : *dt* : timepo en ms desde la ultima invocacion
        """

    def onUpdate(self, dt:float):
        """
        Segunda invocacion para actualizar el estado interno

        **Parametros**
        : *dt* : timepo en ms desde la ultima invocacion
        """

    def onPostUpdate(self, dt:float):
        """
        Tercera invocacion para actualizar el estado interno

        **Parametros**
        : *dt* : timepo en ms desde la ultima invocacion
        """

    def onCollision(self, dt:float, gobjs:list):
        """
        Ejecutada despues de todos los updates al detectar colision con otros GameObjects del layer

        **Parametros**
        : *dt* : timepo en ms desde la ultima invocacion
        """

    def onPreRender(self, dt:float):
        """
        Ejecutada justo antes de realizar el rendering en pantalla

        **Parametros**
        : *dt* : timepo en ms desde la ultima invocacion
        """

    def onQuit(self):
        """
        Invocado justo despues de que ha finalizado el Game Loop
        """

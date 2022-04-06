import uuid

from lge.Rectangle import Rectangle


class GameObject():
    def __init__(self, position, size, name=None):
        """
        Crea un objeto del juego en la posicion y dimensiones especificadas

        Parametros:
            tuple position : posicion (x, y) inicial de este GameObject
            tuple size : dimension (width, height)de este GameObject
            string name : nombre (opcional) a asignar a este GameObject
        """
        self.rect = Rectangle(position, size)
        self.name = "__noname__-" + uuid.uuid4().hex if name is None else name
        self.surface = None
        self.bounds = None
        self.tag = ""
        self._useColliders = False
        self.layer = -1
        self.onEventsEnabled = 0x00

    def getPosition(self):
        """
        Retorna la posicion (x, y) de este objeto
        """
        return self.rect.x, self.rect.y

    def getX(self):
        """
        Obtiene la coordenada X del GameObject

        Retorna:
            int : la coordenada X
        """
        return self.rect.x

    def getY(self):
        """
        Obtiene la coordenada Y del GameObject

        Retorna:
            int : la coordenada Y
        """
        return self.rect.y

    def getSize(self):
        """
        Retorna la dimension de este objeto

        Retorna:
            (int, int) : la dimension
        """
        return self.rect.width, self.rect.height

    def getWidth(self):
        """
        Retorna el ancho de este objeto

        Retorna
            int : el ancho
        """
        return self.rect.width

    def getHeight(self):
        """
        Retorna el alto de este objeto

        Retorna:
            int : el alto
        """
        return self.rect.height

    def getRectangle(self):
        """
        Retorna una copia del rectangulo que rodea a este objeto

        Retorna:
            Rectangle( x, y, width, height ) : el rectangulo
        """
        return self.rect.copy()

    def getName(self):
        """
        Retorna el nombre de este objeto

        Retorna:
            string : el nombre
        """
        return self.name

    def getTag(self):
        """
        Retorna el TAG de este objeto

        Retorna:
            string: el tag
        """
        return self.tag

    def setBounds(self, bounds):
        """
        Establece el rectangulo que limita el movimiento de este objeto

        Parametro:
            Rectangle : el rectangulo en donde se permitira mover al objeto
        """
        self.bounds = bounds.copy()

    def setPosition(self, x, y):
        """
        Establece la posicion de este objeto

        Parametro:
            int x : la coordenada x
            int y : la coordenada y
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

    def setTag(self, tag):
        """
        Establece el TAG para este objeto

        Parametro:
            string tag : el tag a asignar
        """
        self.tag = tag

    def useColliders(self, enabled):
        """
        Establece si este objeto participara o no del procesamiento de colisiones

        Parametro:
            bool enabled : si es verdadero participara del procesamiento de colisiones
        """
        self._useColliders = enabled

    # manejo de eventos
    def setOnEvents(self, onEventsEnabled):
        """
        Establece los eventos que recibira este objeto

        Parametros:
            bool onEventsEnabled : el evento que se sumara a los eventos que recibira
                                    LittleGameEngine.E_ON_DELETE
                                    LittleGameEngine.E_ON_START
                                    LittleGameEngine.E_ON_PRE_UPDATE
                                    LittleGameEngine.E_ON_UPDATE
                                    LittleGameEngine.E_ON_POST_UPDATE
                                    LittleGameEngine.E_ON_COLLISION
                                    LittleGameEngine.E_ON_PRE_RENDER
                                    LittleGameEngine.E_ON_QUIT

        Se deben agregar los siguientes metodos segun se habiliten los eventos:
            onDelete(self)
            onStart(self)
            onPreUpdate(self, dt)
            onUpdate(self, dt)
            onPostUpdate(self, dt)
            onCollision(self, dt, gobjs)
            onPreRender(self, dt)
            onQuit(self)

        """
        self.onEventsEnabled |= onEventsEnabled

class Rectangle():

    def __init__(self, origin, size):
        """
        Crea un rectangulo en el origen y dimensiones especificadas

        Parametros:
            - tuple origin: coordenadas (x, y) del origen del rectangulo
            - tuple size: dimension (width, height) del rectangulo
        """
        x, y = origin
        width, height = size
        assert width > 0 and height > 0, "'ancho/alto invalidos"

        self.x, self.y = int(x), int(y)
        self.width, self.height = int(width), int(height)

    def copy(self):
        """
        Retorna una copia de este rectangulo

        Retorna:
            - Rectangle( x, y, width, height ) : la copia
        """
        return Rectangle((self.x, self.y), (self.width, self.height))

    def getOrigin(self):
        """
        Retorna las coordenadas del origen de este rectangulo

        Retorna:
            - tuple : las coordenadas (x,y)
        """
        return self.x, self.y

    def getSize(self):
        """
        Retorna la dimension de este rectangulo

        Retorna:
            - tuple : la dimension (width,height)
        """
        return self.width, self.height

    def setOrigin(self, x, y):
        """
        Establece el origen de este rectangulo

        Parametros:
            - int x : origen en X
            - int y : origen en Y
        """
        self.x, self.y = int(x), int(y)

    def setSize(self, width, height):
        """
        Establece las dimensiones de este rectangulo

        Parametros:
            - int width : el ancho
            - int height : el alto
        """
        assert width > 0 and height > 0, "ancho/alto invalidos"
        self.width, self.height = int(width), int(height)

    def intersects(self, rect):
        """
        Determina si el rectangulo intersecta a otro

        Parametros:
            - Rectangle rect : el rectangulo sobre el cual determinar la interseccion

        Retorna:
            - bool : True si sintersectan
        """
        sx1, sx2 = self.x, self.x + self.width - 1
        sy1, sy2 = self.y, self.y + self.height - 1

        rx1, rx2 = rect.x, rect.x + rect.width - 1
        ry1, ry2 = rect.y, rect.y + rect.height - 1

        return rx1 <= sx2 and \
            sx1 <= rx2 and \
            ry1 <= sy2 and \
            sy1 <= ry2

    def contains(self, x, y):
        """
        Retorna True si las coordenadas dadas se encuentran dentro de este rectangulo

        Parametros:
            - int x : la coordenada X
            - int y : la coordenada Y

        Retorna
            - bool : True si es que el punto dado se encuentra dentro del rectangulo
        """
        return x >= self.x and x < self.x + self.width and \
            y >= self.y and y < self.y + self.height

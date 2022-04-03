class Rectangle():
    def __init__(self, origin, size):
        """
        Crea un rectangulo en el origen y dimensiones especificadas

        - origin: (x, y)
        - size: (width, height)
        """
        x, y = origin
        width, height = size
        assert width > 0 and height > 0, "'ancho/alto invalidos"

        self.x, self.y = int(x), int(y)
        self.width, self.height = int(width), int(height)

    def Copy(self):
        """
        Retorna una copia de este rectangulo
        """
        return Rectangle((self.x, self.y), (self.width, self.height))

    def GetOrigin(self):
        """
        Retorna las coordenadas (x,y) del origen de este rentangulo
        """
        return self.x, self.y

    def GetSize(self):
        """
        Retorna la dimension (width,height) de este rectangulo
        """
        return self.width, self.height

    def SetOrigin(self, x, y):
        """
        Establece el origen de este rectangulo en las coordenadas (x,y)
        """
        self.x, self.y = int(x), int(y)

    def SetSize(self, width, height):
        """
        Establece las dimensiones de este rectangulo en (width,height)
        """
        assert width > 0 and height > 0, "ancho/alto invalidos"
        self.width, self.height = int(width), int(height)

    def Intersects(self, rect):
        """
        Retorna True si este rectangulo instersecta al rectangulo dado como parametro
        """
        sx1, sx2 = self.x, self.x + self.width - 1
        sy1, sy2 = self.y, self.y + self.height - 1

        rx1, rx2 = rect.x, rect.x + rect.width - 1
        ry1, ry2 = rect.y, rect.y + rect.height - 1

        return rx1 <= sx2 and \
            sx1 <= rx2 and \
            ry1 <= sy2 and \
            sy1 <= ry2

    def Contains(self, x, y):
        """
        Retorna True si las coordenadas (x,y) se encuentran dentro de este rectangulo
        """
        return x >= self.x and x < self.x + self.width and \
            y >= self.y and y < self.y + self.height

class Rectangle():
    def __init__(self, origin, size):
        x, y = origin
        width, height = size
        assert width > 0 and height > 0, "'ancho/allto invalidos"

        self.x, self.y = int(x), int(y)
        self.width, self.height = int(width), int(height)

    def Copy(self):
        return Rectangle((self.x, self.y), (self.width, self.height))

    def GetOrigin(self):
        return self.x, self.y

    def GetSize(self):
        return self.width, self.height

    def SetOrigin(self, x, y):
        self.x, self.y = int(x), int(y)

    def SetSize(self, width, height):
        assert width > 0 and height > 0, "ancho/alto invalidos"
        self.width, self.height = int(width), int(height)

    def Intersects(self, rect):
        x1, x2 = self.x, self.x + self.width - 1
        y1, y2 = self.y, self.y + self.height - 1

        rx1, rx2 = rect.x, rect.x + rect.width - 1
        ry1, ry2 = rect.y, rect.y + rect.height - 1

        return rx1 <= x2 and x1 <= rx2 and ry1 <= y2 and y1 <= y2

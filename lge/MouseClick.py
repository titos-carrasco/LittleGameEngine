"""
Clase para manejar el clic del Mouse

@author Roberto carrasco (titos.carrasco@gmail.com)
"""


class MouseClick():

    def __init__(self):
        """
        Crear el objeto para detectar un clic del mouse
        """
        self.x = -1
        self.y = -1
        self.pushed = False

    def isClicked(self, pushed, x, y):
        """
        Detecta un clic en las coordenadas dadas
        """
        if(pushed):
            if(not self.pushed):
                self.pushed = True
                self.x = x
                self.y = y
        elif(self.pushed):
            self.pushed = False
            return self.x == x and self.y == y

        return False

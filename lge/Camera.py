from lge.GameObject import GameObject


class Camera(GameObject):

    def __init__(self, position, size):
        """
        Crea la camara en la posicion y dimensiones dadas. Esta clase es privada al motor de juegos

        Parametros:
            - tuple position : coordenadas (x, y) de la posicion inicial de la camara
            - tuple size : dimension (width, height) de la camara
        """
        super().__init__(position, size, "__LGE_CAMERA__")
        self.target = None
        self.targetInCenter = True

    def followTarget(self):
        """
        Mueve la camara segun se desplace su objetivo
        """
        # nadie a quien seguir
        if(self.target == None):
            return

        # la posicion del que seguimos
        x = self.target.rect.x
        y = self.target.rect.y

        # el centro de la camara en el centro del gobj
        if (self.targetInCenter):
            x = x + self.target.rect.width / 2
            y = y + self.target.rect.height / 2

        self.setPosition(x - self.rect.width / 2, y - self.rect.height / 2)

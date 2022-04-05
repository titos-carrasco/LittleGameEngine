from lge.GameObject import GameObject


class Camera(GameObject):
    def __init__(self, position, size):
        """
        Crea la camara en la posicion(x, y) y de dimensiones (width, height) especificadas

        Esta clase es privada
        """
        super().__init__(position, size, "__LGE_CAMERA__")
        self.target = None
        self.target_center = True

    def FollowTarget(self):
        """
        Mueve la camara para tener visible al objeto configurado
        """
        # nadie a quien seguir
        if(self.target == None):
            return

        # la posicion del que seguimos
        x = self.target.rect.x
        y = self.target.rect.y

        # el centro de la camara en el centro del gobj
        if (self.target_center):
            x = x + self.target.rect.width / 2
            y = y + self.target.rect.height / 2

        self.SetPosition(x - self.rect.width / 2, y - self.rect.height / 2)

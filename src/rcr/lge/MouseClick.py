"""
Clase para manejar el clic del Mouse

```python
lge = LittleGameEngine(...)
button = MouseClick()
while...
    mb1, mb2, mb3 = lge.getMouseButtons()
    mx, my = lge.getMousePosition()
    if(button.isClicked(mb1, mx, my)):
        hacer algo
```

@author Roberto carrasco (titos.carrasco@gmail.com)
"""


class MouseClick():

    def __init__(self):
        """
        El objeto para detectar clic del mouse
        """
        self.x = -1
        self.y = -1
        self.pushed = False

    def isClicked(self, pushed: bool, x:int , y:int) -> bool:
        """
        Detecta un clic en las coordenadas dadas (ver ejemplo anterior)

        **Parametros**
        : *pushed* : verdadero si el boton a monitorear se encuentra presionado
        : *x* : coordenada X actual del mouse
        : *y* : coordenada Y actual del mouse

        **Retorna**
         : *bool* : Verdadero si el boton se solto en las mismas coordenada en se habia presionado
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

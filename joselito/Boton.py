import pygame
class Boton():
    def __init__(self, x, y, ancho, alto, escala=3):
        self._rect = pygame.Rect(x, y, ancho*escala, alto*escala)
        self._sheet = pygame.image.load("img/button_atlas.png").convert_alpha()
        self._dimension = ancho
        self._dimension2 = alto
        self._escala = escala
        self._animaciones = {
            "3D": self.obtener_frames(0,3),
            "Pokemon": self.obtener_frames(1,3),
            "None": self.obtener_frames(2,3)
        }
        self._estado = "None"
        self._frameActual = 0


    def clickeado(self, mousepos):
        return self._rect.collidepoint(mousepos)
    
    def obtener_frames(self, fila, cantidad):
        frames = []
        for i in range(cantidad):
            cuadro = self._sheet.subsurface((i *self._dimension, fila * self._dimension2, self._dimension, self._dimension2))
            cuadrado_escalado = pygame.transform.scale(cuadro, (self._rect.width, self._rect.height))
            frames.append(cuadrado_escalado)
        return frames
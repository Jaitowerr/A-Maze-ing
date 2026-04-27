import pygame

class Player():
    def __init__(self, coordenadas: tuple[int, int], dimensiones: int):
        self._x, self._y = coordenadas
        self._dimension = dimensiones
        self._sheet = pygame.image.load("img/pacman.png").convert_alpha()
        self._animaciones = {
            "Quieto": self.obtener_frames(0, 2),
            "Izquierda": self.obtener_frames(2, 2),
            "Derecha": self.obtener_frames(0, 2),
            "Arriba": self.obtener_frames(1, 2),
            "Abajo": self.obtener_frames(3, 2)
        }
        self._estado = "Quieto"
        self._frameActual = 0

    def obtener_frames(self, fila, cantidad):
        frames = []
        for i in range(cantidad):
            cuadro = self._sheet.subsurface((i *self._dimension, fila * self._dimension, self._dimension, self._dimension))
            frames.append(cuadro)
        return frames

    def render(self, screen: pygame.Surface):
        self._frameActual += 0.1
        lista_frames = self._animaciones[self._estado]
        if self._frameActual >= len(lista_frames):
            self._frameActual = 0
        img = lista_frames[int(self._frameActual)]
        screen.blit(img, (self._x * self._dimension, self._y * self._dimension))
        #pygame.draw.rect(screen, (255,0, 0), (self._x*self._dimension, self._y*self._dimension,
        #                                       self._dimension, self._dimension))
    
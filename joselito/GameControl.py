import pygame
from Map import Map
from Player import Player

class GameControl():
    def __init__(self, mapa: Map, pj: Player):
        self._mapa = mapa
        self._player = pj
        self._estado = "Activo"
    
    def mover_jugador(self):
        tecla = pygame.key.get_pressed()
        if self._estado == "Activo":
            dx, dy = 0, 0
            if tecla[pygame.K_UP]:
                dy = -1
                self._player._estado = "Arriba"
            elif tecla[pygame.K_DOWN]:
                dy = 1
                self._player._estado = "Abajo"
            elif tecla[pygame.K_LEFT]:
                dx = -1
                self._player._estado = "Izquierda"
            elif tecla[pygame.K_RIGHT]:
                dx = 1
                self._player._estado = "Derecha"
            if dx != 0 or dy != 0:
                nuevo_x = dx + self._player._x
                nuevo_y = dy + self._player._y
                if self._mapa.celda_valida(nuevo_x, nuevo_y):
                    if self._mapa.grid[nuevo_y][nuevo_x] != 1:
                        self._player._x = nuevo_x
                        self._player._y = nuevo_y
        
    def control(self, evento: pygame.event.Event):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_m:
                self._estado = "Menu"
            elif evento.key == pygame.K_p:
                self._estado = "Activo"

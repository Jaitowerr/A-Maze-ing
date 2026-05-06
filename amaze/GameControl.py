from Mapa import Mapa
from Player import Player
class GameControl():
    def __init__(self, m, win, map: Mapa, player: Player):
        self._m = m
        self._win = win
        self._map = map
        self._player = player
        self._estado = True
    
    def set_estado(self, param):
        self._estado = param

    def move_player(self, key):
        if key == 65362 or 119:
            self._player.set_y -= 1
        elif key == 65364 or 115:
            self._player.set_y += 1
        elif key == 65361 or 97:
            self._player.set_x -= 1
        elif key == 65363 or 100:
            self._player.set_x += 1
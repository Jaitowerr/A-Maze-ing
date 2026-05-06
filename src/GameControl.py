from src.maze_generator import MazeGenerator
from .Player import Player
import traceback
class GameControl():
    def __init__(self, m, win, map:MazeGenerator, player: Player, tiles):
        self._m = m
        self._mlx = m.mlx_ptr
        self._win = win
        self._map = map
        self._player = player
        self._estado = True
        self._tiles = tiles
    
    def set_estado(self, param):
        self._estado = param

    def move_player(self, key):
        if key == 65362 or key ==119:
            self._player._y -= 1
        elif key == 65364 or key == 115:
            self._player._y += 1
        elif key == 65361 or key == 97:
            self._player._x -= 1
        elif key == 65363 or key == 100:
            self._player._x += 1

    def crear_mapa2(self):
        self._map.algoritmo()
        self._map.print_grid()
    def crear_mapa1(self):
        try:
            self._map.mark_42(self._m,self._win,self._tiles)
        except Exception as e:
            traceback.print_exc()
    
    def crear_ascii(self):
        self._map.print_maze()
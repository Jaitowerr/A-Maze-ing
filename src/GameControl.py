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
            #self._m.mlx_clear_window(self._m.mlx_ptr, self._win)
            self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
            self._player.render(self._m, self._win)
        elif key == 65364 or key == 115:
            self._player._y += 1
            #self._m.mlx_clear_window(self._m.mlx_ptr, self._win)
            self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
            self._player.render(self._m, self._win)
        elif key == 65361 or key == 97:
            self._player._x -= 1
            #self._m.mlx_clear_window(self._m.mlx_ptr, self._win)
            self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
            self._player.render(self._m, self._win)
        elif key == 65363 or key == 100:
            self._player._x += 1
            #self._m.mlx_clear_window(self._m.mlx_ptr, self._win)
            self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
            self._player.render(self._m, self._win)

    def crear_mapa2(self):
        self._map.algoritmo()
        self._m.mlx_clear_window(self._m.mlx_ptr, self._win)
        self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
    
    def crear_mapa1(self):
        self._map.cfg.algorithm = "kruskal"
        self._map.algoritmo()
        self._m.mlx_clear_window(self._m.mlx_ptr, self._win)
        self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
    
    def crear_ascii(self):
        self._map.print_maze()
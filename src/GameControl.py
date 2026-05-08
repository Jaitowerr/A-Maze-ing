from src.maze_generator import MazeGenerator
from .Player import Player
from .Direcccion import Direccion
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
        dx = 0
        dy = 0
        celda = self._map.get_cell(self._player._x, self._player._y)
        if key == 65362 or key == 119:
            if not celda.walls[Direccion.NORTE]:
                dy -= 1
        elif key == 65364 or key == 115:
            if not celda.walls[Direccion.SUR]:
                dy += 1
        elif key == 65361 or key == 97:
            if not celda.walls[Direccion.OESTE]:
                dx -= 1
        elif key == 65363 or key == 100:
            if not celda.walls[Direccion.ESTE]:
                dx += 1
        old_x = self._player._x
        old_y = self._player._y

        new_x = dx  + old_x
        new_y = dy + old_y
        self._map.redraw_tile(self._m,
                              self._mlx,
                              self._win,
                              self._tiles,
                              old_x,
                              old_y)
        self._player._x = new_x
        self._player._y = new_y
        self._player.render(self._m, self._win)
    
    def crear_mapa2(self):

        self._map.reset()
        self._map.algoritmo()
        self._map.binario()
        self._player._x, self._player._y = self._map.cfg.entry_x_y[0], self._map.cfg.entry_x_y[1]
        self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
        self._player.render(self._m, self._win)
    
    def crear_mapa1(self):
 
        self._map.cfg.algorithm = "kruskal"
        self._map.reset()
        self._map.algoritmo()
        self._map.binario()
        self._player._x, self._player._y = self._map.cfg.entry_x_y[0], self._map.cfg.entry_x_y[1]
        self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
        self._player.render(self._m, self._win)
    
    def crear_ascii(self):
        self._map.print_maze()
    
    '''
    def move_player(self, key):
        dx = 0
        dy = 0
        if key == 65362 or key ==119:
            dy -= 1
            self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
            self._player.render(self._m, self._win)
        elif key == 65364 or key == 115:
            dy += 1
            self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
            self._player.render(self._m, self._win)
        elif key == 65361 or key == 97:
            dx -= 1
            self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
            self._player.render(self._m, self._win)
        elif key == 65363 or key == 100:
            dx += 1
            self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
            self._player.render(self._m, self._win)
'''
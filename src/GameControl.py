from src.maze_generator import MazeGenerator
from .Player import Player
from .Direcccion import Direccion
import traceback
import time
class GameControl():
    def __init__(self, m, win, map:MazeGenerator, player: Player, tiles):
        self._m = m
        self._mlx = m.mlx_ptr
        self._win = win
        self._map = map
        self._player = player
        self._estado = True
        self._tiles = tiles
        self._color = [False,""]
    
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
        self._player.render(self._m, self._win, self._map)
    
    def change_color(self):
        self._map.cfg.ruta = "img2/mario/colores"
        from a_maze_ing import load_tiles
        self._tiles = load_tiles(self._m,self._mlx, self._map.cfg)
        self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
        self._player.render(self._m, self._win, self._map)
        self._color = [True,self._map.cfg.ruta]
        

    def pintar_ruta(self):
        x,y = self._map.cfg.entry_x_y
        if self._estado == True:
            self._map.cfg.ruta = "img2/mario"
            for ruta in self._map.camino:
                if ruta == "N":
                    y -= 1
                elif ruta == "S":
                    y += 1
                elif ruta == "E":
                    x += 1
                elif ruta == "O":
                    x -= 1
                inicio = self._map.get_cell(x,y)
                key = self._map.get_tile_key(inicio)
                tile,_,_ = self._m.mlx_png_file_to_image(self._mlx,f"../{self._map.cfg.ruta}/camino/{key}.png")
                self._m.mlx_put_image_to_window(self._mlx,self._win,tile,x*self._map.cfg.pixel,y*self._map.cfg.pixel)
                self._estado = False
        else:
            for ruta in self._map.camino:
                if ruta == "N":
                    y -= 1
                elif ruta == "S":
                    y += 1
                elif ruta == "E":
                    x += 1
                elif ruta == "O":
                    x -= 1
                inicio = self._map.get_cell(x,y)
                key = self._map.get_tile_key(inicio)
                if self._color[0] == True:
                    self._map.cfg.ruta = self._color[1]
                tile,_,_ = self._m.mlx_png_file_to_image(self._mlx,f"../{self._map.cfg.ruta}/{key}.png")
                self._m.mlx_put_image_to_window(self._mlx,self._win,tile,x*self._map.cfg.pixel,y*self._map.cfg.pixel)
                self._estado = True
        img = self._tiles["exit"]
        x,y = self._map.cfg.exit_x_y
        x = x*self._map.cfg.pixel
        y = y*self._map.cfg.pixel
        self._m.mlx_put_image_to_window(self._mlx, self._win, img, x-(len(self._map.grid_binario[0])//2)+ self._map.cfg.pixel//4, y-(len(self._map.grid_binario)//2)+ self._map.cfg.pixel//4)
        self._player.render(self._m, self._win, self._map)


    def crear_mapa2(self):

        self._map.reset()
        self._map.algoritmo()
        self._map.binario()
        self._player._x, self._player._y = self._map.cfg.entry_x_y[0], self._map.cfg.entry_x_y[1]
        self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
        self._player.render(self._m, self._win, self._map)
        self._map.hexadecimal()
        self._map.shortest_path()
        print(self._map.camino)
    
    def crear_mapa1(self):
 
        self._map.cfg.algorithm = "kruskal"
        self._map.reset()
        self._map.algoritmo()
        self._map.binario()
        self._player._x, self._player._y = self._map.cfg.entry_x_y[0], self._map.cfg.entry_x_y[1]
        self._map.draw_maze(self._m,self._m.mlx_ptr, self._win, self._tiles)
        self._player.render(self._m, self._win, self._map)
        self._map.hexadecimal()
        self._map.shortest_path()
    
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
from .maze_generator import MazeGenerator
class Player():
    def __init__(self, direction: tuple[int,int], img):
        self._x, self._y = direction
        self._img = img

    def render(self, m, win, map: MazeGenerator):
        px = self._x * map.cfg.pixel - (len(map.grid_binario[0])//2) + map.cfg.pixel//4
        py = self._y * map.cfg.pixel - (len(map.grid_binario)//2) + map.cfg.pixel//4
        m.mlx_put_image_to_window(m.mlx_ptr, win, self._img,px,py)
    
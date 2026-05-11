from .maze_generator import MazeGenerator
from typing import Any


class Player():
    def __init__(self, direction: tuple[int, int], img: int) -> None:
        self._x, self._y = direction
        self._img = img

    def render(self, m: Any, win: int, map: MazeGenerator) -> None:
        assert map.cfg.pixel is not None
        assert map.grid_binario is not None
        px = self._x * map.cfg.pixel - (len(
            map.grid_binario[0])//2) + map.cfg.pixel//4
        py = self._y * map.cfg.pixel - (len(
            map.grid_binario)//2) + map.cfg.pixel//4
        m.mlx_put_image_to_window(m.mlx_ptr, win, self._img, px, py)

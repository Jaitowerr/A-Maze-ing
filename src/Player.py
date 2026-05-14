from .maze_generator import MazeGenerator
from typing import Any


class Player():
    def __init__(self, direction: tuple[int, int], img: int) -> None:
        self._x, self._y = direction
        self._img = img

    def render(self, m: Any, win: int, map: MazeGenerator) -> None:
        """Draw the player image on the given window.

        Args:
            m: Mlx-like object with drawing methods.
            win: Window identifier.
            map: MazeGenerator holding pixel and grid info.

        Returns:
            None
        """
        assert map.cfg.pixel is not None
        assert map.binary_grid is not None
        px = self._x * map.cfg.pixel - (len(
            map.binary_grid[0])//2) + map.cfg.pixel//4
        py = self._y * map.cfg.pixel - (len(
            map.binary_grid)//2) + map.cfg.pixel//4
        m.mlx_put_image_to_window(m.mlx_ptr, win, self._img, px, py)

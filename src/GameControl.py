from src.maze_generator import MazeGenerator
from .Player import Player
from .Direcccion import Direction
from typing import Any
import random


class GameControl:
    def __init__(
        self,
        m: Any,
        win: int,
        map: MazeGenerator,
        player: Player,
        tiles: dict[str, int],
    ) -> None:
        self._m = m
        self._mlx = m.mlx_ptr
        self._win = win
        self._map = map
        self._player = player
        self._state = True
        self._tiles = tiles
        self._color: list[Any] = [False, ""]

    def set_state(self, param: bool) -> None:
        """Set the internal drawing state flag.

        Args:
            param: Boolean state value to set.

        Returns:
            None
        """
        self._state = param

    def move_player(self, key: int) -> None:
        """Move the player based on a key code if the way is open.

        Args:
            key: Numeric key code received from input.

        Returns:
            None
        """
        dx = 0
        dy = 0
        cell = self._map.get_cell(self._player._x, self._player._y)
        if key == 65362 or key == 119:
            if not cell.walls[Direction.NORTH]:
                dy -= 1
        elif key == 65364 or key == 115:
            if not cell.walls[Direction.SOUTH]:
                dy += 1
        elif key == 65361 or key == 97:
            if not cell.walls[Direction.WEST]:
                dx -= 1
        elif key == 65363 or key == 100:
            if not cell.walls[Direction.EAST]:
                dx += 1
        old_x = self._player._x
        old_y = self._player._y

        new_x = dx + old_x
        new_y = dy + old_y
        self._map.redraw_tile(
            self._m, self._mlx, self._win, self._tiles, old_x, old_y
        )
        self._player._x = new_x
        self._player._y = new_y
        self._player.render(self._m, self._win, self._map)
        if (self._player._x == self._map.cfg.exit_x_y[0]
                and self._player._y == self._map.cfg.exit_x_y[1]):
            self._m.mlx_loop_exit(self._m.mlx_ptr)

    def change_color(self) -> None:
        """Change the tile color set randomly and redraw the map.

        Returns:
            None
        """
        color_list = ["img2/mario/colores1",
                      "img2/mario/colores", "img2/mario/colores2"]
        random.shuffle(color_list)
        self._map.cfg.rut = color_list[0]
        from a_maze_ing import load_tiles

        self._tiles = load_tiles(self._m, self._mlx, self._map.cfg)
        self._map.draw_maze(self._m, self._m.mlx_ptr, self._win, self._tiles)
        self._player.render(self._m, self._win, self._map)
        self._color = [True, self._map.cfg.rut]

    def paint_path(self) -> None:
        """Paint or clear the solution path on the displayed map.

        The method toggles between showing the path and restoring tiles.

        Returns:
            None
        """
        assert self._map.path is not None
        assert self._map.cfg.pixel is not None
        assert self._map.binary_grid is not None
        x, y = self._map.cfg.entry_x_y
        if self._state:
            self._map.cfg.rut = "img2/mario"
            for step in self._map.path:
                if step == "N":
                    y -= 1
                elif step == "S":
                    y += 1
                elif step == "E":
                    x += 1
                elif step == "O":
                    x -= 1
                start = self._map.get_cell(x, y)
                key = self._map.get_tile_key(start)
                tile, _, _ = self._m.mlx_png_file_to_image(
                    self._mlx, f"./{self._map.cfg.rut}/camino/{key}.png"
                )
                self._m.mlx_put_image_to_window(
                    self._mlx,
                    self._win,
                    tile,
                    x * self._map.cfg.pixel,
                    y * self._map.cfg.pixel,
                )
                self._state = False
        else:
            for step in self._map.path:
                if step == "N":
                    y -= 1
                elif step == "S":
                    y += 1
                elif step == "E":
                    x += 1
                elif step == "O":
                    x -= 1
                start = self._map.get_cell(x, y)
                key = self._map.get_tile_key(start)
                if self._color[0]:
                    self._map.cfg.rut = self._color[1]
                tile, _, _ = self._m.mlx_png_file_to_image(
                    self._mlx, f"./{self._map.cfg.rut}/{key}.png"
                )
                self._m.mlx_put_image_to_window(
                    self._mlx, self._win, tile,
                    x * self._map.cfg.pixel,
                    y * self._map.cfg.pixel
                )
                self._state = True
        img = self._tiles["exit"]
        x, y = self._map.cfg.exit_x_y
        x = x * self._map.cfg.pixel
        y = y * self._map.cfg.pixel
        self._m.mlx_put_image_to_window(
            self._mlx,
            self._win,
            img,
            x - (len(self._map.binary_grid[0]) //
                 2) + self._map.cfg.pixel // 4,
            y - (len(self._map.binary_grid) // 2) + self._map.cfg.pixel // 4,
        )
        self._player.render(self._m, self._win, self._map)

    def create_map_kruskal(self) -> None:
        """Generate and display a maze using Kruskal's algorithm.

        Returns:
            None
        """
        self._map.cfg.algorithm = "kruskal"
        self._map.reset()
        self._map.run_algorithm()
        self._map.build_binary_grid()
        self._player._x = self._map.cfg.entry_x_y[0]
        self._player._y = self._map.cfg.entry_x_y[1]
        self._map.draw_maze(self._m, self._m.mlx_ptr, self._win, self._tiles)
        self._player.render(self._m, self._win, self._map)
        self._map.build_hex_grid()
        self._map.shortest_path()

    def create_map_recursive(self) -> None:
        """Generate and display a maze using recursive backtracker.

        Returns:
            None
        """
        self._map.reset()
        self._map.run_algorithm()
        self._map.build_binary_grid()
        self._player._x = self._map.cfg.entry_x_y[0]
        self._player._y = self._map.cfg.entry_x_y[1]
        self._map.draw_maze(self._m, self._m.mlx_ptr, self._win, self._tiles)
        self._player.render(self._m, self._win, self._map)
        self._map.build_hex_grid()
        self._map.shortest_path()

    def create_ascii(self) -> None:
        """Print the maze to the console in ASCII mode.

        Returns:
            None
        """
        self._map.print_maze()

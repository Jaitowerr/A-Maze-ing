from src.map import MazeConfig
from .Celda import Cell
from .Direcccion import Direction
from collections import deque
from typing import Optional, Any


class MazeGenerator:
    def __init__(self, cfg: MazeConfig) -> None:
        self.cfg = cfg
        assert cfg.grid is not None
        self.grid = [row.copy() for row in cfg.grid]
        self.grid[self.cfg.entry_y][self.cfg.entry_x] = 4
        self.grid[self.cfg.exit_y][self.cfg.exit_x] = 5
        self.binary_grid: Optional[list[list[Cell]]] = None
        self.hex_grid: Optional[list[str]] = None
        self.path: Optional[str] = None
        self.run_algorithm()
        self.build_binary_grid()
        self.build_hex_grid()
        self.shortest_path()

    def run_algorithm(self) -> None:
        """Run the configured maze generation algorithm.

        The method selects and executes the algorithm configured in
        the MazeConfig (e.g. 'recursive_backtracker' or 'kruskal').

        Returns:
            None
        """
        if self.cfg.algorithm == 'recursive_backtracker':
            from .algorithm import recursive_backtracker
            recursive_backtracker.run(self)
        elif self.cfg.algorithm == 'kruskal':
            from .algorithm import kruskal
            kruskal.run(self)

    def reset(self) -> None:
        """Reset the working grid to the initial configuration.

        This restores the grid from the MazeConfig and reapplies the
        entry and exit markers.

        Returns:
            None
        """
        assert self.cfg.grid is not None
        self.grid = [row.copy() for row in self.cfg.grid]
        self.grid[self.cfg.entry_y][self.cfg.entry_x] = 4
        self.grid[self.cfg.exit_y][self.cfg.exit_x] = 5

    def build_binary_grid(self) -> None:
        """Build the internal binary grid of Cell objects.

        Each Cell stores the presence of walls (north/south/east/west)
        and a flag for the 42 area. The binary grid is used for
        drawing and pathfinding.

        Returns:
            None
        """
        self.binary_grid = []
        row = 1
        while row < len(self.grid) - 1:
            fila_celdas = []
            pos = 1
            while pos < len(self.grid[row]) - 1:
                valor = self.grid[row][pos]
                is_42 = (valor == 42)
                west = 1 if self.grid[row][pos - 1] != 0 else 0
                south = 1 if self.grid[row + 1][pos] != 0 else 0
                east = 1 if self.grid[row][pos + 1] != 0 else 0
                north = 1 if self.grid[row - 1][pos] != 0 else 0
                fila_celdas.append(Cell(west, south, east, north, is_42))
                pos += 2
            self.binary_grid.append(fila_celdas)
            row += 2

    def build_hex_grid(self) -> None:
        """Convert the binary grid to hexadecimal string rows.

        The hex grid is a list of strings where each character encodes
        a cell's walls as a single hexadecimal digit.

        Returns:
            None
        """
        assert self.binary_grid is not None
        self.hex_grid = []
        for row in self.binary_grid:
            fila_hexa = ''
            for cell in row:
                fila_hexa += cell.bin_to_hexa()
            self.hex_grid.append(fila_hexa)

    def print_grid(self) -> None:
        """Print the internal numeric grid to stdout for debugging.

        Returns:
            None
        """
        for row in self.grid:
            for idx, val in enumerate(row):
                end = ", " if idx < len(row) - 1 else ""
                print(val, end=end)
            print()

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True when the given coordinates are inside the maze.

        Args:
            x: X coordinate (column).
            y: Y coordinate (row).

        Returns:
            True if (x, y) is within the configured width/height.
        """
        return 0 <= x < self.cfg.width and 0 <= y < self.cfg.height

    def write_output(self) -> None:
        """Write the hex grid and path info to the configured file.

        The output file contains hex rows, an empty line and the entry
        and exit coordinates followed by the path string.

        Returns:
            None
        """
        assert self.hex_grid is not None
        assert self.path is not None
        with open(self.cfg.output_file, 'w') as f:
            for fila in self.hex_grid:
                f.write(fila + '\n')
            f.write('\n')
            f.write(f'{self.cfg.entry_x_y[0]},{self.cfg.entry_x_y[1]}\n')
            f.write(f'{self.cfg.exit_x_y[0]},{self.cfg.exit_x_y[1]}\n')
            f.write(f'{self.path}')

    def get_cell(self, x: int, y: int) -> Cell:
        """Return the Cell at grid coordinate (x, y).

        Args:
            x: X coordinate (column).
            y: Y coordinate (row).

        Returns:
            The Cell object stored at the requested position.
        """
        assert self.binary_grid is not None
        return self.binary_grid[y][x]

    def redraw_tile(self,
                    m: Any,
                    mlx: int,
                    win: int,
                    tiles: dict[str, int],
                    x: int,
                    y: int) -> None:
        """Redraw a single tile at pixel position based on the cell.

        Args:
            m: Mlx-like object providing image drawing methods.
            mlx: The mlx pointer used by the drawing API.
            win: The window identifier.
            tiles: Mapping of tile keys to loaded image ids.
            x: Tile X coordinate.
            y: Tile Y coordinate.

        Returns:
            None
        """
        assert self.cfg.pixel is not None
        assert self.binary_grid is not None
        cell = self.get_cell(x, y)
        key = self.get_tile_key(cell)
        img = tiles[key]
        px = x * self.cfg.pixel
        py = y * self.cfg.pixel
        m.mlx_put_image_to_window(mlx, win, img, px, py)
        if self.cfg.entry_x_y == [x, y]:
            m.mlx_put_image_to_window(
                mlx, win, tiles["entry"],
                px - (len(self.binary_grid[0]) // 2) + self.cfg.pixel // 4,
                py - (len(self.binary_grid) // 2) + self.cfg.pixel // 4)
        elif self.cfg.exit_x_y == [x, y]:
            m.mlx_put_image_to_window(
                mlx, win, tiles["exit"],
                px - (len(self.binary_grid[0]) // 2) + self.cfg.pixel // 4,
                py - (len(self.binary_grid) // 2) + self.cfg.pixel // 4)

    def print_maze(self,
                   color_grid: str = '\033[34m',
                   color_bg_way: str = '\033[93m',
                   icons: Optional[dict[str, str]] = None) -> tuple[str, str]:
        """Print a colored ASCII representation of the maze.

        Args:
            color_grid: ANSI color code for grid lines.
            color_bg_way: ANSI color code for the path background.
            icons: Optional mapping of characters used for drawing.

        Returns:
            A tuple with the used (color_grid, color_bg_way) strings.
        """
        if icons is None:
            icons = {'PARED_H': '---', 'PARED_V': '|', 'ESQUINA': '+'}
        assert self.binary_grid is not None

        wall_h = icons['PARED_H'] + color_grid
        wall_v = icons['PARED_V'] + color_grid
        corner = color_grid + icons['ESQUINA'] + color_grid
        empty_cell_str = "   " + color_grid
        entrance = color_bg_way + "STR" + color_grid
        exit = color_bg_way + "FIN" + color_grid
        p42 = color_bg_way + "\u2588\u2588\u2588" + color_grid

        top_line = corner
        for _ in range(len(self.binary_grid[0])):
            top_line += wall_h + corner
        print(top_line)

        for y in range(len(self.binary_grid)):
            line_walls = wall_v
            line_floor = corner
            for x in range(len(self.binary_grid[0])):
                cell = self.get_cell(x, y)

                if self.cfg.entry_x_y == [x, y]:
                    content = entrance
                elif self.cfg.exit_x_y == [x, y]:
                    content = exit
                elif cell.is_42:
                    content = p42
                else:
                    content = empty_cell_str

                if cell.walls[Direction.EAST]:
                    line_walls += content + wall_v
                else:
                    line_walls += content + " "

                if cell.walls[Direction.SOUTH]:
                    line_floor += wall_h + corner
                else:
                    line_floor += empty_cell_str + corner

            print(line_walls)
            print(line_floor)
        return color_grid, color_bg_way

    def print_maze_path(self,
                        color_grid: str = '\033[32m',
                        color_bg_way: str = '\033[35m',
                        icons: Optional[dict[str, str]] = None) -> tuple[
                            str, str]:
        """Print the maze with the solution path highlighted.

        Args:
            color_grid: ANSI color for grid lines.
            color_bg_way: ANSI color for the path background.
            icons: Optional mapping of characters for drawing.

        Returns:
            A tuple with the used (color_grid, color_bg_way) strings.
        """
        if icons is None:
            icons = {'PARED_H': '---', 'PARED_V': '|', 'ESQUINA': '+'}
        assert self.path is not None
        assert self.binary_grid is not None
        path_cells = {}
        sx, sy = self.cfg.entry_x_y
        x, y = sx, sy
        for d in self.path:
            path_cells[(x, y)] = d
            if d == 'N':
                y -= 1
            elif d == 'S':
                y += 1
            elif d == 'E':
                x += 1
            elif d == 'O':
                x -= 1
        path_cells[(x, y)] = 'X'

        wall_h = icons['PARED_H'] + color_grid
        wall_v = icons['PARED_V'] + color_grid
        corner = color_grid + icons['ESQUINA'] + color_grid
        empty_cell_str = "   " + color_grid
        entrance = color_bg_way + "STR" + color_grid
        exit = color_bg_way + "FIN" + color_grid
        p42 = color_bg_way + "\u2588\u2588\u2588" + color_grid

        top_line = corner
        for _ in range(len(self.binary_grid[0])):
            top_line += wall_h + corner
        print(top_line)

        for cy in range(len(self.binary_grid)):
            line_walls = wall_v
            line_floor = corner
            for cx in range(len(self.binary_grid[0])):
                cell = self.get_cell(cx, cy)

                if self.cfg.entry_x_y == [cx, cy]:
                    content = entrance
                elif self.cfg.exit_x_y == [cx, cy]:
                    content = exit
                elif cell.is_42:
                    content = p42
                elif (cx, cy) in path_cells:
                    d = path_cells[(cx, cy)]
                    if d == 'N':
                        content = color_bg_way + ' ^ ' + color_grid
                    elif d == 'S':
                        content = color_bg_way + ' v ' + color_grid
                    elif d == 'E':
                        content = color_bg_way + ' \u00bb ' + color_grid
                    elif d == 'O':
                        content = color_bg_way + ' \u00ab ' + color_grid
                    else:
                        content = empty_cell_str
                else:
                    content = empty_cell_str

                if cell.walls[Direction.EAST]:
                    line_walls += content + wall_v
                else:
                    line_walls += content + " "

                if cell.walls[Direction.SOUTH]:
                    line_floor += wall_h + corner
                else:
                    line_floor += empty_cell_str + corner

            print(line_walls)
            print(line_floor)

        return color_grid, color_bg_way

    def get_tile_key(self, cell: Cell) -> str:
        """Return the 4-bit tile key string for the given Cell.

        The returned string has the order west, south, east, north.

        Args:
            cell: Cell instance to query.

        Returns:
            A 4-character string of '0'/'1' digits representing walls.
        """
        n = int(cell.walls[Direction.NORTH])
        s = int(cell.walls[Direction.SOUTH])
        e = int(cell.walls[Direction.EAST])
        o = int(cell.walls[Direction.WEST])
        return f"{o}{s}{e}{n}"

    def draw_maze(self,
                  m: Any,
                  mlx: int,
                  win: int,
                  tiles: dict[str, int]) -> None:
        """Draw the whole maze using the provided tile images.

        Args:
            m: Mlx-like drawing object.
            mlx: mlx pointer used for drawing.
            win: Window identifier where to draw.
            tiles: Mapping of tile keys to image ids.

        Returns:
            None
        """
        assert self.binary_grid is not None
        assert self.cfg.pixel is not None
        for y in range(len(self.binary_grid)):
            for x in range(len(self.binary_grid[0])):
                cell = self.get_cell(x, y)
                px = x * self.cfg.pixel
                py = y * self.cfg.pixel

                key = self.get_tile_key(cell)
                img = tiles[key]
                m.mlx_put_image_to_window(mlx, win, img, px, py)
                # AFTER
                if self.cfg.entry_x_y == [x, y]:
                    img = tiles["entry"]
                    m.mlx_put_image_to_window(
                        mlx, win, img,
                        px - (len(self.binary_grid[0]) //
                              2) + self.cfg.pixel // 4,
                        py - (len(
                            self.binary_grid) // 2) + self.cfg.pixel // 4)
                elif self.cfg.exit_x_y == [x, y]:
                    img = tiles["exit"]
                    m.mlx_put_image_to_window(
                        mlx, win, img,
                        px - (len(self.binary_grid[0]) //
                              2) + self.cfg.pixel // 4,
                        py - (len(
                            self.binary_grid) // 2) + self.cfg.pixel // 4)

    def shortest_path(self) -> Optional[str]:
        """Compute the shortest path between entry and exit using BFS.

        Returns:
            A string with directions (N/S/E/O) from entry to exit or
            None when no path exists.
        """
        assert self.binary_grid is not None
        sx, sy = self.cfg.entry_x_y
        ex, ey = self.cfg.exit_x_y

        H = len(self.binary_grid)
        W = len(self.binary_grid[0])

        queue = deque([(sy, sx)])
        visited = {(sy, sx)}
        parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

        while queue:
            y, x = queue.popleft()
            if (y, x) == (ey, ex):
                break

            cell = self.binary_grid[y][x]
            moves = [
                (cell.walls[Direction.NORTH] == 0, y - 1, x, 'N'),
                (cell.walls[Direction.SOUTH] == 0, y + 1, x, 'S'),
                (cell.walls[Direction.EAST] == 0, y, x + 1, 'E'),
                (cell.walls[Direction.WEST] == 0, y, x - 1, 'O'),
            ]

            for has_step, ny, nx, direction in moves:
                if has_step and 0 <= ny < H and 0 <= nx < W:
                    if (ny, nx) not in visited:
                        visited.add((ny, nx))
                        parent[(ny, nx)] = ((y, x), direction)
                        queue.append((ny, nx))

        if (ey, ex) not in parent:
            self.path = None
            return None

        directions: list[str] = []
        cur = (ey, ex)
        while cur != (sy, sx):
            cur, d = parent[cur]
            directions.append(d)

        directions.reverse()
        self.path = ''.join(directions)
        return self.path

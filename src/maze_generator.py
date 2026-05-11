from src.map import MazeConfig
from .Celda import Celda
from .Direcccion import Direccion
from collections import deque
from typing import Optional, Any


class MazeGenerator:
    def __init__(self, cfg: MazeConfig) -> None:
        self.cfg = cfg
        assert cfg.grid is not None
        self.grid = [row.copy() for row in cfg.grid]
        self.grid[self.cfg.entry_y][self.cfg.entry_x] = 4
        self.grid[self.cfg.exit_y][self.cfg.exit_x] = 5
        self.grid_binario: Optional[list[list[Celda]]] = None
        self.grid_hexadecimal: Optional[list[str]] = None
        self.camino: Optional[str] = None
        self.algoritmo()
        self.binario()
        self.hexadecimal()
        self.shortest_path()

    def algoritmo(self) -> None:

        if self.cfg.algorithm == 'recursive_backtracker':
            from .algorithm import recursive_backtracker
            recursive_backtracker.run(self)
        elif self.cfg.algorithm == 'kruskal':
            from .algorithm import kruskal
            kruskal.run(self)

    def reset(self) -> None:
        assert self.cfg.grid is not None
        self.grid = [row.copy() for row in self.cfg.grid]
        self.grid[self.cfg.entry_y][self.cfg.entry_x] = 4
        self.grid[self.cfg.exit_y][self.cfg.exit_x] = 5

    def binario(self) -> None:
        self.grid_binario = []
        row = 1
        while (row < len(self.grid) - 1):
            fila_celdas = []
            pos = 1
            while (pos < len(self.grid[row]) - 1):
                valor = self.grid[row][pos]
                es_42 = (valor == 42)
                oeste = 1 if self.grid[row][pos - 1] != 0 else 0
                sur = 1 if self.grid[row + 1][pos] != 0 else 0
                este = 1 if self.grid[row][pos + 1] != 0 else 0
                norte = 1 if self.grid[row - 1][pos] != 0 else 0

                fila_celdas.append(Celda(oeste, sur, este, norte, es_42))
                pos += 2
            self.grid_binario.append(fila_celdas)
            row += 2

    def hexadecimal(self) -> None:
        assert self.grid_binario is not None
        self.grid_hexadecimal = []
        for row in self.grid_binario:
            fila_hexa = ''
            for celda in row:
                fila_hexa += celda.bin_to_hexa()
            self.grid_hexadecimal.append(fila_hexa)

    def print_grid(self) -> None:
        for row in self.grid:
            for idx, val in enumerate(row):
                end = ", " if idx < len(row) - 1 else ""
                print(val, end=end)
            print()

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.cfg.width and 0 <= y < self.cfg.height

    def docu_finish(self) -> None:
        assert self.grid_hexadecimal is not None
        assert self.camino is not None
        with open(self.cfg.output_file, 'w') as f:
            for fila in self.grid_hexadecimal:
                f.write(fila + '\n')
            f.write('\n')
            f.write(f'{self.cfg.entry_x_y[0]},{self.cfg.entry_x_y[1]}\n')
            f.write(f'{self.cfg.exit_x_y[0]},{self.cfg.exit_x_y[1]}\n')
            f.write(f'{self.camino}')

    def get_cell(self, x: int, y: int) -> Celda:
        """
        Devuelve la celda en la posición (x, y)
        """
        assert self.grid_binario is not None
        return self.grid_binario[y][x]

    def redraw_tile(self,
                    m: Any,
                    mlx: int,
                    win: int,
                    tiles: dict[str, int],
                    x: int,
                    y: int) -> None:
        assert self.cfg.pixel is not None
        assert self.grid_binario is not None
        cell = self.get_cell(x, y)
        key = self.get_tile_key(cell)
        img = tiles[key]
        px = x*self.cfg.pixel
        py = y*self.cfg.pixel
        m.mlx_put_image_to_window(mlx, win, img, px, py)
        if self.cfg.entry_x_y == [x, y]:

            m.mlx_put_image_to_window(
                mlx, win, tiles["entry"],
                px-(len(self.grid_binario[0])//2) + self.cfg.pixel//4,
                py-(len(self.grid_binario)//2) + self.cfg.pixel//4)

        elif self.cfg.exit_x_y == [x, y]:
            m.mlx_put_image_to_window(
                mlx, win, tiles["exit"],
                px-(len(self.grid_binario[0])//2) + self.cfg.pixel//4,
                py-(len(self.grid_binario)//2) + self.cfg.pixel//4)

    def print_maze(self,
                   color_grid: str = '\033[34m',
                   color_bg_way: str = '\033[93m',
                   iconos: Optional[dict[str, str]] = None) -> tuple[str, str]:

        if iconos is None:
            iconos = {
                'PARED_H': '---', 'PARED_V': '|', 'ESQUINA': '+'
            }
        assert self.grid_binario is not None

        PARED_H = iconos['PARED_H'] + color_grid
        PARED_V = iconos['PARED_V'] + color_grid
        ESQUINA = color_grid + iconos['ESQUINA'] + \
            color_grid
        PASILLO = "   " + color_grid
        ENTRADA = color_bg_way + " E " + color_grid
        SALIDA = color_bg_way + " S " + color_grid
        P42 = color_bg_way + "███" + color_grid

        top_line = ESQUINA
        for _ in range(len(self.grid_binario[0])):
            top_line += PARED_H + ESQUINA
        print(top_line)

        for y in range(len(self.grid_binario)):
            line_walls = PARED_V
            line_floor = ESQUINA
            for x in range(len(self.grid_binario[0])):
                cell = self.get_cell(x, y)

                if self.cfg.entry_x_y == [x, y]:
                    content = ENTRADA
                elif self.cfg.exit_x_y == [x, y]:
                    content = SALIDA
                elif cell.casilla_42:
                    content = P42
                else:
                    content = PASILLO

                if cell.walls[Direccion.ESTE]:
                    line_walls += content + PARED_V
                else:
                    line_walls += content + " "

                if cell.walls[Direccion.SUR]:
                    line_floor += PARED_H + ESQUINA
                else:
                    line_floor += PASILLO + ESQUINA

            print(line_walls)
            print(line_floor)
        return color_grid, color_bg_way

    def print_maze_path(
        self,
        color_grid: str = '\033[32m',
        color_bg_way: str = '\033[35m',
        iconos: Optional[dict[str, str]] = None
    ) -> tuple[str, str]:

        if iconos is None:
            iconos = {
                'PARED_H': '---', 'PARED_V': '|', 'ESQUINA': '+'
            }
        assert self.camino is not None
        assert self.grid_binario is not None
        camino_celdas = {}
        sx, sy = self.cfg.entry_x_y
        x, y = sx, sy
        for d in self.camino:
            camino_celdas[(x, y)] = d
            if d == 'N':
                y -= 1
            elif d == 'S':
                y += 1
            elif d == 'E':
                x += 1
            elif d == 'O':
                x -= 1
        camino_celdas[(x, y)] = 'X'

        PARED_H = iconos['PARED_H'] + color_grid
        PARED_V = iconos['PARED_V'] + color_grid
        ESQUINA = color_grid + iconos['ESQUINA'] + color_grid
        PASILLO = "   " + color_grid
        ENTRADA = color_bg_way + " E " + color_grid
        SALIDA = color_bg_way + " S " + color_grid
        P42 = color_bg_way + "███" + color_grid

        top_line = ESQUINA
        for _ in range(len(self.grid_binario[0])):
            top_line += PARED_H + ESQUINA
        print(top_line)

        for cy in range(len(self.grid_binario)):
            line_walls = PARED_V
            line_floor = ESQUINA
            for cx in range(len(self.grid_binario[0])):
                cell = self.get_cell(cx, cy)

                if self.cfg.entry_x_y == [cx, cy]:
                    content = ENTRADA
                elif self.cfg.exit_x_y == [cx, cy]:
                    content = SALIDA
                elif cell.casilla_42:
                    content = P42
                elif (cx, cy) in camino_celdas:
                    d = camino_celdas[(cx, cy)]
                    if d == 'N':
                        content = color_bg_way + ' ^ ' + color_grid
                    elif d == 'S':
                        content = color_bg_way + ' v ' + color_grid
                    elif d == 'E':
                        content = color_bg_way + ' » ' + color_grid
                    elif d == 'O':
                        content = color_bg_way + ' « ' + color_grid

                else:
                    content = PASILLO

                if cell.walls[Direccion.ESTE]:
                    line_walls += content + PARED_V
                else:
                    line_walls += content + " "

                if cell.walls[Direccion.SUR]:
                    line_floor += PARED_H + ESQUINA
                else:
                    line_floor += PASILLO + ESQUINA

            print(line_walls)
            print(line_floor)

        return color_grid, color_bg_way

    def get_tile_key(self, cell: Celda) -> str:
        n = int(cell.walls[Direccion.NORTE])
        s = int(cell.walls[Direccion.SUR])
        e = int(cell.walls[Direccion.ESTE])
        o = int(cell.walls[Direccion.OESTE])
        return f"{o}{s}{e}{n}"

    def draw_maze(self,
                  m: Any,
                  mlx: int,
                  win: int,
                  tiles: dict[str, int]) -> None:
        assert self.grid_binario is not None
        assert self.cfg.pixel is not None
        for y in range(len(self.grid_binario)):
            for x in range(len(self.grid_binario[0])):
                cell = self.get_cell(x, y)
                px = x * self.cfg.pixel
                py = y * self.cfg.pixel

                key = self.get_tile_key(cell)
                img = tiles[key]
                m.mlx_put_image_to_window(mlx, win, img, px, py)
                # DESPUÉS
                if self.cfg.entry_x_y == [x, y]:
                    img = tiles["entry"]
                    m.mlx_put_image_to_window(
                        mlx, win, img,
                        px-(len(self.grid_binario[0])//2) + self.cfg.pixel//4,
                        py-(len(self.grid_binario)//2) + self.cfg.pixel//4)
                elif self.cfg.exit_x_y == [x, y]:
                    img = tiles["exit"]
                    m.mlx_put_image_to_window(
                        mlx, win, img,
                        px-(len(self.grid_binario[0])//2) + self.cfg.pixel//4,
                        py-(len(self.grid_binario)//2) + self.cfg.pixel//4)

    def shortest_path(self) -> Optional[str]:
        assert self.grid_binario is not None
        sx, sy = self.cfg.entry_x_y
        ex, ey = self.cfg.exit_x_y

        H = len(self.grid_binario)
        W = len(self.grid_binario[0])

        queue = deque([(sy, sx)])
        visited = {(sy, sx)}
        parent = {}

        while queue:
            y, x = queue.popleft()

            if (y, x) == (ey, ex):
                break

            celda = self.grid_binario[y][x]

            movimientos = [
                (celda.walls[Direccion.NORTE] == 0, y - 1, x, 'N'),
                (celda.walls[Direccion.SUR] == 0,   y + 1, x, 'S'),
                (celda.walls[Direccion.ESTE] == 0,  y, x + 1, 'E'),
                (celda.walls[Direccion.OESTE] == 0, y, x - 1, 'O'),
            ]

            for hay_paso, ny, nx, direccion in movimientos:
                if hay_paso and 0 <= ny < H and 0 <= nx < W:
                    if (ny, nx) not in visited:
                        visited.add((ny, nx))
                        parent[(ny, nx)] = ((y, x), direccion)
                        queue.append((ny, nx))

        if (ey, ex) not in parent:
            self.camino = None
            return None

        direcciones = []
        cur = (ey, ex)

        while cur != (sy, sx):
            cur, d = parent[cur]
            direcciones.append(d)

        direcciones.reverse()
        self.camino = ''.join(direcciones)
        return self.camino

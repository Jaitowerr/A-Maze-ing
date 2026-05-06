from src.map import MazeConfig
from .Celda import Celda
from .Direcccion import Direccion
import random


class MazeGenerator:
    def __init__(self, cfg: MazeConfig) -> None:
        self.cfg = cfg
        self.grid = [row.copy() for row in cfg.grid]
        self.grid[self.cfg.entry_y][self.cfg.entry_x] = 4
        self.grid[self.cfg.exit_y][self.cfg.exit_x] = 5
        self.grid_binario = None
        self.grid_hexadecimal = None
        self.camino = None
        self.algoritmo()
        self.binario()
        self.hexadecimal()

    def algoritmo(self) -> None:
        random.seed(self.cfg.seed)
        if self.cfg.algorithm == 'recursive_backtracker':
            from .algorithm import recursive_backtracker
            ok = recursive_backtracker.run(self)
        if self.cfg.algorithm == 'kruskal':
            from .algorithm import kruskal
            ok = kruskal.run(self)


    def binario(self):
        self.grid_binario = []
        row = 1
        while(row < len(self.grid) - 1):
            fila_celdas = []
            pos = 1
            while(pos < len(self.grid[row]) - 1):
                valor = self.grid[row][pos]
                es_42 = (valor == 42)
                oeste = 1 if self.grid[row][pos - 1] != 0 else 0
                sur   = 1 if self.grid[row + 1][pos] != 0 else 0
                este  = 1 if self.grid[row][pos + 1] != 0 else 0
                norte = 1 if self.grid[row - 1][pos] != 0 else 0

                fila_celdas.append(Celda(oeste, sur, este, norte, es_42))
                pos += 2
            self.grid_binario.append(fila_celdas)
            row += 2

    def hexadecimal(self):
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

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def docu_finish(self):
        with open(self.cfg.output_file, 'w') as f:
            for fila in self.grid_hexadecimal:
                f.write(fila + '\n')
            f.write('\n')
            f.write(f'{self.cfg.entry_x_y[0]},{self.cfg.entry_x_y[1]}\n')
            f.write(f'{self.cfg.exit_x_y[0]},{self.cfg.exit_x_y[1]}')
            # f.write(self.camino)

    def get_cell(self, x, y) -> Celda:
            """
            Devuelve la celda en la posición (x, y)
            """
            return self.grid_binario[y][x]

    def print_maze(self):
        """
        Representación visual simple en consola.

        +---+ = paredes horizontales
        |   | = paredes verticales
        """

        top_line = "+"
        for _ in range(len(self.grid_binario[0])):
            top_line += "---+"
        print(top_line)

        for y in range(len(self.grid_binario)):
            line_walls = "|"
            line_floor = "+"
            for x in range(len(self.grid_binario[0])):
                #print(f"celda: {x} {y}")
                cell = self.get_cell(x, y)

                
                if self.cfg.entry_x_y ==[x, y]:
                    content = " E "
                elif self.cfg.exit_x_y == [x, y]:
                    content = " S "
                elif cell.casilla_42:
                    content = "42 "
                else:
                    content = "   "


                if cell.walls[Direccion.ESTE]:
                    line_walls += content + "|"
                else:
                    line_walls += content + " "

      
                if cell.walls[Direccion.SUR]:
                    line_floor += "---+"
                else:
                    line_floor += "   +"

            print(line_walls)
            print(line_floor)
    
    def get_tile_key(self, cell: Celda):
        n = int(cell.walls[Direccion.NORTE])
        s = int(cell.walls[Direccion.SUR])
        e = int(cell.walls[Direccion.ESTE])
        o = int(cell.walls[Direccion.OESTE])
        return f"{n}{s}{e}{o}"

    def draw_maze(self,m,mlx,win,tiles):
        for y in range(len(self.grid_binario)):
            for x in range(len(self.grid_binario[0])):
                cell = self.get_cell(x,y)
                px = x *40
                py = y *40
                
                key = self.get_tile_key(cell)
                img = tiles[key]
                m.mlx_put_image_to_window(mlx,win,img,px,py)
                if self.cfg.entry_x_y == [x,y]:
                    img = tiles["entry"]
                    m.mlx_put_image_to_window(mlx,win,img,px+14,py+14)
                elif self.cfg.exit_x_y == [x,y]:
                    img = tiles["exit"]
                    m.mlx_put_image_to_window(mlx,win,img,px+14,py+14)
                


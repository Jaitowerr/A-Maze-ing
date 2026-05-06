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

    def algoritmo(self) -> None:
        random.seed(self.cfg.seed)
        if self.cfg.algorithm == 'recursive_backtracker':
            from .algorithm import recursive_backtracker
            ok = recursive_backtracker.run(self)

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


    def map_bin_hex(self):
        grid = self.grid
        H = len(grid)
        W = len(grid[0])

    def print_grid(self) -> None:
        for row in self.grid:
            for idx, val in enumerate(row):
                end = ", " if idx < len(row) - 1 else ""
                print(val, end=end)
            print()

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    '''
    def get_cell(self, x, y) -> Celda:
            """
            Devuelve la celda en la posición (x, y)
            """
            return self.grid2[y][x]


    def get_unvisited_neighbors(self, x, y):
            """
            Devuelve vecinos no visitados y válidos para DFS.

            Retorna:
            [
                (nx, ny, direction)
            ]
            """
            neighbors = []

            for direction, (dx, dy) in MOVES.items():
                nx = x + dx
                ny = y + dy

                if not self.in_bounds(nx, ny):
                    continue

                neighbor = self.get_cell(nx, ny)


                if neighbor.es_42:
                    continue

                if not neighbor.visited:
                    neighbors.append((nx, ny, direction))

            return neighbors


    def remove_wall(self, x, y, nx, ny, direction):
            """
            Rompe la pared entre dos celdas:
            celda actual y celda vecina

            Garantiza coherencia:
            si una pared se abre, la opuesta también.
            """
            current = self.get_cell(x, y)
            neighbor = self.get_cell(nx, ny)

            current.walls[direction] = False
            neighbor.walls[OPUESTO[direction]] = False

    def add_loops(self, probability=0.15):
         for y in range(self.height):
              for x in range(self.width):
                   current = self.get_cell(x,y)
                   if current.es_42:
                        continue
                   for direction, (dx,dy) in MOVES.items():
                        nx = x + dx
                        ny = y + dy
                        if not self.in_bounds(nx,ny):
                             continue
                        neighbor = self.get_cell(nx,ny)
                        if neighbor.es_42:
                             continue
                        if current.walls[direction] is False:
                             continue
                        if random.random() < probability:
                             self.remove_wall(x,y,nx,ny,direction)

    def generate_maze(self, x=0, y=0):
            """
            DFS .

            Si perfect=True:
            genera un perfect maze automáticamente.
            """
            from algorithm  import dfs
            dfs.run(self,x,y)

    def print_maze(self):
        """
        Representación visual simple en consola.

        +---+ = paredes horizontales
        |   | = paredes verticales
        """

 
        top_line = "+"
        for _ in range(self.width):
            top_line += "---+"
        print(top_line)

        for y in range(self.height):
            line_walls = "|"
            line_floor = "+"

            for x in range(self.width):
                cell = self.get_cell(x, y)


                if self.entry == (x, y):
                    content = " E "
                elif self.exit == (x, y):
                    content = " S "
                elif cell.es_42:
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
    
    def mark_42(self, m, win, tiles):
        """
        Reserva celdas para dibujar el patrón '42'
        usando celdas completamente cerradas.
        """

        print(self.width)
        if self.width < 10 or self.height < 10:
            raise ValueError(
                "El laberinto es demasiado pequeño para dibujar '42'"
            )

        start_x = self.width // 3
        start_y = self.height // 3


        four = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
            (2,3),
            (2,4)
        ]

       
        two = [
            (4, 0),
            (5, 0),
            (6, 0),
            (6, 1),
            (4, 2),
            (4,3),
            (4,4),
            (5, 2),
            (5,4),
            (6, 2),
            (6,4)
        ]

        pattern = four + two
        pattern_width = 7
        pattern_height = 5

        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            raise ValueError(
                "El laberinto es demasiado pequeño para centrar el 42"
            )

    
        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        for dx, dy in pattern:
            x = start_x + dx
            y = start_y + dy

            if not self.in_bounds(x, y):
                raise ValueError(
                    "Error al colocar el patrón 42"
                )

            self.grid2[y][x].es_42 = True
        self.generate_maze(0,0)
        if not self.perfect:
            self.add_loops(probability=0.10)
        self.draw_maze(m,m.mlx_ptr,win, tiles)

    def get_tile_key(self, cell: Celda):
        n = int(cell.walls[Direccion.NORTE])
        s = int(cell.walls[Direccion.SUR])
        e = int(cell.walls[Direccion.ESTE])
        o = int(cell.walls[Direccion.OESTE])
        return f"{n}{s}{e}{o}"

    def draw_maze(self,m,mlx,win,tiles):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x,y)
                px = x *40
                py = y *40
                if self.entry == (x,y):
                    img = tiles["entry"]
                elif self.exit == (x,y):
                    img = tiles["exit"]
                else:
                    key = self.get_tile_key(cell)
                    img = tiles[key]
                m.mlx_put_image_to_window(mlx,win,img,px,py)
    '''

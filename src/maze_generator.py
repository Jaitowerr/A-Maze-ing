from src.map import MazeConfig
from .Celda import Celda
from .Direcccion import Direccion
import random
from collections import deque


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
        self.shortest_path()

    def algoritmo(self) -> None:
        # random.seed(self.cfg.seed)
        if self.cfg.algorithm == 'recursive_backtracker':
            from .algorithm import recursive_backtracker
            recursive_backtracker.run(self)
        elif self.cfg.algorithm == 'kruskal':
            from .algorithm import kruskal
            kruskal.run(self)
        # elif self.cfg.algorithm == 'dfs':
        #     from .algorithm import dfs
        #     dfs.run(self)


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
            f.write(f'{self.cfg.exit_x_y[0]},{self.cfg.exit_x_y[1]}\n')
            f.write(f'{self.camino}')

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
        simples = ['─', '│', '┌', '┐', '└', '┘', '├', '┤', '┬', '┴', '┼']
        dobles  = ['═', '║', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬']
        relleno = ['█', '▓', '▒', '░', '▄', '▀', '▌', '▐']

        texto = {
            "negro": "\033[30m", "rojo": "\033[31m", "verde": "\033[32m",
            "amarillo": "\033[33m", "azul": "\033[34m", "magenta": "\033[35m",
            "cian": "\033[36m", "blanco": "\033[37m", "gris": "\033[90m",
            "rojo_b": "\033[91m", "verde_b": "\033[92m", "amarillo_b": "\033[93m",
            "azul_b": "\033[94m", "magenta_b": "\033[95m", "cian_b": "\033[96m",
            "blanco_b": "\033[97m"
        }

        fondo = {
            "negro": "\033[40m", "rojo": "\033[41m", "verde": "\033[42m",
            "amarillo": "\033[43m", "azul": "\033[44m", "magenta": "\033[45m",
            "cian": "\033[46m", "blanco": "\033[47m", "gris": "\033[100m",
            "rojo_b": "\033[101m", "verde_b": "\033[102m", "amarillo_b": "\033[103m",
            "azul_b": "\033[104m", "magenta_b": "\033[105m", "cian_b": "\033[106m",
            "blanco_b": "\033[107m"
        }

        estilo = {
            "reset": "\033[0m", "negrita": "\033[1m",
            "tenue": "\033[2m", "subrayado": "\033[4m", "invertido": "\033[7m"
        }

        PARED_H  = "───"   # pared horizontal
        PARED_V  = "│"     # pared vertical
        ESQUINA  = "│"     # esquinas/intersecciones
        PASILLO  = "   "   # espacio abierto
        ENTRADA  = " E "
        SALIDA   = " S "
        P42      = "███"

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


    # def print_maze(self):
    #     """
    #     Representación visual simple en consola.

    #     +---+ = paredes horizontales
    #     |   | = paredes verticales
    #     """

    #     top_line = "+"
    #     for _ in range(len(self.grid_binario[0])):
    #         top_line += "---+"
    #     print(top_line)

    #     for y in range(len(self.grid_binario)):
    #         line_walls = "|"
    #         line_floor = "+"
    #         for x in range(len(self.grid_binario[0])):
    #             #print(f"celda: {x} {y}")
    #             cell = self.get_cell(x, y)

                
    #             if self.cfg.entry_x_y ==[x, y]:
    #                 content = " E "
    #             elif self.cfg.exit_x_y == [x, y]:
    #                 content = " S "
    #             elif cell.casilla_42:
    #                 content = "42 "
    #             else:
    #                 content = "   "


    #             if cell.walls[Direccion.ESTE]:
    #                 line_walls += content + "|"
    #             else:
    #                 line_walls += content + " "

      
    #             if cell.walls[Direccion.SUR]:
    #                 line_floor += "---+"
    #             else:
    #                 line_floor += "   +"

    #         print(line_walls)
    #         print(line_floor)
    
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
    
    def shortest_path(self):
        # sy = self.cfg.entry_y // 2
        # sx = self.cfg.entry_x // 2
        # ey = self.cfg.exit_y // 2
        # ex = self.cfg.exit_x // 2
        sx, sy = self.cfg.entry_x_y
        ex, ey = self.cfg.exit_x_y

        H = len(self.grid_binario)
        W = len(self.grid_binario[0])

        queue = deque([(sy, sx)])
        visited = {(sy, sx)}
        parent = {}  # (ny, nx) → ((y, x), 'dirección')

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

        # ✅ reconstruir string de direcciones
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
        # print(self.camino)
        return self.camino
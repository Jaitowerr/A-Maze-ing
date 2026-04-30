import random
from Celda import Celda
from Direcccion import Direccion, OPUESTO, MOVES
class Mapa():
    def __init__(self, width, height, seed=42, perfect=True):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect


        self.grid = [
            [Celda() for _ in range(width)]
            for _ in range(height)
        ]


        self.entry = None
        self.exit = None

 
        random.seed(self.seed)

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height


    def get_cell(self, x, y) -> Celda:
            """
            Devuelve la celda en la posición (x, y)
            """
            return self.grid[y][x]


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


    def generate_maze(self, x=0, y=0):
            """
            DFS recursivo con backtracking.

            Si perfect=True:
            genera un perfect maze automáticamente.
            """
            current = self.get_cell(x, y)
            current.visited = True

            neighbors = self.get_unvisited_neighbors(x, y)
            random.shuffle(neighbors)

            for nx, ny, direction in neighbors:
                neighbor = self.get_cell(nx, ny)

                if not neighbor.visited:
                    self.remove_wall(x, y, nx, ny, direction)
                    self.generate_maze(nx, ny)
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




    def set_entry_exit(self):
        """
        Entrada: esquina superior izquierda
        Salida: esquina inferior derecha
        """

        self.entry = (0, 0)
        self.exit = (self.width - 1, self.height - 1)

    def mark_42(self):
        """
        Reserva celdas para dibujar el patrón '42'
        usando celdas completamente cerradas.
        """

     
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

            self.grid[y][x].es_42 = True
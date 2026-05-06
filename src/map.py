from dataclasses import dataclass
from typing import Optional


@dataclass
class MazeConfig:
    width: int
    height: int
    entry_x_y: list[int, int]
    entry_x: int
    entry_y: int
    exit_x_y: list[int, int]
    exit_x: int
    exit_y: int
    output_file: str
    perfect: bool
    center_42: bool
    seed: Optional[int] = None
    algorithm: Optional[str] = None
    display: Optional[str] = None
    grid: list[list[int]] = None
    cell_size: int = None

    def __post_init__(self):
        self.iniciando_grid()
        self.construir_42()
        self.añadir_cuadricula()
        self.proteger_42()
        self.añadir_marco()
        self.verificar_entrada_salida()

    def iniciando_grid(self) -> None:
        self.grid = [[1 for _ in range(self.width)]
                     for _ in range(self.height)]

    def print_grid(self) -> None:
        for row in self.grid:
            for idx, val in enumerate(row):
                end = ", " if idx < len(row) - 1 else ""
                print(val, end=end)
            print()

    def construir_42(self) -> None:
        if not self.center_42:
            return
        # if (self.width % 2 != 0) or (self.height % 2 != 0):
        #     self.center_42 = False
        patron = [
            "X    XXXX",
            "X       X",
            "X  X    X",
            "XXXX XXXX",
            "   X X   ",
            "   X X   ",
            "   X XXXX",
        ]
        pat_w, pat_h = 9, 7
        top = (self.height - pat_h) // 2
        left = (self.width - pat_w) // 2
        for r in range(pat_h):
            row = patron[r]
            for c in range(pat_w):
                if row[c] == "X":
                    if self.grid[top + r][left + c] == 1:
                        self.grid[top + r][left + c] = 2

    def añadir_marco(self):
        top = [2] * self.width
        bot = [2] * self.width
        # for _ in range(self.width):
        #     top.append(2)
        #     bot.append(2)
        self.grid.insert(0, top)
        self.grid.append(bot)

        for row in self.grid:
            row.insert(0, 2)
            row.append(2)

        self.entry_y += 1
        self.exit_y += 1
        self.entry_x += 1
        self.exit_x += 1
        self.width += 2
        self.height += 2

    def añadir_cuadricula(self) -> None:

        old_h = len(self.grid)
        # old_w = max(len(r) for r in self.grid) if old_h > 0 else 0

        new_grid = []

        for i, old_row in enumerate(self.grid):
            new_row = []
            for j, cell in enumerate(old_row):
                new_row.append(cell)
                if j != len(old_row) - 1:
                    new_row.append(3)
            new_grid.append(new_row)

            # if i != old_h - 1:
            #     sep_row = [3] * len(new_row)
            #     new_grid.append(sep_row)

            if i != old_h - 1:
                # fila separadora: 3, espacio, 3, espacio, ...
                sep_row = [3 if k %
                           2 == 0 else ' ' for k in range(len(new_row))]
                new_grid.append(sep_row)

        self.grid = new_grid

        self.height = len(self.grid)
        self.width = max(len(r) for r in self.grid) if self.height > 0 else 0

        self.entry_x = self.entry_x * 2
        self.exit_x = self.exit_x * 2
        self.entry_y = self.entry_y * 2
        self.exit_y = self.exit_y * 2


    def proteger_42(self) -> None:
        if not self.center_42:
            return

        rows = len(self.grid)

        to_set = set()  # conjunto de (r,c) a cambiar a 2

        for r in range(rows):
            row = self.grid[r]
            for c in range(len(row)):
                if row[c] == 2:
                    # izquierda
                    if c - 1 >= 0 and self.grid[r][c - 1] == 3:
                        to_set.add((r, c - 1))
                    # derecha
                    if c + 1 < len(row) and self.grid[r][c + 1] == 3:
                        to_set.add((r, c + 1))
                    # arriba
                    if r - 1 >= 0 and c < len(self.grid[r - 1]) and self.grid[r - 1][c] == 3:
                        to_set.add((r - 1, c))
                    # abajo
                    if r + 1 < rows and c < len(self.grid[r + 1]) and self.grid[r + 1][c] == 3:
                        to_set.add((r + 1, c))

        # aplicar cambios
        for (r, c) in to_set:
            self.grid[r][c] = 2


    def verificar_entrada_salida(self):
        import sys
        errores = []
 
        celda_entrada = self.grid[self.entry_y][self.entry_x]
        celda_salida = self.grid[self.exit_y][self.exit_x]

 
        if celda_entrada == 2:
            errores.append(
                f"Error: La entrada {self.entry_x_y} cae sobre una celda "
                f"bloqueada (marco o patrón 42). Elige otra posición."
            )
 
        if celda_salida == 2:
            errores.append(
                f"Error: La salida {self.exit_x_y} cae sobre una celda "
                f"bloqueada (marco o patrón 42). Elige otra posición."
            )
 
        if errores:
            print("\nErrores en la configuración del laberinto:")
            for e in errores:
                print("  - ", e)
            sys.exit(1)
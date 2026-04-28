from dataclasses import dataclass
from typing import Optional


@dataclass
class MazeConfig:
    width: int
    height: int
    entry_x: int
    entry_y: int
    exit_x: int
    exit_y: int
    output_file: str
    perfect: bool
    center_42: bool
    seed: Optional[int] = None
    algorithm: Optional[str] = None
    display: Optional[str] = None
    grid: list[list[int]] = None

    def __post_init__(self):
        self.iniciando_grid()
        self.construir_42()
        self.añadir_marco()

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
                        self.grid[top + r][left + c] = 'O'  # ó

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

    def añadir_cuadricula(self):
        pass

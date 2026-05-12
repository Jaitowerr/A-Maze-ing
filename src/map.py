from dataclasses import dataclass
from typing import Optional, Any
import random


@dataclass
class MazeConfig:
    width: int
    height: int
    entry_x_y: list[int]
    entry_x: int
    entry_y: int
    exit_x_y: list[int]
    exit_x: int
    exit_y: int
    output_file: str
    perfect: bool
    center_42: bool
    seed: Optional[Any] = None
    algorithm: Optional[str] = None
    display: Optional[str] = None
    grid: Optional[list[list[int]]] = None
    cell_size: Optional[int] = None
    pixel: Optional[int] = None
    rut: Optional[str] = None

    def __post_init__(self) -> None:
        self.init_grid()
        self.build_42()
        self.add_grid_lines()
        self.protect_42()
        self.add_frame()
        self.check_entry_exit()
        random.seed(self.seed)

    def init_grid(self) -> None:
        self.grid = [[1 for _ in range(self.width)]
                     for _ in range(self.height)]

    def print_grid(self) -> None:
        assert self.grid is not None
        for row in self.grid:
            for idx, val in enumerate(row):
                end = ", " if idx < len(row) - 1 else ""
                print(val, end=end)
            print()

    def build_42(self) -> None:
        if not self.center_42:
            return
        assert self.grid is not None
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
                        self.grid[top + r][left + c] = 42

    def add_frame(self) -> None:
        assert self.grid is not None
        top = [2] * self.width
        bot = [2] * self.width

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

    def add_grid_lines(self) -> None:
        assert self.grid is not None
        old_h = len(self.grid)

        new_grid = []

        for i, old_row in enumerate(self.grid):
            new_row = []
            for j, cell in enumerate(old_row):
                new_row.append(cell)
                if j != len(old_row) - 1:
                    new_row.append(3)
            new_grid.append(new_row)

            if i != old_h - 1:
                sep_row = [3 if k %
                           2 == 0 else 2 for k in range(len(new_row))]
                new_grid.append(sep_row)

        self.grid = new_grid

        self.height = len(self.grid)
        self.width = max(len(r) for r in self.grid) if self.height > 0 else 0

        self.entry_x = self.entry_x * 2
        self.exit_x = self.exit_x * 2
        self.entry_y = self.entry_y * 2
        self.exit_y = self.exit_y * 2

    def protect_42(self) -> None:
        if not self.center_42:
            return
        assert self.grid is not None
        rows = len(self.grid)

        to_set = set()

        for r in range(rows):
            row = self.grid[r]
            for c in range(len(row)):
                if row[c] == 42:
                    # izquierda
                    if c - 1 >= 0 and self.grid[r][c - 1] == 3:
                        to_set.add((r, c - 1))
                    # derecha
                    if c + 1 < len(row) and self.grid[r][c + 1] == 3:
                        to_set.add((r, c + 1))
                    # arriba
                    if (r - 1 >= 0 and c < len(self.grid[r - 1])
                            and self.grid[r - 1][c] == 3):
                        to_set.add((r - 1, c))
                    # abajo
                    if (r + 1 < rows and c < len(self.grid[r + 1])
                            and self.grid[r + 1][c] == 3):
                        to_set.add((r + 1, c))

        for (r, c) in to_set:
            self.grid[r][c] = 2

    def check_entry_exit(self) -> None:
        import sys
        assert self.grid is not None
        errors = []

        entry_cell = self.grid[self.entry_y][self.entry_x]
        exit_cell = self.grid[self.exit_y][self.exit_x]

        if entry_cell == 42:
            errors.append(
                f"Error: Entry {self.entry_x_y} falls on a blocked cell "
                f"(frame or 42 pattern). Choose another position."
            )

        if exit_cell == 42:
            errors.append(
                f"Error: Exit {self.exit_x_y} falls on a blocked cell "
                f"(frame or 42 pattern). Choose another position."
            )

        if errors:
            print("\nErrors in maze configuration:")
            for e in errors:
                print("  - ", e)
            sys.exit(1)

    # Spanish aliases were removed; names are English-only now

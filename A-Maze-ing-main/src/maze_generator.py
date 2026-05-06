from src.map import MazeConfig
import random


class MazeGenerator:
    def __init__(self, cfg: MazeConfig) -> None:
        self.cfg = cfg
        self.grid = [row.copy() for row in cfg.grid]
        self.grid_binario = None
        self.grid_hexadecimal = None
        self.grid[self.cfg.entry_y][self.cfg.entry_x] = 4
        self.grid[self.cfg.exit_y][self.cfg.exit_x] = 5

    def algoritmo(self) -> None:
        random.seed(self.cfg.seed)
        if self.cfg.algorithm == 'recursive_backtracker':
            from .algorithm import recursive_backtracker
            ok = recursive_backtracker.run(self)


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

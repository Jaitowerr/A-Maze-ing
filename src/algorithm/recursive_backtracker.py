import random
from ..maze_generator import MazeGenerator


def run(gen: MazeGenerator) -> None:
    cfg = gen.cfg
    grid = gen.grid

    sy, sx = cfg.entry_y, cfg.entry_x
    # ey, ex = cfg.exit_y, cfg.exit_x

    H = len(grid)
    W = len(grid[0])
    moves = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    stack = [(sy, sx)]
    visited = {(sy, sx)}

    while stack:
        y, x = stack[-1]
        dirs = moves[:]
        random.shuffle(dirs)
        moved = False

        for dy, dx in dirs:
            ny, nx = y + dy, x + dx
            py, px = y + dy // 2, x + dx // 2

            if not (0 <= ny < H and 0 <= nx < W):
                continue
            if grid[py][px] == 2 or grid[ny][nx] == 2:
                continue
            if (ny, nx) in visited:
                continue
            if grid[ny][nx] not in (1, 0, 5):
                continue

            if grid[py][px] == 3:
                grid[py][px] = 0

            if grid[ny][nx] == 1:
                grid[ny][nx] = 0

            visited.add((ny, nx))
            stack.append((ny, nx))
            moved = True
            break

        if not moved:
            stack.pop()

    if not cfg.perfect:
        paredes = []
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                # Una pared es un 3 que NO fue abierto por el algoritmo
                if grid[y][x] != 3:
                    continue

                # pared vertical (separa izquierda/derecha)
                if y % 2 == 1 and x % 2 == 0:
                    c1, c2 = (y, x - 1), (y, x + 1)
                # pared horizontal (separa arriba/abajo)
                elif y % 2 == 0 and x % 2 == 1:
                    c1, c2 = (y - 1, x), (y + 1, x)
                else:
                    continue

                # Solo si ambas celdas vecinas son parte del laberinto
                if c1 in visited and c2 in visited:
                    paredes.append((y, x))

        n_romper = max(1, len(paredes) // 3)
        for y, x in random.sample(paredes, min(n_romper, len(paredes))):
            grid[y][x] = 0

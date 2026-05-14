from ..maze_generator import MazeGenerator
import random
from ..dsu import DSU


def run(map: MazeGenerator) -> None:
    """Generate a maze using Kruskal's algorithm.

    The function builds a list of candidate walls, shuffles them and
    removes walls that connect two different components. Optionally
    some loops are added when the maze is not perfect.

    Args:
        map: MazeGenerator instance with grid and configuration.

    Returns:
        None
    """
    sy, sx = map.cfg.entry_y, map.cfg.entry_x
    ey, ex = map.cfg.exit_y, map.cfg.exit_x
    cells = []
    for y in range(map.cfg.height):
        for x in range(map.cfg.width):
            if map.grid[y][x] == 1 or map.grid[y][x] in (4, 5):
                cells.append((y, x))
    dsu = DSU()
    for cell in cells:
        dsu._parent[cell] = cell

    walls = []
    for y in range(map.cfg.height):
        for x in range(map.cfg.width):
            if map.grid[y][x] == 3:
                if x - 1 >= 0 and x + 1 < map.cfg.width:
                    if map.grid[y][x-1] != 2 and map.grid[y][x+1] != 2:
                        walls.append((y, x, (y, x-1), (y, x+1)))
                if y - 1 >= 0 and y + 1 < map.cfg.height:
                    if map.grid[y-1][x] != 2 and map.grid[y+1][x] != 2:
                        walls.append((y, x, (y-1, x), (y+1, x)))
    random.shuffle(walls)
    for wy, wx, c1, c2 in walls:
        if c1 not in dsu._parent or c2 not in dsu._parent:
            continue
        if dsu.find(c1) != dsu.find(c2):
            dsu.union(c1, c2)
            map.grid[wy][wx] = 0
            y1, x1 = c1
            y2, x2 = c2
            if map.grid[y1][x1] == 1:
                map.grid[y1][x1] = 0
            if map.grid[y2][x2] == 1:
                map.grid[y2][x2] = 0
    map.grid[sy][sx] = 4
    map.grid[ey][ex] = 5
    if not map.cfg.perfect:
        add_loops(map, 0.10)


def add_loops(map: MazeGenerator, probability: float = 0.10) -> None:
    """Randomly remove some walls to create loops in the maze.

    Args:
        map: MazeGenerator with grid data.
        probability: Chance to remove a valid wall.

    Returns:
        None
    """

    H = len(map.grid)
    W = len(map.grid[0])

    for y in range(1, H - 1):
        for x in range(1, W - 1):

            if map.grid[y][x] != 3:
                continue

            # only valid walls

            # vertical wall
            if y % 2 == 1 and x % 2 == 0:
                c1 = (y, x - 1)
                c2 = (y, x + 1)

            # horizontal wall
            elif y % 2 == 0 and x % 2 == 1:
                c1 = (y - 1, x)
                c2 = (y + 1, x)

            else:
                # this is a pillar -> do not break
                continue

            # both neighbor cells must be passages
            if map.grid[c1[0]][c1[1]] not in (0, 4, 5):
                continue

            if map.grid[c2[0]][c2[1]] not in (0, 4, 5):
                continue

            if random.random() < probability:
                map.grid[y][x] = 0

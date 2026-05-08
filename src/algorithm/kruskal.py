from ..maze_generator import MazeGenerator
import random
from ..dsu import DSU

def add_loops(map:MazeGenerator, probability=0.10):
    heigh = len(map.grid)
    width = len(map.grid[0])
    for y in range(1, heigh - 1):
        for x in range(1, width - 1):
            if map.grid[y][x] != 3:
                continue
            if random.random() > probability:
                continue
            if map.grid[y][x] == 2:
                continue
            map.grid[y][x] = 0
    

def run(map: MazeGenerator):
    sy, sx = map.cfg.entry_y, map.cfg.entry_x
    ey, ex = map.cfg.exit_y, map.cfg.exit_x
    cells = []
    for y in range(map.cfg.height):
        for x in range(map.cfg.width):
            if map.grid[y][x] == 1 or map.grid[y][x] in (4,5):
                cells.append((y,x))
    dsu = DSU()
    for cell in cells:
        dsu._parent[cell] = cell
    
    walls = []
    for y in range(map.cfg.height):
        for x in range(map.cfg.width):
            if map.grid[y][x] == 3:
                if x - 1 >= 0 and x + 1 < map.cfg.width:
                    if map.grid[y][x-1] != 2 and map.grid[y][x+1] != 2:
                        walls.append((y,x,(y,x-1),(y,x+1)))
                if y - 1 >= 0 and y + 1 < map.cfg.height:
                    if map.grid[y-1][x] != 2 and map.grid[y+1][x] != 2:
                        walls.append((y,x,(y-1,x),(y+1,x)))
    random.shuffle(walls)
    for  wy, wx, c1, c2 in walls:
        if c1 not in dsu._parent or c2 not in dsu._parent:
            continue
        if dsu.find(c1) != dsu.find(c2):
            dsu.union(c1,c2)
            map.grid[wy][wx] = 0
            y1, x1 = c1
            y2, x2 = c2
            if map.grid[y1][x1] == 1:
                map.grid[y1][x1] = 0
            if map.grid[y2][x2] == 1:
                map.grid[y2][x2] = 0
    map.grid[sy][sx] = 4
    map.grid[ey][ex] = 5
    if map.cfg.perfect == False:
        add_loops(map, 0.15)
            
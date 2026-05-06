from ..maze_generator import MazeGenerator
import random

def run(map: MazeGenerator, x=0, y=0):
    current = map.get_cell(x, y)
    current.visited = True

    neighbors = map.get_unvisited_neighbors(x, y)
    random.shuffle(neighbors)

    for nx, ny, direction in neighbors:
        neighbor = map.get_cell(nx, ny)
        if not neighbor.visited:
            map.remove_wall(x, y, nx, ny, direction)
            map.generate_maze(nx, ny)
from Celda import Celda
from Mapa import Mapa
from Direcccion import Direccion, OPUESTO, MOVES
import pygame


CELL_SIZE = 40
WIDTH = 20
HEIGHT = 20

SCREEN_WIDTH = WIDTH * CELL_SIZE
SCREEN_HEIGHT = HEIGHT * CELL_SIZE
def main():
    


    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Generator")

    clock = pygame.time.Clock()
    maze = Mapa(
        width=WIDTH,
        height=HEIGHT,
        seed=42,
        perfect=True
    )
    maze.mark_42()
    maze.generate_maze(0, 0)
    maze.set_entry_exit()


    # si no es perfect → añadir ciclos
    if not maze.perfect:
        maze.add_loops(probability=0.10)

    # imprimir resultado
    maze.print_maze()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_maze(screen, maze)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_maze(screen, maze: Mapa):
    screen.fill((255, 255, 255))

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)

            px = x * CELL_SIZE
            py = y * CELL_SIZE

            # NORTH
            if cell.walls[Direccion.NORTE]:
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (px, py),
                    (px + CELL_SIZE, py),
                    2
                )

            # SOUTH
            if cell.walls[Direccion.SUR]:
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (px, py + CELL_SIZE),
                    (px + CELL_SIZE, py + CELL_SIZE),
                    2
                )

            # WEST
            if cell.walls[Direccion.OESTE]:
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (px, py),
                    (px, py + CELL_SIZE),
                    2
                )

            # EAST
            if cell.walls[Direccion.ESTE]:
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (px + CELL_SIZE, py),
                    (px + CELL_SIZE, py + CELL_SIZE),
                    2
                )

if __name__ == "__main__":
    main()
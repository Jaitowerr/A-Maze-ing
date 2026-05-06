from mlx import Mlx
from Mapa import Mapa
from Direcccion import Direccion
from Celda import Celda

CELL_SIZE = 40
WIDTH = 20
HEIGHT = 20

SCREEN_WIDTH = WIDTH * CELL_SIZE
SCREEN_HEIGHT = HEIGHT * CELL_SIZE


def put_pixel(data, size_line, x, y, color):
    """
    Escribe un pixel directamente en el buffer de imagen.
    Formato: BGRA (4 bytes por pixel)
    """

    if x < 0 or y < 0:
        return

    if x >= SCREEN_WIDTH or y >= SCREEN_HEIGHT:
        return
    pixel_index = y * size_line + x * 4

    blue = color & 0xFF
    green = (color >> 8) & 0xFF
    red = (color >> 16) & 0xFF

    data[pixel_index + 0] = blue
    data[pixel_index + 1] = green
    data[pixel_index + 2] = red
    data[pixel_index + 3] = 255  # alpha importante


def draw_line(data, size_line, x1, y1, x2, y2, color):
    """
    Dibuja una línea pixel por pixel
    """

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    steps = max(dx, dy)

    if steps == 0:
        put_pixel(data, size_line, x1, y1, color)
        return

    for i in range(steps + 1):
        x = int(x1 + (x2 - x1) * i / steps)
        y = int(y1 + (y2 - y1) * i / steps)

        put_pixel(data, size_line, x, y, color)


def draw_cell(data, size_line, px, py, cell):
    WALL_COLOR = 0xFFFFFF

    # NORTH
    if cell.walls[Direccion.NORTE]:
        draw_line(
            data,
            size_line,
            px,
            py,
            px + CELL_SIZE,
            py,
            WALL_COLOR
        )

    # SOUTH
    if cell.walls[Direccion.SUR]:
        draw_line(
            data,
            size_line,
            px,
            py + CELL_SIZE,
            px + CELL_SIZE,
            py + CELL_SIZE,
            WALL_COLOR
        )

    # WEST
    if cell.walls[Direccion.OESTE]:
        draw_line(
            data,
            size_line,
            px,
            py,
            px,
            py + CELL_SIZE,
            WALL_COLOR
        )

    # EAST
    if cell.walls[Direccion.ESTE]:
        draw_line(
            data,
            size_line,
            px + CELL_SIZE,
            py,
            px + CELL_SIZE,
            py + CELL_SIZE,
            WALL_COLOR
        )


def draw_maze(m, mlx, win, maze):
    """
    Render completo usando mlx_new_image()
    """

    # Crear imagen
    img = m.mlx_new_image(
        mlx,
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )

    # Obtener buffer
    data, bpp, size_line, endian = m.mlx_get_data_addr(img)

    # Dibujar todas las celdas
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)

            px = x * CELL_SIZE
            py = y * CELL_SIZE

            draw_cell(
                data,
                size_line,
                px,
                py,
                cell
            )

    # Mostrar imagen en ventana
    m.mlx_put_image_to_window(
        mlx,
        win,
        img,
        0,
        0
    )

    m.mlx_do_sync(mlx)

    # Texto de prueba
    m.mlx_string_put(
        mlx,
        win,
        10,
        10,
        0x00FF00,
        "Maze generado con MLX Image Buffer"
    )


def close_window(param):
    param.mlx_loop_exit(param.mlx_ptr)


def key_hook(key, param):
    """
    ESC para salir
    """

    if key == 65307:
        param.mlx_loop_exit(param.mlx_ptr)


def main():
    # Inicializar MLX
    m = Mlx()
    m.mlx_ptr = m.mlx_init()

    # Crear ventana
    win = m.mlx_new_window(
        m.mlx_ptr,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "42 A-Maze-ing"
    )

    # Crear maze
    maze = Mapa(
        width=WIDTH,
        height=HEIGHT,
        seed=42,
        perfect=True
    )

    maze.mark_42()
    maze.generate_maze(0, 0)
    maze.set_entry_exit()

    if not maze.perfect:
        maze.add_loops(probability=0.10)

    maze.print_maze()

    # Hooks
    m.mlx_key_hook(
        win,
        key_hook,
        m
    )

    # Botón X de la ventana
    m.mlx_hook(
        win,
        17,
        0,
        close_window,
        m
    )

    # Dibujar maze
    draw_maze(
        m,
        m.mlx_ptr,
        win,
        maze
    )

    # Loop principal
    m.mlx_loop(m.mlx_ptr)


if __name__ == "__main__":
    main()
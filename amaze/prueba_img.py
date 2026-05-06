from mlx import Mlx
from Mapa import Mapa
from Direcccion import Direccion
from Celda import Celda

CELL_SIZE = 40
WIDTH = 20
HEIGHT = 20

SCREEN_WIDTH = WIDTH * CELL_SIZE
SCREEN_HEIGHT = HEIGHT * CELL_SIZE

def draw_tile(m, mlx, win, img,x,y):
    m.mlx_put_image_to_window(mlx,win,img,x,y)

#Solucion en base al hexadecimal y binario
def get_tile_key(cell: Celda):
    n = int(cell.walls[Direccion.NORTE])
    s = int(cell.walls[Direccion.SUR])
    e = int(cell.walls[Direccion.ESTE])
    o = int(cell.walls[Direccion.OESTE])
    return f"{n}{s}{e}{o}"

def load_tiles(m, mlx):
    tiles = {}
    for i in range(16):
        key = format(i, "04b")
        path = f"./img/{key}.png"
        img,_,_ = m.mlx_png_file_to_image(mlx, path)
        tiles[key] = img
    
    tiles["entry"],_,_ = m.mlx_png_file_to_image(mlx, "./img/pacman1.png")
    tiles["exit"],_,_ = m.mlx_png_file_to_image(mlx, "./img/pj.png")
    return tiles
'''
def draw_maze(m,mlx,win,maze: Mapa):
    wall_img,_,_ = m.mlx_png_file_to_image(mlx, "./img/roca.png")
    floor_img,_,_ = m.mlx_png_file_to_image(mlx, "./img/tile00.png")
    entry_img,_,_ = m.mlx_png_file_to_image(mlx, "./img/player_E00.png")
    exit_img,_,_ = m.mlx_png_file_to_image(mlx, "./img/roca.png")
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x,y)
            px = x * CELL_SIZE
            py = y *CELL_SIZE
            #Necesitamos un fondo
            draw_tile(m, mlx, win, floor_img, px, py)
            #Deteccion de entrada y salida
            if maze.entry == (x,y):
                draw_tile(m,mlx,win,entry_img,px,py)
            elif maze.exit == (x,y):
                draw_tile(m,mlx,win,exit_img,px,py)
            #deteccion de paredes
            if cell.walls[Direccion.NORTE]:
                draw_tile(m,mlx,win,wall_img,px,py)
            if cell.walls[Direccion.SUR]:
                draw_tile(m,mlx,win,wall_img,px,py)
            if cell.walls[Direccion.ESTE]:
                draw_tile(m,mlx,win,wall_img,px,py)
            if cell.walls[Direccion.OESTE]:
                draw_tile(m,mlx,win,wall_img,px,py)
    m.mlx_string_put(mlx,win,10,10,0xFFFFFF,"maze png")
'''

def draw_maze(m,mlx,win,maze: Mapa,tiles):
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x,y)
            px = x *CELL_SIZE
            py = y *CELL_SIZE
            if maze.entry == (x,y):
                img = tiles["entry"]
            elif maze.exit == (x,y):
                img = tiles["exit"]
            else:
                key = get_tile_key(cell)
                img = tiles[key]
            m.mlx_put_image_to_window(mlx,win,img,px,py)

def close_window(param):
    param.mlx_loop_exit(param.mlx_ptr)

def key_hook(key, param):
    print(key)
    if key == 65307:
        param.mlx_loop_exit(param.mlx_ptr)
    if 65361 <= key <= 65364:
        pass #gamecontrol
    if key == 112:
        pass #gamecontrol pause false
    elif key == 49:
        pass#es el 1
    elif key == 50:
        pass#es el 2


def main():
    m = Mlx()
    m.mlx_ptr = m.mlx_init()
    win = m.mlx_new_window(
        m.mlx_ptr,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "42 maze"
    )
    maze = Mapa(
        width = WIDTH,
        height = HEIGHT,
        seed = 42,
        perfect = True
    )
    maze.mark_42()
    maze.generate_maze(0,0)
    maze.set_entry_exit()

    if not maze.perfect:
        maze.add_loops(probability=0.10)
    m.mlx_key_hook(win,key_hook,m)
    maze.print_maze()
    tiles = load_tiles(m, m.mlx_ptr)
    m.mlx_hook(win,17,0,close_window,m)
    draw_maze(m,m.mlx_ptr,win,maze, tiles)
    m.mlx_loop(m.mlx_ptr)

if __name__ == "__main__":
    main()
#! /usr/bin/env python3

import sys
import os
from Direcccion import Direccion
from Celda import Celda
from mlx import Mlx

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

def programa(parse_config):
    print('Ejecutando programa...')
    print(parse_config)


def init_sys() -> None:
    errores = []

    if len(sys.argv) < 2:
        errores.append('Error: No se ha proporcionado el archivo de '
                       'configuración.')

    if len(sys.argv) > 2:
        errores.append('Error: Demasiados parámetros.')

    if len(sys.argv) == 2:
        if not os.path.exists(sys.argv[1]):
            errores.append(f"Error: El archivo '{sys.argv[1]}' no existe.")

        if sys.argv[1] != 'config.txt':
            errores.append("Error: El nombre del archivo no es config.txt")

    if errores:
        print('\nSe encontraron los siguientes errores:')
        for er in errores:
            print('  - ', er)
        print('\n*** Uso correcto: python3 a_maze_ing.py config.txt\n')
        sys.exit(1)
    else:
        return

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

if __name__ == '__main__':
    init_sys()
    from src.config_parser import parse_config
    cfg = parse_config(sys.argv[1]) # objeto, listo para enviar a cualquier sitio
    # programa(cfg)
    # cfg.print_grid()
    
    print('-' * 55)
    print('-' * 55)
    from src.maze_generator import MazeGenerator
    gen = MazeGenerator(cfg)
    m = Mlx()
    m.mlx_ptr = m.mlx_init()
    win = m.mlx_new_window(
        m.mlx_ptr,
        cfg.width*cfg.cell_size,
        cfg.height*cfg.cell_size,
        "42 maze"
    )
    m.mlx_key_hook(win,key_hook,m)
    tiles = load_tiles(m, m.mlx_ptr)
    m.mlx_hook(win,17,0,close_window,m)
    m.mlx_loop(m.mlx_ptr)
    # gen.print_grid()
    print('-' * 55)
    print('-' * 55)
    print('-' * 55)
    print('-' * 55)
    gen.algoritmo()
    gen.print_grid()
    # print('-' * 55)
    # print('-' * 55)
    # cfg.print_grid()
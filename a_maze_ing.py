#! /usr/bin/env python3

import sys
import os
from src.Direcccion import Direccion
from src.Celda import Celda
from src.GameControl import GameControl
from src.Player import Player
from mlx import Mlx

def draw_tile(m, mlx, win, img,x,y):
    m.mlx_put_image_to_window(mlx,win,img,x,y)



def load_tiles(m, mlx):
    tiles = {}
    for i in range(16):
        key = format(i, "04b")
        path = f"./img2/{key}.png"
        img,_,_ = m.mlx_png_file_to_image(mlx, path)
        tiles[key] = img
    
    tiles["entry"],_,_ = m.mlx_png_file_to_image(mlx, "./img/pj.png")
    tiles["exit"],_,_ = m.mlx_png_file_to_image(mlx, "./img/pj.png")
    tiles["player"],_,_ = m.mlx_png_file_to_image(mlx, "./img/pj.png")
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

def key_hook(key, control:GameControl):
    if key == 65307:
        control._m.mlx_loop_exit(control._m.mlx_ptr)
    if 65361 <= key <= 65364:
        control.move_player(key)
    if key == 112:
        pass #gamecontrol pause false
    if key == 109:
        control.crear_ascii()
    elif key == 49:
        control.crear_mapa2()
    elif key == 50:
        control.crear_mapa1()
        #control.crear_mapa1()


if __name__ == '__main__':
    init_sys()
    from src.config_parser import parse_config
    cfg = parse_config(sys.argv[1])
    from src.maze_generator import MazeGenerator
    gen = MazeGenerator(cfg)
    gen.docu_finish()
    print('Existen distintos algoritmos de ejecución, puedes ejegir entre : recursive_backtracker y kruskal')
    print(f'El algoritmo utilizdo es: {gen.cfg.algorithm}\n')
    if cfg.display == 'ascii':
        gen.print_maze()
        from src.ascii_menu import ascii_menu
        ascii_menu(gen)
    else:
        m = Mlx()
        m.mlx_ptr = m.mlx_init()
        win = m.mlx_new_window(
            m.mlx_ptr,
            len(gen.grid_binario[0]) * 40,
            len(gen.grid_binario) * 40,
            "42 maze"
        )
        tiles = load_tiles(m, m.mlx_ptr)
        player = Player((cfg.entry_x, cfg.entry_y), tiles["player"])
        control = GameControl(m, win, gen, player, tiles)
        control.crear_mapa2()
        player.render(m, win)
        m.mlx_key_hook(win, key_hook, control)
        m.mlx_hook(win, 17, 0, close_window, m)
        m.mlx_loop(m.mlx_ptr)
    # m = Mlx()
    # m.mlx_ptr = m.mlx_init()
    # win = m.mlx_new_window(
    #     m.mlx_ptr,
    #     len(gen.grid_binario[0])*40,
    #     len(gen.grid_binario)*40,
    #     "42 maze"
    # )
    # tiles = load_tiles(m, m.mlx_ptr)
    # player = Player((cfg.entry_x,cfg.entry_y), tiles["player"])
    # control = GameControl(m,win,gen,player, tiles)
    # control.crear_mapa2()
    # player.render(m,win)
    # m.mlx_key_hook(win,key_hook,control)
    
    # m.mlx_hook(win,17,0,close_window,m)
    # m.mlx_loop(m.mlx_ptr)

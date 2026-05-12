#! /usr/bin/env python3

import sys
import os
from src.GameControl import GameControl
from src.Player import Player
from src.map import MazeConfig
from mlx import Mlx  # type: ignore[import-untyped]


def draw_tile(m: Mlx, mlx: int, win: int, img: int, x: int, y: int) -> None:
    m.mlx_put_image_to_window(mlx, win, img, x, y)


def load_tiles(m: Mlx, mlx: int, cfg: MazeConfig) -> dict[str, int]:
    tiles = {}
    for i in range(16):
        key = format(i, "04b")
        path = f"./{cfg.rut}/{key}.png"
        img, _, _ = m.mlx_png_file_to_image(mlx, path)
        tiles[key] = img

    tiles["entry"], _, _ = m.mlx_png_file_to_image(
        mlx, f"./{cfg.rut}/entrada.png")
    tiles["exit"], _, _ = m.mlx_png_file_to_image(
        mlx, f"./{cfg.rut}/salida.png")
    tiles["player"], _, _ = m.mlx_png_file_to_image(
        mlx, f"./{cfg.rut}/mario1.png")
    return tiles


def programa(parse_config: str) -> None:
    print('Running program...')
    print(parse_config)


def init_sys() -> None:
    errors = []

    if len(sys.argv) < 2:
        errors.append('Error: The configuration file has not been provided.')

    if len(sys.argv) > 2:
        errors.append('Error: Too many parameters.')

    if len(sys.argv) == 2:
        if not os.path.exists(sys.argv[1]):
            errors.append(f"Error: The file '{sys.argv[1]}' does not exist.")

        if sys.argv[1] != 'config.txt':
            errors.append("Error: The file name is not config.txt")

    if errors:
        print('\nThe following errors were found:')
        for er in errors:
            print('  - ', er)
        print('\n*** Correct usage: python3 a_maze_ing.py config.txt\n')
        sys.exit(1)
    else:
        return


def close_window(param: Mlx) -> None:
    param.mlx_loop_exit(param.mlx_ptr)


def key_hook(key: int, control: GameControl) -> None:
    botones = [119, 115, 97, 100]
    if key == 65307:
        control._m.mlx_loop_exit(control._m.mlx_ptr)
    if 65361 <= key <= 65364 or key in botones:
        control.move_player(key)
    if key == 112:
        pass  # gamecontrol pause false
    if key == 109:
        control.create_ascii()
    elif key == 49:
        control.create_map_recursive()
    elif key == 50:
        control.create_map_kruskal()
    elif key == 99:
        control.change_color()
    elif key == 32:
        control.paint_path()


if __name__ == '__main__':
    init_sys()
    from src.config_parser import parse_config
    cfg = parse_config(sys.argv[1])
    from src.maze_generator import MazeGenerator
    gen = MazeGenerator(cfg)
    gen.write_output()
    print(
        'There are different execution algorithms, '
        'you can choose between: recursive_backtracker and kruskal')
    print(f'The algorithm used is: {gen.cfg.algorithm}\n')
    if cfg.display == 'ascii':
        gen.print_maze()
        from src.ascii_menu import ascii_menu
        ascii_menu(gen)
    else:
        assert gen.binary_grid is not None
        assert cfg.pixel is not None
        m = Mlx()
        m.mlx_ptr = m.mlx_init()
        win = m.mlx_new_window(
            m.mlx_ptr,
            len(gen.binary_grid[0]) * cfg.pixel,
            (len(gen.binary_grid) * cfg.pixel)+80,
            "42 maze"
        )
        tiles = load_tiles(m, m.mlx_ptr, cfg)
        player = Player((cfg.entry_x, cfg.entry_y), tiles["player"])
        control = GameControl(m, win, gen, player, tiles)
        control.create_map_recursive()
        # ESTO ES SOLO PRUEBA, LUEGO AÑADIRE UN BUEN FUNCIONAMIENTO
        # SOLO ES PARA LA SEPARACION DEL MAPA

        img, _, _ = m.mlx_png_file_to_image(
            m.mlx_ptr, "./img/play.png")
        esc, _, _ = m.mlx_png_file_to_image(
            m.mlx_ptr, "./img/esc.png")
        space, _, _ = m.mlx_png_file_to_image(
            m.mlx_ptr, "./img/space.png")
        c, _, _ = m.mlx_png_file_to_image(
            m.mlx_ptr, "./img/color.png")

        width_pixel = len(gen.binary_grid[0]) * cfg.pixel //4
        m.mlx_put_image_to_window(
            m.mlx_ptr, win, img, 0,
            (len(gen.binary_grid) * cfg.pixel)+20)

        m.mlx_put_image_to_window(
            m.mlx_ptr, win, esc, width_pixel,
            (len(gen.binary_grid) * cfg.pixel)+20)

        m.mlx_put_image_to_window(
            m.mlx_ptr, win, space, width_pixel*2,
            (len(gen.binary_grid) * cfg.pixel)+20)

        m.mlx_put_image_to_window(
            m.mlx_ptr, win, c, width_pixel*3,
            (len(gen.binary_grid) * cfg.pixel)+20)
        m.mlx_key_hook(win, key_hook, control)
        m.mlx_hook(win, 17, 0, close_window, m)
        m.mlx_loop(m.mlx_ptr)

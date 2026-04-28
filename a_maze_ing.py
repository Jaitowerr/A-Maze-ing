#! /usr/bin/env python3

import sys
import os


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


if __name__ == '__main__':
    init_sys()
    from src.config_parser import parse_config
    cfg = parse_config(sys.argv[1]) # objeto, listo para enviar a cualquier sitio
    # programa(cfg)
    
    cfg.print_grid()
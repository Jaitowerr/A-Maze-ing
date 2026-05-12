from .map import MazeConfig

import sys


def _validar_y_construir(dict_config: dict[str, str]) -> MazeConfig:
    errors = []
    required = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for r in required:
        if r not in dict_config:
            errors.append(f'Falta clave obligatoria: {r}')

    if errors:
        print('\nerrors en config.txt, falta de datos:')
        for e in errors:
            print('  - ', e)
        sys.exit(1)

    try:
        width = int(dict_config['WIDTH'])
    except ValueError:
        errors.append('WIDTH debe ser un entero')

    try:
        height = int(dict_config['HEIGHT'])
    except ValueError:
        errors.append('HEIGHT debe ser un entero')

    try:
        entry_x, entry_y = map(int, dict_config['ENTRY'].split(','))
    except ValueError:
        errors.append('ENTRY debe tener formato x,y de enteros. Ejemplo: 0,0')

    try:
        exit_x, exit_y = map(int, dict_config['EXIT'].split(','))
    except ValueError:
        errors.append('EXIT debe tener formato x,y de enteros. '
                       'Ejemplo: 19,14')

    if dict_config['PERFECT'] not in ('True', 'False'):
        errors.append('PERFECT debe ser True o False')
    else:
        perfect = dict_config['PERFECT'] == 'True'

    seed = None
    if 'SEED' in dict_config:
        try:
            seed = int(dict_config['SEED'])
        except ValueError:
            errors.append('SEED debe ser un entero')

    valid_algorithms = ('recursive_backtracker', 'kruskal')
    valid_display = ('mlx', 'ascii')

    algorithm = dict_config.get('ALGORITHM', 'recursive_backtracker')
    display = dict_config.get('DISPLAY', 'mlx')

    if display == 'mlx':
        if width > 90:
            errors.append('WIDTH debe ser menor de 90')
        if height > 45:
            errors.append('HEIGHT debe ser menor de 45')
    if display == 'ascii':
        if width > 60:
            errors.append('WIDTH debe ser menor de 90')
        # if height > 600:
        #     errors.append('HEIGHT debe ser menor de 45')

    if algorithm is not None and algorithm not in valid_algorithms:
        errors.append(
            f'ALGORITHM no válido: {algorithm}. Opciones: {valid_algorithms}'
        )

    if display is not None and display not in valid_display:
        errors.append(
            f'DISPLAY no válido: {display}. Opciones: {valid_display}')

    if errors:
        print('\nerrors en config.txt:')
        for e in errors:
            print('  - ', e)
        sys.exit(1)

    if width <= 0:
        errors.append('WIDTH debe ser mayor que 0')
    if height <= 0:
        errors.append('HEIGHT debe ser mayor que 0')

    if entry_x < 0 or entry_x >= width or entry_y < 0 or entry_y >= height:
        errors.append(
            f'ENTRY ({entry_x},{entry_y}) fuera de rango (0-{width - 1}, '
            f'0-{height - 1})')

    if exit_x < 0 or exit_x >= width or exit_y < 0 or exit_y >= height:
        errors.append(
            f'EXIT ({exit_x},{exit_y}) fuera de rango (0-{width - 1}, '
            f'0-{height - 1})')

    if entry_x == exit_x and entry_y == exit_y:
        errors.append('ENTRY y EXIT no pueden ser la misma casilla')

    if errors:
        print('\nerrors en config.txt:')
        for e in errors:
            print('  - ', e)
        sys.exit(1)

    center_42 = False if width < 9 or height < 7 else True

    return MazeConfig(
        width=width,
        height=height,
        entry_x=entry_x,
        entry_y=entry_y,
        entry_x_y=[entry_x, entry_y],
        exit_x=exit_x,
        exit_y=exit_y,
        exit_x_y=[exit_x, exit_y],
        output_file=dict_config['OUTPUT_FILE'],
        perfect=perfect,
        center_42=center_42,
        seed=seed,
        algorithm=algorithm,
        display=display,
        pixel=60,
        rut="img2/mario",
    )


def parse_config(config_txt: str) -> MazeConfig:
    errors = []
    dict_config = {}

    with open(config_txt) as config:
        for line in config:
            line = line.rstrip('\n')

            if not line.strip() or line.strip().startswith('#'):
                continue

            if '=' not in line:
                errors.append(f'Línea sin "=": {line}')
                continue

            key, value = line.split('=')[0], line.split('=')[1]

            if not key:
                errors.append(f'Clave vacía en línea: "{line}"')
                continue

            if not value:
                errors.append(f'Valor vacío en línea: "{line}"')
                continue

            if key != key.strip():
                errors.append(f'Espacios no permitidos en clave: "{line}"')
                continue

            if value != value.strip():
                errors.append(f'Espacios no permitidos en valor: "{line}"')
                continue
            if key in dict_config:
                errors.append(f'Clave duplicada: "{key}"')
                continue
            dict_config[key] = value

    if errors:
        print('\nerrors en config.txt:')
        for e in errors:
            print('  - ', e)
        sys.exit(1)
    else:
        return _validar_y_construir(dict_config)

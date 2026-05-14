from .map import MazeConfig

import sys


def _validate_and_build(dict_config: dict[str, str]) -> MazeConfig:
    """Validate parsed config values and return a MazeConfig.

    Args:
        dict_config: Mapping of configuration keys to raw string values.

    Returns:
        A validated MazeConfig instance constructed from inputs.

    Exits:
        Exits the program with code 1 and prints errors on invalid input.
    """
    errors = []
    required = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for r in required:
        if r not in dict_config:
            errors.append(f'Missing required key: {r}')

    if errors:
        print('\nerrors in config.txt, missing data:')
        for e in errors:
            print('  - ', e)
        sys.exit(1)

    try:
        width = int(dict_config['WIDTH'])
    except ValueError:
        errors.append('WIDTH must be an integer')

    try:
        height = int(dict_config['HEIGHT'])
    except ValueError:
        errors.append('HEIGHT must be an integer')

    try:
        entry_x, entry_y = map(int, dict_config['ENTRY'].split(','))
    except ValueError:
        errors.append(
            'ENTRY must be in the format x,y of integers. Example: 0,0')

    try:
        exit_x, exit_y = map(int, dict_config['EXIT'].split(','))
    except ValueError:
        errors.append('EXIT must have the format x,y of integers.'
                      'Example: 19,14')

    if dict_config['PERFECT'] not in ('True', 'False'):
        errors.append('PERFECT must be True or False')
    else:
        perfect = dict_config['PERFECT'] == 'True'

    seed = None
    if 'SEED' in dict_config:
        try:
            seed = int(dict_config['SEED']) or str(dict_config['SEED'])
        except ValueError:
            errors.append('SEED must be an integer or a string of characters')

    valid_algorithms = ('recursive_backtracker', 'kruskal')
    valid_display = ('mlx', 'ascii')

    algorithm = dict_config.get('ALGORITHM', 'recursive_backtracker')
    display = dict_config.get('DISPLAY', 'mlx')

    if display == 'mlx':
        if width > 90:
            errors.append('WIDTH must be less than 90')
        if height > 45:
            errors.append('HEIGHT must be less than 45')
    if display == 'ascii':
        if width > 60:
            errors.append('WIDTH must be less than 90')

    if algorithm is not None and algorithm not in valid_algorithms:
        errors.append(
            f'Invalid ALGORITHM: {algorithm}. Options: {valid_algorithms}'
        )

    if display is not None and display not in valid_display:
        errors.append(
            f'Invalid display: {display}. Options: {valid_display}')

    if errors:
        print('\nerrors in config.txt:')
        for e in errors:
            print('  - ', e)
        sys.exit(1)

    if width <= 0:
        errors.append('WIDTH must be greater than 0')
    if height <= 0:
        errors.append('HEIGHT must be greater than 0')

    if entry_x < 0 or entry_x >= width or entry_y < 0 or entry_y >= height:
        errors.append(
            f'ENTRY ({entry_x},{entry_y}) out of range (0-{width - 1}, '
            f'0-{height - 1})')

    if exit_x < 0 or exit_x >= width or exit_y < 0 or exit_y >= height:
        errors.append(
            f'EXIT ({exit_x},{exit_y}) out of range (0-{width - 1}, '
            f'0-{height - 1})')

    if entry_x == exit_x and entry_y == exit_y:
        errors.append('ENTRY and EXIT cannot be the same box')

    if errors:
        print('\nerrors in config.txt:')
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
    """Parse the config file and return a validated MazeConfig.

    The parser reads key=value lines, ignores comments and blank lines,
    and enforces simple formatting rules. It returns a MazeConfig built
    from the validated values.

    Args:
        config_txt: Path to the configuration file.

    Returns:
        A MazeConfig instance.

    Exits:
        Exits the program with code 1 and prints errors on invalid input.
    """
    errors: list[str] = []
    dict_config: dict[str, str] = {}

    with open(config_txt) as config:
        for line in config:
            line = line.rstrip('\n')

            if not line.strip() or line.strip().startswith('#'):
                continue

            if '=' not in line:
                errors.append(f'Line without "=":{line}')
                continue

            key, value = line.split('=')[0], line.split('=')[1]

            if not key:
                errors.append(f'Empty key online:"{line}"')
                continue

            if not value:
                errors.append(f'Empty value in line:"{line}"')
                continue

            if key != key.strip():
                errors.append(f'Spaces not allowed in the code:"{line}"')
                continue

            if value != value.strip():
                errors.append(f'Spaces not permitted in value:"{line}"')
                continue
            if key in dict_config:
                errors.append(f'Duplicate key:"{key}"')
                continue
            dict_config[key] = value

    if errors:
        print('\nerrors in config.txt:')
        for e in errors:
            print('  - ', e)
        sys.exit(1)
    else:
        return _validate_and_build(dict_config)

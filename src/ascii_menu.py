import os
import random
from .maze_generator import MazeGenerator


def print_menu(gen: "MazeGenerator") -> None:
    """Print the ASCII menu to the terminal.

    Args:
        gen: MazeGenerator instance used to query configuration.

    Returns:
        None
    """
    print('\033[97m')
    print("\n--- MENU ---")
    print("  1. Generate a new maze")
    print("  2. Show/Hide solution path")
    print("  3. Change wall color (random)")
    if gen.cfg.center_42:
        print("  4. Change '42' background color (random)")
        print("  5. Change wall style")
    else:
        print("  4. Change wall style")
    print("  q. Quit")


def color_random() -> str:
    """Return a random ANSI color escape sequence.

    Returns:
        A string with an ANSI color escape sequence.
    """
    texto = {
        "verde":      "\033[32m",
        "amarillo":   "\033[33m",
        "gris":       "\033[90m",
        "rojo_b":     "\033[91m",
        "rosa":       "\033[95m",
        "turquesa":   "\033[96m",
        "blanco_b":   "\033[97m"
    }
    return random.choice(list(texto.values()))


def _get_style_chars(style: int) -> dict[str, str]:
    """Return a mapping of characters for the given style id.

    Args:
        style: Style identifier number.

    Returns:
        A dict mapping style keys to display strings.
    """
    if style == 1:      # simples
        return {'PARED_H': '───', 'PARED_V': '│', 'ESQUINA': '┼'}
    elif style == 2:    # dobles
        return {'PARED_H': '═══', 'PARED_V': '║', 'ESQUINA': '╬'}
    elif style == 3:    # retro
        return {'PARED_H': '<o>', 'PARED_V': '|', 'ESQUINA': 'i'}
    elif style == 4:    # bloques sólidos
        return {'PARED_H': '███', 'PARED_V': '█', 'ESQUINA': '█'}
    elif style == 5:    # punteado
        return {'PARED_H': '···', 'PARED_V': ':', 'ESQUINA': '+'}
    elif style == 6:    # hash / dungeon
        return {'PARED_H': '###', 'PARED_V': '#', 'ESQUINA': '#'}
    elif style == 7:    # guiones
        return {'PARED_H': '---', 'PARED_V': '|', 'ESQUINA': '+'}
    elif style == 8:    # bloques degradados
        return {'PARED_H': '▓▓▓', 'PARED_V': '▓', 'ESQUINA': '▓'}
    elif style == 9:    # asteriscos
        return {'PARED_H': '***', 'PARED_V': '*', 'ESQUINA': '*'}
    elif style == 10:   # ondas
        return {'PARED_H': '~~~', 'PARED_V': '!', 'ESQUINA': '~'}
    return {'PARED_H': '---', 'PARED_V': '|', 'ESQUINA': '+'}


def ascii_menu(gen: MazeGenerator) -> bool:
    """Run an interactive ASCII menu loop for the maze.

    The function shows a menu, reads user input and triggers actions on
    the provided MazeGenerator. It returns False when the user quits.

    Args:
        gen: MazeGenerator instance to operate on.

    Returns:
        False when exiting the menu, True otherwise (keeps running).
    """
    print_menu(gen)
    color_grid = '\033[34m'
    color_bg_way = '\033[33m'
    true_false = False
    iconos = {
        'PARED_H': '---', 'PARED_V': '|', 'ESQUINA': '+'
    }
    number = 3

    while True:

        try:
            option = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            return False

        if option == 'q':
            print("\033[93m" + "Exiting...")
            return False
        elif option == '1':
            os.system('clear')
            print('\n\nPressed 1, generating new maze\n')
            from .maze_generator import MazeGenerator
            gen = MazeGenerator(gen.cfg)
            color_grid, color_bg_way = gen.print_maze(
                color_grid, color_bg_way, iconos)
            gen.write_output()
            print_menu(gen)
            true_false = False

        elif option == '2':
            os.system('clear')
            print('\n\nPressed 2, toggling solution path\n')
            if not true_false:
                color_grid, color_bg_way = gen.print_maze_path(
                    color_grid, color_bg_way, iconos)
                true_false = True
            else:
                color_grid, color_bg_way = gen.print_maze(
                    color_grid, color_bg_way, iconos)
                true_false = False
            print_menu(gen)

        elif option == '3':
            os.system('clear')
            print('\n\nPressed 3, changing colors randomly\n')

            color_grid = color_random()
            while color_grid == color_bg_way:
                color_grid = color_random()

            if true_false:
                color_grid, color_bg_way = gen.print_maze_path(
                    color_grid, color_bg_way, iconos)
            else:
                color_grid, color_bg_way = gen.print_maze(
                    color_grid, color_bg_way, iconos)
            print_menu(gen)

        elif option == '4':
            os.system('clear')
            if gen.cfg.center_42:
                print('\n\nPressed 4, changing 42 background color\n')

                color_bg_way = color_random()
                while color_bg_way == color_grid:
                    color_bg_way = color_random()

                if true_false:
                    color_grid, color_bg_way = gen.print_maze_path(
                        color_grid, color_bg_way, iconos)
                else:
                    color_grid, color_bg_way = gen.print_maze(
                        color_grid, color_bg_way, iconos)
            else:
                print('\n\nPressed 4, changing map style\n')
                number2 = random.randint(1, 10)
                while number == number2:
                    number2 = random.randint(1, 10)
                number = number2
                iconos = _get_style_chars(number)
                if true_false:
                    color_grid, color_bg_way = gen.print_maze_path(
                        color_grid, color_bg_way, iconos)
                else:
                    color_grid, color_bg_way = gen.print_maze(
                        color_grid, color_bg_way, iconos)
            print_menu(gen)

        elif option == '5' and gen.cfg.center_42:
            os.system('clear')
            print('\n\nPressed 5, changing map style\n')
            number2 = random.randint(1, 10)
            while number == number2:
                number2 = random.randint(1, 10)
            number = number2
            iconos = _get_style_chars(number)
            if true_false:
                color_grid, color_bg_way = gen.print_maze_path(
                    color_grid, color_bg_way, iconos)
            else:
                color_grid, color_bg_way = gen.print_maze(
                    color_grid, color_bg_way, iconos)
            print_menu(gen)

        else:
            if gen.cfg.center_42:
                print("Invalid option. Use 1, 2, 3, 4, 5 or q.")
            else:
                print("Invalid option. Use 1, 2, 3, 4 or q.")

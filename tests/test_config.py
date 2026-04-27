import pytest
import os
from src.config_parser import parse_config, MazeConfig


def crear_config_test(tmp_path, contenido):
    """Función auxiliar para crear archivos de config temporales."""
    p = tmp_path / "config_test.txt"
    p.write_text(contenido)
    return str(p)


def test_config_valido_basico(tmp_path):
    """Verifica que un config perfecto devuelva el objeto MazeConfig correcto."""
    contenido = (
        "WIDTH=20\n"
        "HEIGHT=15\n"
        "ENTRY=0,0\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
    )
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)

    assert isinstance(config, MazeConfig)
    assert config.width == 20
    assert config.center_42 is True
    assert config.perfect is True


def test_error_espacios_clave(tmp_path):
    """Detecta error si hay espacios en la clave (ej: 'WIDTH =20')."""
    path = crear_config_test(tmp_path, "WIDTH =20\n")
    with pytest.raises(SystemExit):
        parse_config(path)


def test_error_tipo_ancho(tmp_path):
    """Detecta error si WIDTH no es un número."""
    contenido = (
        "WIDTH=veinte\n"
        "HEIGHT=15\n"
        "ENTRY=0,0\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
    )
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_entry_fuera_de_rango(tmp_path):
    """Detecta error si ENTRY está fuera de las dimensiones del mapa."""
    contenido = (
        "WIDTH=10\n"
        "HEIGHT=10\n"
        "ENTRY=15,15\n"  # Fuera de rango
        "EXIT=5,5\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
    )
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_entry_igual_a_exit(tmp_path):
    """Detecta error si entrada y salida son la misma casilla."""
    contenido = (
        "WIDTH=10\n"
        "HEIGHT=10\n"
        "ENTRY=5,5\n"
        "EXIT=5,5\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
    )
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_center_42_false_si_pequeno(tmp_path):
    """Verifica que center_42 sea False si el laberinto es muy pequeño."""
    contenido = (
        "WIDTH=5\n"
        "HEIGHT=5\n"
        "ENTRY=0,0\n"
        "EXIT=4,4\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
    )
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.center_42 is False


def test_seed_opcional_entero(tmp_path):
    """Verifica que SEED se acepte si es un entero."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=salida.txt\nPERFECT=True\nSEED=42\n"
    )
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.seed == 42


def test_seed_invalido(tmp_path):
    """Error si SEED no es entero."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=salida.txt\nPERFECT=True\nSEED=abc\n"
    )
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_perfect_case_insensitive(tmp_path):
    """PERFECT debe aceptar 'true', 'True', 'false', etc."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=salida.txt\nPERFECT=true\n"
    )
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_perfect_valor_invalido(tmp_path):
    """Error si PERFECT no es True/False."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=salida.txt\nPERFECT=maybe\n"
    )
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_display_opcional_valido(tmp_path):
    """DISPLAY acepta valores válidos."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=salida.txt\nPERFECT=True\nDISPLAY=ascii\n"
    )
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.display == "ascii"


def test_display_invalido(tmp_path):
    """Error si DISPLAY tiene valor no permitido."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=salida.txt\nPERFECT=True\nDISPLAY=3d\n"
    )
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_falta_width(tmp_path):
    """Error si falta WIDTH."""
    contenido = "HEIGHT=10\nENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_falta_height(tmp_path):
    """Error si falta HEIGHT."""
    contenido = "WIDTH=10\nENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_linea_sin_igual(tmp_path):
    """Error si hay una línea sin '='."""
    contenido = "WIDTH=10\nHEIGHT=10\nMAL_FORMADA\nENTRY=0,0\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_clave_vacia(tmp_path):
    """Error si la clave está vacía (ej: =valor)."""
    contenido = "=10\nWIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_valor_vacio(tmp_path):
    """Error si el valor está vacío (ej: WIDTH=)."""
    contenido = "WIDTH=\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_espacios_en_valor(tmp_path):
    """Error si hay espacios en el valor (ej: WIDTH= 10)."""
    contenido = "WIDTH= 10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_espacios_en_clave(tmp_path):
    """Error si hay espacios en la clave (ej: WIDTH =10)."""
    contenido = "WIDTH =10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_width_negativo(tmp_path):
    """Error si WIDTH es negativo."""
    contenido = "WIDTH=-5\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_height_cero(tmp_path):
    """Error si HEIGHT es cero."""
    contenido = "WIDTH=10\nHEIGHT=0\nENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_entry_formato_invalido(tmp_path):
    """Error si ENTRY no sigue formato x,y."""
    contenido = "WIDTH=10\nHEIGHT=10\nENTRY=0-0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_exit_no_enteros(tmp_path):
    """Error si EXIT contiene letras."""
    contenido = "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=a,b\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_algorithm_valido(tmp_path):
    """ALGORITHM válido."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=s.txt\nPERFECT=True\nALGORITHM=recursive_backtracker\n"
    )
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.algorithm == "recursive_backtracker"


def test_algorithm_invalido(tmp_path):
    """ALGORITHM no válido."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=s.txt\nPERFECT=True\nALGORITHM=dijkstra\n"
    )
    path = crear_config_test(tmp_path, contenido)
    with pytest.raises(SystemExit):
        parse_config(path)


def test_display_none_por_defecto(tmp_path):
    """DISPLAY es None si no se especifica."""
    contenido = "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.display is None


def test_seed_none_por_defecto(tmp_path):
    """SEED es None si no se especifica."""
    contenido = "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=s.txt\nPERFECT=True\n"
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.seed is None


def test_center_42_true_si_grande(tmp_path):
    """center_42 es True si el mapa es suficientemente grande."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=s.txt\nPERFECT=True\n"
    )
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.center_42 is True


def test_perfect_false(tmp_path):
    """PERFECT=False debe devolver False."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=s.txt\nPERFECT=False\n"
    )
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.perfect is False


def test_entry_y_exit_distintos(tmp_path):
    """ENTRY y EXIT distintos deben ser válidos."""
    contenido = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=s.txt\nPERFECT=True\n"
    )
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.entry_x == 0
    assert config.exit_x == 9


def test_comentarios_se_ignoran(tmp_path):
    """Las líneas que empiezan por # deben ignorarse."""
    contenido = (
        "# Este es un comentario\n"
        "WIDTH=10\n"
        "HEIGHT=10\n"
        "# Otro comentario\n"
        "ENTRY=0,0\n"
        "EXIT=9,9\n"
        "OUTPUT_FILE=s.txt\n"
        "PERFECT=True\n"
    )
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.width == 10


def test_lineas_vacias_se_ignoran(tmp_path):
    """Las líneas vacías deben ignorarse."""
    contenido = (
        "\n"
        "WIDTH=10\n"
        "\n"
        "HEIGHT=10\n"
        "\n"
        "ENTRY=0,0\n"
        "EXIT=9,9\n"
        "OUTPUT_FILE=s.txt\n"
        "PERFECT=True\n"
        "\n"
    )
    path = crear_config_test(tmp_path, contenido)
    config = parse_config(path)
    assert config.width == 10

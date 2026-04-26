import sys
import logging
from Map import Map
import pygame

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s | Archivo: %(filename)s | Linea: %(lineno)d | %(levelname)s: %(message)s"
)

def comprobar_claves(parametros: dict):
    keys_validas = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    if not(all(x for x in parametros.keys() if x in keys_validas)):
        raise ValueError("Faltan claves")
    elif len(parametros.keys()) > 6:
        raise ValueError("Solo debes tener 6 parametros de configuracion")


def cargando_parametros(args: list[str]) -> dict:
    if (len(args) == 2):
        archivos = [x for x in args if x.endswith(".txt")]
        if len(archivos) == 0:
            raise ValueError("Es necesario el archivo de configuracion .txt")
        with open(archivos[0], "r") as f:
            parametros = {}
            for linea in f:
                linea.strip()
                try:
                    clave, valor = linea.split("=", 1)
                    parametros[clave.strip()] = valor.strip()
                except ValueError as e:
                    logging.error(e)
            comprobar_claves(parametros)
            return parametros

if __name__ == "__main__":
    logging.info("La aplicacion ha iniciado")
    argumentos = sys.argv

    if (len(argumentos) == 2):
        try:
            parametros = cargando_parametros(argumentos)
            pygame.init()
            mapa = Map(**parametros)
            clock = pygame.time.Clock()
            dimension = 32
            screen = pygame.display.set_mode((mapa.WIDTH*dimension, mapa.HEIGHT*dimension))
            while (True):
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                mapa.render(dimension, screen)
                pygame.display.flip()
                

        except FileNotFoundError as e:
            logging.error(e)
            print(e)
        except PermissionError as e:
            logging.error(e)
            print(e)
        except ValueError as e:
            logging.error(e)
            print(e)
        except Exception as e:
            logging.error(e)
            print(F"ERROR CRITICO: {e}")

    else:
        print("El sistema debe ser ejecutado por: <main> <.txt>")
    
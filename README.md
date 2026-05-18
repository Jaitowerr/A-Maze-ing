*This project has been created as part of the 42 curriculum by jopajuel y aitorres*


# A-Maze-ing 
tu propio generador de laberintos y muestra su resultado!


## Description

**A-Maze-ing** es un generador de laberintos escrito en Python que toma un archivo de configuración, genera el laberinto, lo guarda en un archivo de salida en formato hexadecimal y lo muestra visualmente. Por defecto arranca con interfaz gráfica usando MiniLibX y el algoritmo Recursive Backtracker, aunque ambas cosas son configurables.

El laberinto siempre incluye el patrón **"42"** dibujado con celdas cerradas en el centro (si el tamaño lo permite), y calcula automáticamente el camino más corto entre la entrada y la salida usando **BFS**.

---

## Instructions
> ⚠️ Solo compatible con **macOS** y **Linux**

### Installation & Run

El proyecto usa **Poetry** para gestionar las dependencias. El propio `make run` se encarga de instalar todo automáticamente antes de arrancar:

```bash
make run
```

Esto instala las dependencias, instala la librería MiniLibX desde el `.whl` incluido en el repositorio y lanza el programa. También puedes ejecutarlo directamente:

```bash
python3 a_maze_ing.py config.txt
```

### Other Makefile rules

```bash
make run	        #Instala dependencias y lanza el programa
make install	    #Solo instala dependencias (Poetry + MiniLibX)
make debug	        #Lanza el programa con pdb (debugger de Python)
make clean	        #Elimina __pycache__, .mypy_cache, dist, build
make lint	        #Ejecuta flake8 + mypy con los flags estándar del subject
make lint-strict	#Ejecuta flake8 + mypy --strict (más restrictivo)
```

### Debug mode
Explicación make debud:

Para lanzar el programa con el debugger de Python (`pdb`):

```bash
make debug
```
---

```bash
Comando	Acción
n	        #Next — ejecuta la línea actual y pasa a la siguiente
s	        #Step — entra dentro de una función
c	        #Continue — ejecuta hasta el siguiente breakpoint (o hasta el final)
l	        #List — muestra el código alrededor de donde estás
p variable	#Print — imprime el valor de una variable, ej: p self._estado
b 42	    #Breakpoint — pone un punto de parada en la línea 42
q	        #Quit — sale del debugger
```

## Configuration File

El archivo de configuración (`config.txt`) sigue el formato `KEY=VALUE`, una por línea. Las líneas que empiezan por `#` son comentarios y se ignoran.

### Mandatory keys

| Key | Description | Example |
| :--- | :--- | :--- |
| `WIDTH` | Ancho del laberinto en celdas | `WIDTH=25` |
| `HEIGHT` | Alto del laberinto en celdas | `HEIGHT=15` |
| `ENTRY` | Coordenadas de entrada (x,y) | `ENTRY=1,0` |
| `EXIT` | Coordenadas de salida (x,y) | `EXIT=14,3` |
| `OUTPUT_FILE` | Archivo donde se guarda el laberinto | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` para laberinto perfecto, `False` para permitir ciclos | `PERFECT=True` |

### Optional keys

| Key | Description | Default | Options |
| :--- | :--- | :--- | :--- |
| `ALGORITHM` | Algoritmo de generación | `recursive_backtracker` | `recursive_backtracker`, `kruskal` |
| `SEED` | Semilla para reproducibilidad | `None` (aleatorio) | Cualquier entero |
| `DISPLAY` | Modo de visualización | `mlx` | `mlx`, `ascii` |

Ejemplo de `config.txt`:
```
WIDTH=25
HEIGHT=15
ENTRY=1,0
EXIT=14,3
OUTPUT_FILE=maze.txt
PERFECT=True
#PERFECT=False
#DISPLAY=ascii
SEED=42
#ALGORITHM=kruskal
```

---

## Algorithms

### Recursive Backtracker (por defecto)

Es un algoritmo de búsqueda en profundidad (DFS). Parte de la celda de entrada y va abriendo caminos aleatoriamente, retrocediendo cuando se queda sin vecinos sin visitar. El resultado son laberintos con pasillos largos y sinuosos, muy desafiantes visualmente.

**Por qué lo elegimos**: Es el más intuitivo de implementar, genera laberintos estéticamente interesantes y es fácil de controlar. Además, el backtracking es un concepto fundamental que queríamos trabajar.

### Kruskal (Randomized)

Basado en el algoritmo de Kruskal para Árboles de Recubrimiento Mínimo (MST). Trata todas las paredes del laberinto como aristas de un grafo y las va eliminando aleatoriamente, siempre que conecten dos zonas que aún no estén conectadas. Para esto usa una estructura **DSU (Disjoint Set Union)** que permite saber eficientemente si dos celdas ya pertenecen al mismo componente.

El resultado son laberintos más "fractales", con muchas ramificaciones cortas y un aspecto más caótico que el backtracker.

---

## PERFECT=False: cómo funciona

Cuando `PERFECT=False`, el laberinto deja de tener un único camino entre entrada y salida. Después de generar el laberinto base, el algoritmo selecciona aleatoriamente un subconjunto de paredes interiores horizontales y las rompe, creando conexiones adicionales entre pasillos.

La agresividad está ajustada para romper aproximadamente **1/3 de las paredes candidatas**, lo que crea ciclos sin llegar a generar espacios abiertos de 3×3 (que el subject prohíbe expresamente). Las paredes candidatas son solo las que separan dos celdas ya visitadas, así que nunca se rompe el marco exterior ni las celdas del patrón "42".

---

## La semilla: reproducibilidad

Una de las cosas más interesantes del proyecto es la semilla (`SEED`). El módulo `random` de Python no genera números verdaderamente aleatorios, sino que ejecuta un algoritmo determinista que, partiendo de un estado inicial, produce una secuencia de números que *parecen* aleatorios. Ese estado inicial es la semilla.

Cuando no se especifica semilla, Python usa parámetros del sistema (como el tiempo actual) para inicializarla, por eso cada ejecución da un laberinto distinto. Pero si inyectas una semilla concreta con `random.seed(42)`, el algoritmo siempre parte del mismo estado y produce exactamente la misma secuencia de decisiones, lo que significa **el mismo laberinto, con las mismas paredes, y la misma solución**, sin importar cuántas veces lo ejecutes o en qué máquina.

Esto es especialmente útil para compartir laberintos concretos, para depurar, o para que la Moulinette pueda validar resultados de forma determinista.

---

## Visual Representation

### MLX (por defecto)

Arranca una ventana gráfica con tiles estilo **Mario Bros**. Los controles son:

| Tecla | Acción |
| :--- | :--- |
| `↑ ↓ ← →` / `W A S D` | Mover al jugador |
| `1` | Regenerar laberinto (Recursive Backtracker) |
| `2` | Regenerar laberinto (Kruskal) |
| `Space` | Cambiar skin/colores del laberinto |
| `C` | Mostrar/ocultar la solución |
| `M` | Cambiar a vista ASCII en terminal |
| `ESC` | Salir |

### ASCII (con `DISPLAY=ascii`)

Renderiza el laberinto directamente en la terminal con caracteres de texto. Desde el menú interactivo puedes:

| Opción | Acción |
| :--- | :--- |
| `1` | Generar un nuevo laberinto |
| `2` | Mostrar/ocultar el camino solución - animado |
| `3` | Cambiar color de las paredes (aleatorio) |
| `4` | Cambiar color del fondo del "42" (si existe) y el camino / Cambiar estilo de pared |
| `5` | Cambiar estilo de pared (si el "42" está activo) |
| `q` | Salir |

Hay **10 estilos de pared** disponibles: desde líneas simples (`---`) hasta bloques sólidos (`███`), dobles (`═══`), ondas (`~~~`), asteriscos y más.

---

## Reusability

La lógica de generación está completamente encapsulada en `MazeGenerator` (`src/maze_generator.py`) y es independiente de la visualización. Se puede importar en cualquier proyecto.

### Basic example

```python
from src.maze_generator import MazeGenerator
from src.map import MazeConfig

cfg = MazeConfig(
    width=15,
    height=10,
    entry_x=0, entry_y=0,
    entry_x_y=[0, 0],
    exit_x=14, exit_y=9,
    exit_x_y=[14, 9],
    output_file="maze.txt",
    perfect=True,
    center_42=True,
    seed=42,
    algorithm="recursive_backtracker",
    display="ascii",
    pixel=60,
    rut="img2/mario"
)

gen = MazeGenerator(cfg)

# Acceder a la estructura del laberinto
print(gen.binary_grid)      # list[list[Celda]]
print(gen.hex_grid)  # list[str]
print(gen.camino)            # str con la solución (N, S, E, O)

# Guardar el archivo de salida
gen.write_output()

# Imprimir en terminal
gen.print_maze()
gen.print_maze_path()
```

El paquete redistribuible está disponible en la raíz del repositorio como `mazegen-*.whl` y puede instalarse con:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Para reconstruirlo desde el código fuente:

```bash
pip install build
python -m build
```

#### Poetry
El make utiliza poetry para manejar el a-maze-ing, algunos de los comandos par poetry son:
```bash
poetry init → crea pyproject.toml
poetry lock → poetry.lock basado en lo que tienes en pyproject.toml.
poetry show → ver dependencias
poetry add X → añadir una dependencia
poetry install → instalar todo
poetry check → comprobar configuración
poetry remove nombre_del_paquete → Para desinstalar dependencias
```
---

## Resources & AI Usage

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Randomized Kruskal's algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Kruskal's_algorithm)
- [Recursive backtracker](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker)
- [BFS — Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python typing — mypy docs](https://mypy.readthedocs.io/en/stable/)
- [PEP 257 — Type Hints](https://peps.python.org/pep-0257/#multi-line-docstrings)

### AI Usage Disclosure

Se ha utilizado IA (**Claude / GPT**) como apoyo en las siguientes tareas:

- **Tipado estático**: Resolución de errors complejos de `mypy --strict`, especialmente con tipos opcionales (`Optional`, `Union-attr`) y la estrategia de `assert` para narrowing de tipos.
- **Limpieza de código**: Corrección sistemática de errors `flake8` (E501, E231, E302, E712, W293...) sin tocar la lógica.
- **Debugging**: Identificación de problemas de coherencia en la representación interna de la cuadrícula.
- **Documentación**: Estructura y redacción del README siguiendo los requisitos del subject.

Todo el código generado o modificado con ayuda de IA ha sido revisado, entendido y validado manualmente antes de integrarse en el proyecto.

---

## Team & Project Management

### Roles

- **[jopajuel]**: Parseo, algoritmo recursive backtracking, algoritmo de solución, representación ASCII y archivo de salida.
- **[aitorres]**: Parseo, algoritmo Kruskal, representación MiniLibX(reparación código, diseño y jugueteo), eventos de teclado, Player y GameControl.

### Planning

Inicialmente estimamos que la parte más compleja sería la generación del laberinto. En la práctica, la integración de **MiniLibX con Python** fue lo que más tiempo nos llevó, ya que la librería está pensada para C y su binding en Python tiene algunas particularidades. También subestimamos el tiempo necesario para cumplir con `mypy --strict`, que requirió una revisión profunda de todos los tipos del proyecto.

### What worked well

- La separación clara entre lógica de generación y visualización desde el principio facilitó mucho el trabajo en paralelo.
- El uso de `random.seed()` para reproducibilidad fue sencillo de implementar y muy útil para depurar.
- El sistema de tiles binarios (16 combinaciones de paredes) resultó elegante y fácil de extender con nuevos estilos visuales.


### Tools used

- **Poetry**: Gestión de dependencias y entorno virtual.
- **mypy**: Tipado estático, incluyendo modo `--strict`.
- **flake8**: Estilo de código (PEP 8).
- **MiniLibX (Python binding)**: Renderizado gráfico.
- **IA**: Apoyo en tipado, limpieza de código y documentación. Tal como Claude y GPT
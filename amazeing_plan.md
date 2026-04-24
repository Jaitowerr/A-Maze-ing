# Plan de trabajo — A-Maze-ing

---

## 1. Aclaraciones previas

### ¿Qué es la semilla (seed)?

La semilla es un número que se pasa al generador de números aleatorios de Python
(`random.seed(42)`). Lo que hace es que **con la misma semilla, el laberinto generado
es siempre idéntico**. Sin semilla, cada ejecución produce un laberinto diferente.
Con semilla, puedes reproducir exactamente el mismo laberinto.

La semilla **actúa junto al algoritmo**: no hay mapas pregrabados. Simplemente hace
el azar reproducible. Ejemplo:

```
SEED=42  →  siempre el mismo laberinto
SEED=99  →  siempre otro laberinto diferente (pero reproducible)
```

---

### ASCII vs MLX — ¿cuál es el mandatory?

El subject dice "ASCII **o** MLX" — **ninguno es bonus sobre el otro**.
Son dos opciones equivalentes para el mandatory de visualización.

Lo que SÍ es bonus (capítulo VIII) es:
- Soportar múltiples algoritmos de generación
- Añadir **animación durante la generación**

**Decisión del equipo: MLX (gráfico)**
Esto significa que todo el display es gráfico. No hace falta implementar ASCII.

---

### ¿Qué es MLX / MiniLibX en Python?

MiniLibX es una librería gráfica usada en proyectos de 42 (normalmente en C).
Para Python, la alternativa más limpia y compatible es **pygame** o **tkinter**.

- **pygame**: más potente, mejor para renderizado pixel a pixel, ideal para el laberinto
- **tkinter**: viene con Python, más limitado visualmente

**Recomendación: pygame** — permite dibujar celdas, paredes y colores fácilmente,
y se gestiona bien con Poetry.

---

### ¿Cómo funciona el arranque automático con Poetry?

El flujo completo al ejecutar el programa es:

```
python3 a_maze_ing.py config.txt
        ↓
  Lee y valida config.txt
        ↓
  ¿Hay errores? → imprime error y sale
        ↓
  Todo OK → genera el laberinto
        ↓
  Abre la ventana gráfica (pygame/MLX)
        ↓
  Menú interactivo dentro de la ventana
```

Poetry gestiona que las dependencias estén instaladas (`make install`).
El usuario no necesita hacer nada más que `make run`.

---

## 2. Estructura de archivos

```
a-maze-ing/
│
├── a_maze_ing.py              ← OBLIGATORIO (nombre exacto del subject)
│                                Punto de entrada. Lee args, orquesta todo.
│
├── config.txt                 ← OBLIGATORIO en el repo (configuración por defecto)
├── Makefile                   ← OBLIGATORIO
├── README.md                  ← OBLIGATORIO (con todo lo que pide el subject)
├── .gitignore                 ← excluir __pycache__, .mypy_cache, venv, dist, etc.
├── pyproject.toml             ← Poetry + build del paquete mazegen
│
├── src/                       ← código interno del proyecto
│   ├── __init__.py
│   ├── config_parser.py       ← parsea y valida el config.txt (KEY=VALUE)
│   ├── maze.py                ← clase Maze: estructura de datos (grid de celdas)
│   ├── generator.py           ← clase MazeGenerator: algoritmo de generación
│   ├── solver.py              ← BFS: encuentra el camino más corto (N/E/S/W)
│   ├── writer.py              ← escribe el archivo de salida en formato hexadecimal
│   ├── renderer.py            ← visualización gráfica con pygame (ventana + menú)
│   └── pattern42.py           ← lógica para incrustar el patrón "42" en el laberinto
│
├── mazegen/                   ← módulo reutilizable (para pip install)
│   ├── __init__.py
│   └── generator.py           ← clase MazeGenerator independiente del proyecto
│
├── dist/                      ← generado automáticamente al hacer build
│   ├── mazegen-1.0.0-py3-none-any.whl
│   └── mazegen-1.0.0.tar.gz
│
└── tests/                     ← tests (no se entregan pero el subject los recomienda)
    ├── test_config.py
    ├── test_generator.py
    ├── test_solver.py
    └── test_writer.py
```

---

## 3. Qué hace cada archivo

| Archivo | Responsabilidad |
|---|---|
| `a_maze_ing.py` | Lee `sys.argv`, llama al parser, genera, resuelve, escribe archivo, lanza renderer |
| `src/config_parser.py` | Parsea KEY=VALUE, ignora `#`, valida tipos y rangos, devuelve dataclass `MazeConfig` |
| `src/maze.py` | Clase `Maze`: grid 2D de enteros (cada celda = 4 bits de paredes) |
| `src/generator.py` | Clase `MazeGenerator`: recibe `Maze` y ejecuta el algoritmo elegido con la semilla |
| `src/solver.py` | BFS desde ENTRY hasta EXIT, devuelve string de movimientos `N/E/S/W` |
| `src/writer.py` | Serializa la grid a hex, escribe el archivo de salida con el formato exacto |
| `src/renderer.py` | Ventana pygame: dibuja paredes, entrada, salida, camino; gestiona el menú interactivo |
| `src/pattern42.py` | Define las coordenadas del "42" y cierra esas celdas (`0xF`) antes de generar |
| `mazegen/generator.py` | Copia limpia del generador, sin dependencias del proyecto, lista para pip |
| `pyproject.toml` | Metadata de Poetry + build: nombre `mazegen`, versión, dependencias |

---

## 4. La representación interna de una celda

Esta es la decisión más importante. Hay que acordarla antes de escribir nada.

Cada celda es un **entero de 4 bits** donde cada bit indica si una pared está cerrada:

```
Bit 0 (LSB) = North  (1 = pared cerrada, 0 = abierta)
Bit 1       = East
Bit 2       = South
Bit 3       = West
```

Ejemplos:
```
0xF = 1111 = cerrada por los 4 lados (celdas del patrón "42")
0x0 = 0000 = sin ninguna pared (célula completamente abierta)
0x5 = 0101 = paredes Norte y Sur cerradas
0xA = 1010 = paredes Este y Oeste cerradas
```

La grid es una lista de listas: `grid[fila][columna]` → entero 0-15.

---

## 5. El algoritmo de generación — Recursive Backtracker (DFS)

### ¿Por qué este algoritmo?

- Es el más sencillo de implementar correctamente
- Produce laberintos **perfectos** de forma natural (un único camino entre dos puntos)
- Con una semilla es completamente reproducible
- Genera laberintos con pasillos largos y orgánicos, visualmente atractivos

### Cómo funciona (resumen):

1. Empieza en una celda aleatoria
2. Marca la celda como visitada
3. Escoge un vecino no visitado aleatoriamente
4. Abre la pared entre la celda actual y el vecino
5. Mueve a ese vecino y repite
6. Si no hay vecinos no visitados, retrocede (backtrack) hasta encontrar uno
7. Termina cuando todas las celdas han sido visitadas

El resultado es un **spanning tree** del grafo de celdas → laberinto perfecto.

---

## 6. El patrón "42"

El patrón "42" son celdas completamente cerradas (`0xF`) que forman visualmente
el número "42" cuando se dibuja el laberinto.

### Proceso:
1. Antes de generar, se definen las coordenadas del "42" según el tamaño del laberinto
2. Esas celdas se marcan como `0xF` (4 paredes cerradas)
3. El algoritmo de generación las trata como obstáculos (no las visita)
4. Al renderizar, aparecen como bloques sólidos formando el "42"

### ¿Cuándo omitirlo?
Si el laberinto es demasiado pequeño (el subject no da un tamaño mínimo exacto,
decidid vosotros, por ejemplo menos de 15x15), imprimís un error por consola y
el laberinto se genera sin el patrón.

---

## 7. El módulo reutilizable (mazegen)

El subject exige que la clase `MazeGenerator` esté en un módulo independiente
que se pueda instalar con pip. Debe estar en un único archivo.

### Estructura mínima del paquete:

```
mazegen/
├── __init__.py       ← exporta MazeGenerator
└── generator.py      ← la clase, sin imports del proyecto principal
```

### Instalación:
```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Uso básico (lo que debe documentarse en README.md):
```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
gen.generate()

maze = gen.maze          # grid 2D de enteros
solution = gen.solution  # string con el camino "NNEESSWW..."
```

---

## 8. El archivo de salida (formato exacto)

El archivo debe tener este formato exacto (sin espacios extra, sin líneas de más):

```
9515391539551795151151153
EBABAE812853C1412BA812812
...
(una línea por fila del laberinto, cada carácter = un hex de una celda)

0,0
19,14
SWSESWSESWSSSEESEEENEESESEESSSEEESSSEEENNENEE
```

Desglose:
- Líneas 1..HEIGHT: la grid en hex, sin separadores, una fila por línea
- Línea vacía
- Coordenadas de entrada: `x,y`
- Coordenadas de salida: `x,y`
- Camino más corto: string de `N`, `E`, `S`, `W` sin separadores
- Todas las líneas terminan en `\n`

---

## 9. La ventana gráfica (renderer.py con pygame)

### Elementos visuales obligatorios:
- Paredes del laberinto (dibujadas como líneas o rectángulos)
- Celda de entrada (color distinto, por ejemplo verde/morado)
- Celda de salida (color distinto, por ejemplo rojo/naranja)
- Patrón "42" visible (celdas completamente rellenas)
- Camino solución (toggle: se muestra u oculta)

### Interacciones obligatorias:
- **1** o botón: regenerar laberinto nuevo y mostrarlo
- **2** o botón: mostrar/ocultar el camino más corto
- **3** o botón: cambiar colores de las paredes (ciclar entre paletas)
- **4** o botón: salir

### Interacciones opcionales (bonus):
- Colorear el patrón "42" con un color específico
- Animación del proceso de generación
- Mostrar el camino animado (celda a celda)

---

## 10. El Makefile

```makefile
install:
    poetry install

run:
    poetry run python3 a_maze_ing.py config.txt

debug:
    poetry run python3 -m pdb a_maze_ing.py config.txt

clean:
    find . -type d -name __pycache__ -exec rm -rf {} +
    rm -rf .mypy_cache dist build *.egg-info

lint:
    poetry run flake8 .
    poetry run mypy . --warn-return-any --warn-unused-ignores \
        --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
    poetry run flake8 .
    poetry run mypy . --strict
```

---

## 11. El config.txt por defecto

```ini
# Configuración por defecto del laberinto A-Maze-ing
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
ALGORITHM=recursive_backtracker
DISPLAY=mlx
```

Claves obligatorias (del subject): WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT
Claves opcionales que añadís: SEED, ALGORITHM, DISPLAY

---

## 12. El README.md — estructura obligatoria

El subject especifica exactamente qué debe contener. Secciones mínimas:

1. Primera línea en cursiva: `*This project has been created as part of the 42 curriculum by <login1>, <login2>.*`
2. **Description** — qué hace el proyecto y objetivo general
3. **Instructions** — cómo instalar y ejecutar
4. **Config file format** — tabla con todas las claves y ejemplos
5. **Algorithm** — cuál usasteis y por qué
6. **Reusable module** — qué es mazegen, cómo instalarlo, ejemplo de uso
7. **Team and project management** — roles, planning, qué funcionó, herramientas
8. **Resources** — referencias + cómo usasteis la IA (para qué tareas, qué partes)

---

## 13. División de trabajo entre 2 personas

### Fase 0 — Setup (juntos, medio día)
- Crear el repo, estructura de carpetas, pyproject.toml con Poetry
- Acordar la representación interna de la celda (sección 4 de este doc)
- Escribir juntos `src/maze.py` — es la base de todo

### Fase 1 — Core (en paralelo, 2-3 días)

**Persona A — Generación y solución:**
- `src/generator.py` → algoritmo Recursive Backtracker con seed
- `src/solver.py` → BFS que devuelve el path N/E/S/W
- Verificar que no hay áreas 3×3 abiertas tras la generación

**Persona B — Config, escritura y patrón:**
- `src/config_parser.py` → parsear KEY=VALUE, validar todo
- `src/writer.py` → serializar a hex con el formato exacto del subject
- `src/pattern42.py` → definir coordenadas del "42" y aplicarlas

### Fase 2 — Integración (juntos, 1 día)
- Conectar todo en `a_maze_ing.py`
- Verificar que el archivo de salida es válido con el validador del subject
- Probar casos de error (config inválida, coordenadas fuera de rango, etc.)

### Fase 3 — Visualización (Persona A o juntos, 2 días)
- `src/renderer.py` → ventana pygame con todos los elementos obligatorios
- Menú interactivo funcional
- Colores configurables

### Fase 4 — Paquete y documentación (Persona B, 1 día)
- `mazegen/` → módulo limpio sin dependencias del proyecto
- `pyproject.toml` → build del paquete (.whl y .tar.gz)
- `README.md` → completo con todo lo que exige el subject

### Fase 5 — Calidad (juntos, 1 día)
- Pasar `flake8` sin errores
- Pasar `mypy` con los flags del Makefile
- Type hints y docstrings en todas las funciones
- Tests básicos en `tests/`

---

## 14. Requisitos que más se suelen olvidar

Estos son los puntos críticos donde los proyectos fallan en la evaluación:

- **Coherencia de paredes**: si celda A tiene pared al Este, celda B (a su derecha)
  DEBE tener pared al Oeste. El validador del subject lo detecta.

- **Sin áreas 3×3 abiertas**: después de generar, hay que verificar que no existe
  ningún bloque de 3×3 celdas todas abiertas entre sí. El Recursive Backtracker
  no garantiza esto solo, hay que verificarlo y corregirlo si ocurre.

- **Paredes en los bordes externos**: todas las celdas del borde del laberinto
  deben tener pared exterior cerrada, excepto en las celdas de entrada y salida.

- **Formato exacto del archivo de salida**: línea vacía antes de las coordenadas,
  `\n` al final de cada línea, coordenadas en formato `x,y` sin espacios.

- **El paquete mazegen debe instalarse en un virtualenv limpio**: durante la
  evaluación os pedirán que lo hagáis desde cero. Probadlo antes.

- **El patrón "42" debe ser visible**: celdas completamente cerradas (valor `F`),
  con suficiente tamaño para reconocerse en el renderizado.

- **Manejo de errores**: el programa NUNCA debe crashear. Todo error debe
  mostrar un mensaje claro y salir limpiamente.

---

## 15. Dependencias del proyecto (pyproject.toml)

```toml
[tool.poetry]
name = "a-maze-ing"
version = "1.0.0"
description = "Maze generator - 42 project"
authors = ["login1", "login2"]

[tool.poetry.dependencies]
python = "^3.10"
pygame = "^2.5.0"

[tool.poetry.dev-dependencies]
flake8 = "^7.0.0"
mypy = "^1.8.0"
pytest = "^8.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Para el paquete mazegen por separado, usar un `pyproject.toml` adicional
dentro de la carpeta `mazegen/` o configurar el build con `hatchling`/`flit`.

---

## 16. Orden de implementación recomendado (checklist)

### Semana 1
- [ ] Setup del repo y Poetry
- [ ] `src/maze.py` — clase Maze con la grid
- [ ] `src/config_parser.py` — parseo y validación
- [ ] `src/generator.py` — Recursive Backtracker básico (sin "42" aún)
- [ ] `src/solver.py` — BFS
- [ ] `src/writer.py` — escritura del archivo hex

### Semana 2
- [ ] `src/pattern42.py` — patrón "42"
- [ ] Integrar todo en `a_maze_ing.py`
- [ ] Verificar con el validador del subject
- [ ] `src/renderer.py` — ventana pygame básica (paredes + entrada + salida)
- [ ] Menú interactivo completo en el renderer

### Semana 3
- [ ] `mazegen/` — módulo reutilizable limpio
- [ ] Build del paquete (.whl)
- [ ] `README.md` completo
- [ ] Flake8 y mypy sin errores
- [ ] Tests básicos
- [ ] Prueba de instalación del paquete en virtualenv limpio
- [ ] Revisión final con el validador
```

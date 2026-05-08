import random


def run(gen):
    cfg = gen.cfg
    grid = gen.grid

    sy, sx = cfg.entry_y, cfg.entry_x
    ey, ex = cfg.exit_y, cfg.exit_x

    H = len(grid)
    W = len(grid[0])
    moves = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    stack = [(sy, sx)]
    visited = {(sy, sx)}

    while stack:
        y, x = stack[-1]
        dirs = moves[:]
        random.shuffle(dirs)
        moved = False

        for dy, dx in dirs:
            ny, nx = y + dy, x + dx
            py, px = y + dy // 2, x + dx // 2

            if not (0 <= ny < H and 0 <= nx < W):
                continue
            if grid[py][px] == 2 or grid[ny][nx] == 2:
                continue
            if (ny, nx) in visited:
                continue
            if grid[ny][nx] not in (1, 0, 5):
                continue

            if grid[py][px] == 3:
                grid[py][px] = 0

            if grid[ny][nx] == 1:
                grid[ny][nx] = 0

            visited.add((ny, nx))
            stack.append((ny, nx))
            moved = True
            break

        if not moved:
            stack.pop()


    if not cfg.perfect:
        paredes = []
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                # Una pared es un 3 que NO fue abierto por el algoritmo
                if grid[y][x] != 3:
                    continue

                # pared vertical (separa izquierda/derecha)
                if y % 2 == 1 and x % 2 == 0:
                    c1, c2 = (y, x - 1), (y, x + 1)
                # pared horizontal (separa arriba/abajo)
                elif y % 2 == 0 and x % 2 == 1:
                    c1, c2 = (y - 1, x), (y + 1, x)
                else:
                    continue

                # Solo si ambas celdas vecinas son parte del laberinto
                if c1 in visited and c2 in visited:
                    paredes.append((y, x))

        n_romper = max(1, len(paredes) // 3)
        for y, x in random.sample(paredes, min(n_romper, len(paredes))):
            grid[y][x] = 0


# def run(gen):

#     cfg = gen.cfg
#     template = cfg.grid
#     sy, sx = cfg.entry_y, cfg.entry_x
#     ey, ex = cfg.exit_y, cfg.exit_x

#     H = len(template)
#     W = len(template[0])
#     moves = [(0, 2), (0, -2), (2, 0), (-2, 0)]

#     attempt = 0
#     while True:
#         # --- semilla/seed handling ---
#         # Primer intento no reseedea: asumimos gen.algoritmo() ya hizo random.seed(cfg.seed)
#         if attempt > 0:
#             if getattr(cfg, "seed", None) is not None:
#                 cfg.seed = cfg.seed + 1  # incrementa la semilla para determinismo
#                 random.seed(cfg.seed)
#             else:
#                 random.seed(None)  # aleatorio distinto por intento

#         # --- restaurar grid desde plantilla y asegurar 4/5 en sus posiciones ---
#         gen.grid = [row.copy() for row in template]
#         grid = gen.grid
#         grid[sy][sx] = 4
#         grid[ey][ex] = 5

#         # --- normalizar placeholders simples (strings -> int; placeholders -> 2) ---
#         for y in range(H):
#             for x in range(W):
#                 v = grid[y][x]
#                 if not isinstance(v, int):
#                     try:
#                         grid[y][x] = int(str(v).strip())
#                     except Exception:
#                         grid[y][x] = 2

#         # --- DFS iterativo que talla mientras busca la salida ---
#         stack = [(sy, sx)]
#         parent = {(sy, sx): None}
#         visited = {(sy, sx)}
#         found = False

#         while stack:
#             y, x = stack[-1]
#             if (y, x) == (ey, ex):
#                 found = True
#                 break

#             dirs = moves[:]
#             random.shuffle(dirs)
#             moved = False

#             for dy, dx in dirs:
#                 ny, nx = y + dy, x + dx
#                 py, px = y + dy // 2, x + dx // 2  # pared intermedia
#                 if not (0 <= ny < H and 0 <= nx < W):
#                     continue
#                 # nunca tocar impenetrable
#                 if grid[py][px] == 2 or grid[ny][nx] == 2:
#                     continue
#                 if (ny, nx) in visited:
#                     continue

#                 # si destino es la salida: romper pared intermedia si 3 y avanzar
#                 if (ny, nx) == (ey, ex):
#                     if grid[py][px] == 3:
#                         grid[py][px] = 0
#                     parent[(ny, nx)] = (y, x)
#                     stack.append((ny, nx))
#                     moved = True
#                     break

#                 # avanzar solo si destino es 1 o 0 y no es 4/5
#                 if grid[ny][nx] not in (1, 0):
#                     continue
#                 if grid[ny][nx] in (4, 5):
#                     continue

#                 # romper pared intermedia si es 3
#                 if grid[py][px] == 3:
#                     grid[py][px] = 0
#                 # abrir destino si era 1 (no tocar 4/5)
#                 if grid[ny][nx] == 1:
#                     grid[ny][nx] = 0

#                 visited.add((ny, nx))
#                 parent[(ny, nx)] = (y, x)
#                 stack.append((ny, nx))
#                 moved = True
#                 break

#             if not moved:
#                 stack.pop()

#         # --- si encontramos la salida, reconstruimos la ruta y salimos ---
#         if found and (ey, ex) in parent:
#             cur = (ey, ex)
#             while cur is not None:
#                 cy, cx = cur
#                 if grid[cy][cx] not in (4, 5):
#                     grid[cy][cx] = 0
#                 cur = parent[cur]
#             # dejar cfg.seed con la semilla que funcionó (si existe)
#             # (si attempt == 0 y gen.algoritmo() había fijado la semilla, no la cambiamos)
#             # si intentos > 0 y cfg.seed existe, ya lo hemos incrementado arriba
#             return  # terminado: gen.grid contiene el mapa generado

#         # no encontrado -> incrementar contador e intentar de nuevo
#         attempt += 1
#         # el loop repite hasta encontrar la salida (o nunca si el mapa es realmente imposible)
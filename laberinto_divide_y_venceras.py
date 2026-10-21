import time
from collections import deque

LIBRE = "⬜"
PARED = "⬛"
CAMINO = "🟩"

DIRECCIONES = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Si la región tiene esta cantidad de casillas o menos, se resuelve directo
UMBRAL = 16

# Estadísticas del último análisis (para mostrar en pantalla)
stats = {"visitadas": 0, "respaldos": 0}


def imprimir_laberinto(tablero):
    for fila in tablero:
        print("".join(fila))
    print()


def copiar(tablero):
    return [fila[:] for fila in tablero]


# ---------------------------------------------------------------------------
# Región = (f0, f1, c0, c1), con f1 y c1 EXCLUSIVOS: filas f0..f1-1, cols c0..c1-1
# ---------------------------------------------------------------------------

def en_region(region, x, y):
    f0, f1, c0, c1 = region
    return f0 <= x < f1 and c0 <= y < c1


def es_libre(tablero, region, x, y):
    return en_region(region, x, y) and tablero[x][y] == LIBRE


def area(region):
    f0, f1, c0, c1 = region
    return (f1 - f0) * (c1 - c0)


# ---------------------------------------------------------------------------
# CASO BASE: resolver directamente una región pequeña (BFS dentro de la región)
# ---------------------------------------------------------------------------

def resolver_directo(tablero, region, inicio, fin):
    if not es_libre(tablero, region, *inicio) or not es_libre(tablero, region, *fin):
        return None

    padres = {inicio: None}
    cola = deque([inicio])

    while cola:
        actual = cola.popleft()
        stats["visitadas"] += 1

        if actual == fin:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padres[actual]
            return camino[::-1]

        x, y = actual
        for dx, dy in DIRECCIONES:
            vecino = (x + dx, y + dy)
            if vecino not in padres and es_libre(tablero, region, *vecino):
                padres[vecino] = actual
                cola.append(vecino)

    return None


# ---------------------------------------------------------------------------
# DIVIDIR: partir la región en dos mitades por su lado más largo
# ---------------------------------------------------------------------------

def dividir(region):
    f0, f1, c0, c1 = region
    if (f1 - f0) >= (c1 - c0):
        medio = (f0 + f1) // 2
        return (f0, medio, c0, c1), (medio, f1, c0, c1), "fila", medio
    medio = (c0 + c1) // 2
    return (f0, f1, c0, medio), (f0, f1, medio, c1), "columna", medio


def pares_frontera(tablero, mitad_a, mitad_b, eje, medio, region):
    """
    Casillas libres a ambos lados de la línea de corte: (p en A, q en B),
    con p y q vecinas. Son los únicos puntos por donde se puede pasar de A a B.
    """
    f0, f1, c0, c1 = region
    pares = []
    if eje == "fila":
        for y in range(c0, c1):
            if tablero[medio - 1][y] == LIBRE and tablero[medio][y] == LIBRE:
                pares.append(((medio - 1, y), (medio, y)))
    else:
        for x in range(f0, f1):
            if tablero[x][medio - 1] == LIBRE and tablero[x][medio] == LIBRE:
                pares.append(((x, medio - 1), (x, medio)))
    return pares


# ---------------------------------------------------------------------------
# VENCER: resolver cada mitad y COMBINAR los caminos por la frontera
# ---------------------------------------------------------------------------

def resolver(tablero, region, inicio, fin):
    if inicio == fin:
        return [inicio] if es_libre(tablero, region, *inicio) else None

    if area(region) <= UMBRAL:
        return resolver_directo(tablero, region, inicio, fin)

    mitad_a, mitad_b, eje, medio = dividir(region)
    en_a_inicio = en_region(mitad_a, *inicio)
    en_a_fin = en_region(mitad_a, *fin)

    if en_a_inicio != en_a_fin:
        # Inicio y fin en mitades distintas: el camino cruza por la frontera
        if not en_a_inicio:
            # Para no duplicar lógica, resolvemos en sentido contrario e invertimos
            camino = resolver(tablero, region, fin, inicio)
            return camino[::-1] if camino else None

        for p, q in pares_frontera(tablero, mitad_a, mitad_b, eje, medio, region):
            izquierda = resolver(tablero, mitad_a, inicio, p)
            if izquierda is None:
                continue
            derecha = resolver(tablero, mitad_b, q, fin)
            if derecha is None:
                continue
            return izquierda + derecha  # COMBINAR
    else:
        # Ambos en la misma mitad: se intenta resolver solo en esa mitad
        mitad = mitad_a if en_a_inicio else mitad_b
        camino = resolver(tablero, mitad, inicio, fin)
        if camino is not None:
            return camino

    # Respaldo: el camino necesita cruzar la línea de corte más de una vez,
    # así que se resuelve directamente sobre toda la región.
    stats["respaldos"] += 1
    return resolver_directo(tablero, region, inicio, fin)


def resolver_laberinto(tablero, inicio, fin):
    region = (0, len(tablero), 0, len(tablero[0]))
    return resolver(tablero, region, inicio, fin)


def camino_valido(tablero, camino, inicio, fin):
    if not camino or camino[0] != inicio or camino[-1] != fin:
        return False
    if len(set(camino)) != len(camino):
        return False
    for (x, y) in camino:
        if tablero[x][y] != LIBRE:
            return False
    for (x1, y1), (x2, y2) in zip(camino, camino[1:]):
        if abs(x1 - x2) + abs(y1 - y2) != 1:
            return False
    return True


# ---------------------------------------------------------------------------
# Datos de prueba
# ---------------------------------------------------------------------------

def crear_laberinto_trampa(k):
    """
    Laberinto con una zona abierta k x k sin salida a la que se entra primero
    desde el inicio (muy costosa para backtracking puro) y un pasillo
    que lleva a la meta por la parte superior y la última columna.
    """
    filas = k + 2
    cols = k + 4
    t = [[PARED] * cols for _ in range(filas)]

    for c in range(cols):
        t[0][c] = LIBRE
    for f in range(filas):
        t[f][cols - 1] = LIBRE

    t[1][0] = LIBRE
    for f in range(2, 2 + k):
        for c in range(k):
            t[f][c] = LIBRE

    return t


pequeno = [
    [LIBRE, LIBRE, LIBRE, LIBRE, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, LIBRE],
]

mediano = crear_laberinto_trampa(5)
grande = crear_laberinto_trampa(6)

rect_ancho = [
    [LIBRE, PARED, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, PARED, LIBRE, LIBRE, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, PARED, PARED, PARED, PARED, PARED, PARED, LIBRE, PARED, LIBRE, PARED, LIBRE],
    [LIBRE, LIBRE, LIBRE, PARED, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, PARED, LIBRE],
]

rect_alto = [
    [LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE],
    [LIBRE, LIBRE, LIBRE],
    [PARED, PARED, LIBRE],
    [LIBRE, LIBRE, LIBRE],
    [LIBRE, PARED, PARED],
    [LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE],
    [LIBRE, LIBRE, LIBRE],
]

rect_extra_ancho = [
    [LIBRE, PARED, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, PARED, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, PARED, LIBRE, LIBRE, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, PARED, PARED, PARED, PARED, PARED, PARED, PARED, PARED, LIBRE, PARED, LIBRE, PARED, LIBRE, PARED, PARED, PARED, LIBRE],
    [LIBRE, PARED, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, PARED, LIBRE, PARED, LIBRE, LIBRE, LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, PARED, PARED, PARED, PARED, PARED, PARED, PARED, PARED, PARED, PARED, LIBRE, PARED, PARED, PARED, LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, PARED, LIBRE, LIBRE, LIBRE, PARED, LIBRE, LIBRE, LIBRE, PARED, LIBRE],
    [LIBRE, PARED, PARED, PARED, LIBRE, PARED, PARED, PARED, PARED, PARED, LIBRE, PARED, LIBRE, PARED, PARED, PARED, LIBRE, PARED, PARED, PARED, LIBRE],
    [LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, PARED, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, PARED, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE, LIBRE],
]

pruebas = [
    ("Pequeño (5x5)", pequeno),
    (f"Mediano ({len(mediano)}x{len(mediano[0])}, trampa 5x5)", mediano),
    (f"Grande ({len(grande)}x{len(grande[0])}, trampa 6x6)", grande),
    ("Rectangular ancho (3x15)", rect_ancho),
    ("Rectangular alto (15x3)", rect_alto),
    ("Rectangular extra ancho (7x21)", rect_extra_ancho),
]


def main():
    for nombre, laberinto in pruebas:
        print("Probando:", nombre)
        inicio = (0, 0)
        fin = (len(laberinto) - 1, len(laberinto[0]) - 1)
        stats["visitadas"] = 0
        stats["respaldos"] = 0

        t0 = time.perf_counter()
        camino = resolver_laberinto(laberinto, inicio, fin)
        tiempo = time.perf_counter() - t0

        resuelto = camino is not None
        print("Resuelto:", resuelto)
        print(f"Tiempo: {tiempo:.6f} segundos")
        print("Pasos del camino final:", len(camino) if resuelto else 0)
        print("Casillas visitadas:", f"{stats['visitadas']:,}")
        print("Veces que se usó el respaldo:", stats["respaldos"])

        if resuelto:
            assert camino_valido(laberinto, camino, inicio, fin)
            tablero = copiar(laberinto)
            for x, y in camino:
                tablero[x][y] = CAMINO
            print("Laberinto resuelto:")
            imprimir_laberinto(tablero)


if __name__ == "__main__":
    main()

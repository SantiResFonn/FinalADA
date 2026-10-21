import time

LIBRE = "⬜"
PARED = "⬛"
CAMINO = "🟩"

# Orden de exploración: abajo, derecha, arriba, izquierda
DIRECCIONES = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def imprimir_laberinto(tablero):
    for fila in tablero:
        print("".join(fila))
    print()


def es_valida(tablero, x, y):
    """La casilla está dentro del tablero y es transitable."""
    return (
        0 <= x < len(tablero)
        and 0 <= y < len(tablero[0])
        and tablero[x][y] == LIBRE
    )


def resolver_laberinto(tablero, x, y, destino, camino, contador):
    """
    Backtracking: elige una casilla, la marca, intenta avanzar en cada
    dirección y, si ninguna funciona, deshace la decisión (retrocede).
    contador[0] acumula la cantidad de casillas visitadas.
    """
    if not es_valida(tablero, x, y):
        return False

    # Elegir
    tablero[x][y] = CAMINO
    camino.append((x, y))
    contador[0] += 1

    # Caso base: llegamos a la meta
    if (x, y) == destino:
        return True

    # Explorar
    for dx, dy in DIRECCIONES:
        if resolver_laberinto(tablero, x + dx, y + dy, destino, camino, contador):
            return True

    # Deshacer (backtrack)
    tablero[x][y] = LIBRE
    camino.pop()
    return False


def crear_laberinto_trampa(k):
    """
    Genera un laberinto que obliga al backtracking a trabajar mucho.

    Desde el inicio (0,0) la primera dirección probada es 'abajo', que entra
    a una zona abierta de k x k sin salida. Como el algoritmo desmarca las
    casillas al retroceder, debe recorrer TODOS los caminos posibles dentro
    de esa zona (crecimiento explosivo) antes de probar 'derecha', que es
    el pasillo que realmente lleva a la meta.
    """
    filas = k + 2
    cols = k + 4
    t = [[PARED] * cols for _ in range(filas)]

    # Pasillo superior y bajada por la última columna hasta la meta
    for c in range(cols):
        t[0][c] = LIBRE
    for f in range(filas):
        t[f][cols - 1] = LIBRE

    # Entrada a la trampa y zona abierta k x k
    t[1][0] = LIBRE
    for f in range(2, 2 + k):
        for c in range(k):
            t[f][c] = LIBRE

    return t


def copiar(tablero):
    return [fila[:] for fila in tablero]


pequeno = [
    [LIBRE, LIBRE, LIBRE, LIBRE, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, LIBRE],
    [LIBRE, PARED, LIBRE, PARED, LIBRE],
]

# Zonas abiertas de 5x5 (mediano) y 6x6 (grande): la cantidad de caminos
# posibles crece de forma explosiva con k. Sube k para tardar aún más.
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


def meta(tablero):
    """Esquina inferior derecha."""
    return (len(tablero) - 1, len(tablero[0]) - 1)


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
        tablero = copiar(laberinto)
        camino = []
        contador = [0]

        inicio = time.perf_counter()
        resuelto = resolver_laberinto(tablero, 0, 0, meta(tablero), camino, contador)
        tiempo = time.perf_counter() - inicio

        print("Resuelto:", resuelto)
        print(f"Tiempo: {tiempo:.6f} segundos")
        print("Pasos del camino final:", len(camino))
        print("Casillas visitadas (incluye retrocesos):", f"{contador[0]:,}")
        print("Laberinto resuelto:")
        imprimir_laberinto(tablero)


if __name__ == "__main__":
    main()

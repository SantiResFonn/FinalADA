import sys
import threading
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


def crear_laberinto_trampa(k, filas=None, cols=None):
    """
    Genera un laberinto que obliga al backtracking a trabajar mucho.

    Desde el inicio (0,0) la primera dirección probada es 'abajo', que entra
    a una zona abierta de k x k sin salida. Como el algoritmo desmarca las
    casillas al retroceder, debe recorrer TODOS los caminos posibles dentro
    de esa zona (crecimiento explosivo) antes de probar 'derecha', que es
    el pasillo que realmente lleva a la meta.

    k      -> tamaño de la zona trampa (controla el TIEMPO, es exponencial)
    filas  -> alto total del tablero (mínimo k + 2)
    cols   -> ancho total del tablero (mínimo k + 4)
    El resto del tablero son paredes: solo agrandan las dimensiones y
    alargan el pasillo (borde superior + última columna) hasta la meta.
    """
    filas = max(filas or 0, k + 2)
    cols = max(cols or 0, k + 4)
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

# Tableros sobredimensionados. El TIEMPO lo controla k (zona trampa, crecimiento
# explosivo); las dimensiones del tablero alargan el pasillo y la recursión.
mediano = crear_laberinto_trampa(5, 1000, 1000)    # 1.000 x 1.000 =   1.000.000 casillas
grande = crear_laberinto_trampa(6, 3000, 3000)     # 3.000 x 3.000 =   9.000.000 casillas

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


# Caso extremo OPCIONAL: trampa 7x7 con tablero de 5.000 x 5.000.
# Con k=7 el backtracking tarda HORAS (cientos de millones de casillas
# visitadas); por eso está desactivado por defecto.
INCLUIR_EXTREMO = False

pruebas = [
    ("Pequeño (5x5)", pequeno),
    (f"Mediano ({len(mediano)}x{len(mediano[0])}, trampa 5x5)", mediano),
    (f"Grande ({len(grande)}x{len(grande[0])}, trampa 6x6)", grande),
    ("Rectangular ancho (3x15)", rect_ancho),
    ("Rectangular alto (15x3)", rect_alto),
    ("Rectangular extra ancho (7x21)", rect_extra_ancho),
]

if INCLUIR_EXTREMO:
    pruebas.append(("EXTREMO (5000x5000, trampa 7x7)", crear_laberinto_trampa(7, 5000, 5000)))


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
        if len(tablero) * len(tablero[0]) <= 400:
            print("Laberinto resuelto:")
            imprimir_laberinto(tablero)
        else:
            print("(tablero demasiado grande para imprimirlo en consola)\n")


if __name__ == "__main__":
    # Los tableros enormes generan recursión muy profunda (miles de niveles):
    # se sube el límite y se ejecuta en un hilo con pila grande.
    sys.setrecursionlimit(10_000_000)
    threading.stack_size(512 * 1024 * 1024)
    hilo = threading.Thread(target=main)
    hilo.start()
    hilo.join()

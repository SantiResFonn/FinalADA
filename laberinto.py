import sys
import threading
import time

# Contador de casillas visitadas (incluye las que luego se deshacen)
visitadas = 0


def imprimir_laberinto(tablero):
    for fila in tablero:
        for casilla in fila:
            print(casilla, end="")
        print()
    print()


def resolver_laberinto(tablero, x, y, x_fin, y_fin, camino):
    global visitadas

    if x == x_fin and y == y_fin:
        visitadas += 1
        tablero[x][y] = "🟩"
        camino.append((x, y))
        return True

    if x < 0 or x >= len(tablero) or y < 0 or y >= len(tablero[0]):
        return False

    if tablero[x][y] != "⬜":
        return False

    visitadas += 1
    tablero[x][y] = "🟩"
    camino.append((x, y))

    if resolver_laberinto(tablero, x + 1, y, x_fin, y_fin, camino):
        return True
    if resolver_laberinto(tablero, x, y + 1, x_fin, y_fin, camino):
        return True
    if resolver_laberinto(tablero, x - 1, y, x_fin, y_fin, camino):
        return True
    if resolver_laberinto(tablero, x, y - 1, x_fin, y_fin, camino):
        return True

    tablero[x][y] = "⬜"
    camino.pop()
    return False


def crear_laberinto_trampa(k, filas=None, cols=None):
    """
    Laberinto 'trampa' (el mismo de las otras versiones).

    Desde el inicio (0,0) la primera dirección probada es 'abajo', que entra
    a una zona abierta de k x k sin salida. Como la fuerza bruta desmarca las
    casillas al retroceder, debe recorrer TODOS los caminos posibles dentro
    de esa zona antes de probar 'derecha', que es el pasillo real a la meta.

    k      -> tamaño de la zona trampa (controla el TIEMPO, es exponencial)
    filas  -> alto total del tablero (mínimo k + 2)
    cols   -> ancho total del tablero (mínimo k + 4)
    """
    filas = max(filas or 0, k + 2)
    cols = max(cols or 0, k + 4)
    t = [["⬛"] * cols for _ in range(filas)]

    # Pasillo superior y bajada por la última columna hasta la meta
    for c in range(cols):
        t[0][c] = "⬜"
    for f in range(filas):
        t[f][cols - 1] = "⬜"

    # Entrada a la trampa y zona abierta k x k
    t[1][0] = "⬜"
    for f in range(2, 2 + k):
        for c in range(k):
            t[f][c] = "⬜"

    return t


pequeno = [
    ["⬜", "⬜", "⬜", "⬜", "⬜"],
    ["⬜", "⬛", "⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜", "⬛", "⬜"]
]

# Tableros sobredimensionados (mismos que backtracking y divide y vencerás)
mediano = crear_laberinto_trampa(5, 1000, 1000)    # 1.000 x 1.000 = 1.000.000 casillas
grande = crear_laberinto_trampa(6, 3000, 3000)     # 3.000 x 3.000 = 9.000.000 casillas

rect_ancho = [
    ["⬜", "⬛", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜"],
    ["⬜", "⬛", "⬜", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬜", "⬛", "⬜", "⬛", "⬜"],
    ["⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬛", "⬜"]
]

rect_alto = [
    ["⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜"],
    ["⬜", "⬜", "⬜"],
    ["⬛", "⬛", "⬜"],
    ["⬜", "⬜", "⬜"],
    ["⬜", "⬛", "⬛"],
    ["⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜"],
    ["⬜", "⬜", "⬜"]
]

rect_extra_ancho = [
    ["⬜", "⬛", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜"],
    ["⬜", "⬛", "⬜", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬜", "⬛", "⬜", "⬛", "⬜", "⬛", "⬛", "⬛", "⬜"],
    ["⬜", "⬛", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬛", "⬜", "⬛", "⬜", "⬜", "⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬜", "⬛", "⬛", "⬛", "⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬜", "⬛", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬛", "⬜"],
    ["⬜", "⬛", "⬛", "⬛", "⬜", "⬛", "⬛", "⬛", "⬛", "⬛", "⬜", "⬛", "⬜", "⬛", "⬛", "⬛", "⬜", "⬛", "⬛", "⬛", "⬜"],
    ["⬜", "⬜", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"]
]

# Caso extremo OPCIONAL: trampa 7x7 con tablero de 5.000 x 5.000.
# Con k=7 la fuerza bruta tarda HORAS; por eso está desactivado.
INCLUIR_EXTREMO = False

pruebas = [
    ("Pequeno (5x5)", pequeno, 0, 0, 4, 4),
    ("Mediano (1000x1000, trampa 5x5)", mediano, 0, 0, 999, 999),
    ("Grande (3000x3000, trampa 6x6)", grande, 0, 0, 2999, 2999),
    ("Rectangular ancho (3x15)", rect_ancho, 0, 0, 2, 14),
    ("Rectangular alto (15x3)", rect_alto, 0, 0, 14, 2),
    ("Rectangular extra ancho (7x21)", rect_extra_ancho, 0, 0, 6, 20)
]

if INCLUIR_EXTREMO:
    pruebas.append(("EXTREMO (5000x5000, trampa 7x7)",
                    crear_laberinto_trampa(7, 5000, 5000), 0, 0, 4999, 4999))


def main():
    global visitadas

    for nombre, laberinto, x1, y1, x2, y2 in pruebas:
        print("Probando:", nombre)
        camino = []
        copia = [fila[:] for fila in laberinto]
        visitadas = 0

        t_inicio = time.time()
        resuelto = resolver_laberinto(copia, x1, y1, x2, y2, camino)
        t_fin = time.time()

        tiempo = t_fin - t_inicio
        print("Resuelto:", resuelto)
        print("Tiempo:", f"{tiempo:.6f}", "segundos")
        print("Pasos:", len(camino))
        print("Casillas visitadas (incluye retrocesos):", f"{visitadas:,}")

        if len(copia) * len(copia[0]) <= 400:
            print("Laberinto resuelto:")
            imprimir_laberinto(copia)
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
    print("Pasos:", len(camino))
    print("Laberinto resuelto:")
    imprimir_laberinto(copia)

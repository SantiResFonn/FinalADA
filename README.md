# Resolución de Laberintos — Fuerza Bruta vs. Backtracking vs. Divide y Vencerás

**Curso:** Análisis y Diseño de Algoritmos — 2026-2  
**Integrantes:** Alejandro Bermudez, Juan David Mosquera, Santiago Restrepo  
**Entrega:** Entrega 1 — Análisis de Complejidad y Recursividad  
**Caso de uso elegido:** 3.3 Juego o Puzzle (Laberinto)  

**Archivos:**
- [`laberinto_fuerza_bruta.py`](laberinto_fuerza_bruta.py): solución por fuerza bruta (búsqueda exhaustiva recursiva, código original).
- [`laberinto_backtracking.py`](laberinto_backtracking.py): solución por backtracking (búsqueda exhaustiva recursiva).
- [`laberinto_divide_y_venceras.py`](laberinto_divide_y_venceras.py): solución por divide y vencerás.

---

## 1. Definición del Problema

El problema consiste en encontrar un camino transitable desde una casilla de inicio hasta una casilla de destino (salida) dentro de una matriz bidimensional que modela un laberinto con obstáculos.

### 1.1 Entradas
- **Tablero:** Matriz bidimensional de tamaño $N \times M$ representada directamente con emojis:
  - `⬜` (Casilla libre): Espacio transitable.
  - `⬛` (Pared): Obstáculo intransitable.
- **Punto de inicio:** Coordenadas `(x_inicio, y_inicio)`. Por convención, se inicia en `(0, 0)`.
- **Punto de destino:** Coordenadas `(x_fin, y_fin)`. Por convención, la esquina opuesta `(N-1, M-1)`.

### 1.2 Salidas
- **Confirmación:** Booleano (`True` si se encontró solución, `False` en caso contrario).
- **Tablero resuelto:** La misma matriz donde el camino recorrido se reemplaza con `🟩`. Solo se imprime en consola si el tablero tiene 400 casillas o menos; los tableros grandes se omiten.
- **Métricas:** Tiempo de ejecución en segundos, cantidad de pasos del camino final y cantidad de casillas visitadas (incluyendo retrocesos).

### 1.3 Restricciones
- No salirse de los límites de la matriz ($0 \le x < N$ y $0 \le y < M$).
- No pisar obstáculos (`⬛`).
- No repetir casillas dentro del camino actual para evitar ciclos infinitos.

---

## 2. Solución por Fuerza Bruta (Recursividad)

Implementada en [`laberinto_fuerza_bruta.py`](laberinto_fuerza_bruta.py) (es el código original del proyecto, con tableros sobredimensionados y un contador de casillas visitadas). Realiza una **búsqueda exhaustiva recursiva**:

1. **Caso base de éxito:** Si la posición actual $(x, y)$ coincide con la meta, se marca la casilla con `🟩`, se guarda en la lista de pasos y se retorna `True`.
2. **Validaciones:** Si la posición excede los bordes o no es una casilla libre (`!= '⬜'`), la rama se descarta retornando `False`.
3. **Exploración ciega (orden fijo):** Se marca temporalmente la casilla como parte del camino (`🟩`) y se exploran recursivamente las 4 direcciones en orden predeterminado: abajo, derecha, arriba, izquierda.
4. **Desmarcado:** Si ninguna dirección conduce a la salida, se desmarca la casilla devolviéndola a `⬜`, se remueve del camino y se retorna `False`.

> **Relación con la sección 3:** el algoritmo de la versión de backtracking es **el mismo** (mismo orden de exploración, misma casilla desmarcada al retroceder). Lo único que cambia es la organización del código: validación en `es_valida()`, bucle sobre `DIRECCIONES` y constantes en lugar de emojis repetidos. Por eso ambas visitan exactamente la misma cantidad de casillas en todos los casos.

---

## 3. Solución por Backtracking (Recursividad)

Implementada en [`laberinto_backtracking.py`](laberinto_backtracking.py). Sigue el esquema **elegir → explorar → deshacer**:

1. **Validación:** Si la casilla está fuera de los bordes o no es `⬜`, la rama se descarta retornando `False`.
2. **Elegir:** Se marca la casilla como parte del camino (`🟩`) y se agrega a la lista de pasos.
3. **Caso base de éxito:** Si la posición actual coincide con la meta, se retorna `True`.
4. **Explorar (orden fijo):** Se prueban recursivamente las 4 direcciones en este orden:
   - Abajo $(x+1, y)$
   - Derecha $(x, y+1)$
   - Arriba $(x-1, y)$
   - Izquierda $(x, y-1)$
5. **Deshacer (backtrack):** Si ninguna dirección conduce a la salida, la casilla vuelve a `⬜`, se remueve del camino y se retorna `False`.

Como la casilla se **desmarca** al retroceder, el algoritmo puede volver a pasar por ella desde otro camino. Esto es lo que lo hace exhaustivo (y exponencial en zonas abiertas).

---

## 4. Solución por Divide y Vencerás

Implementada en [`laberinto_divide_y_venceras.py`](laberinto_divide_y_venceras.py). El problema se define sobre una **región rectangular** del tablero:

1. **Caso base:** Si la región tiene 16 casillas o menos (`UMBRAL`), se resuelve directamente con una búsqueda en anchura (BFS) restringida a esa región.
2. **Dividir:** La región se parte en dos mitades por su lado más largo.
3. **Vencer:** Si el inicio y la meta quedan en mitades distintas, el camino debe cruzar la línea de corte por algún par de casillas vecinas libres (A, B). Para cada par se resuelve recursivamente *inicio → A* en la primera mitad y *B → meta* en la segunda.
4. **Combinar:** Se concatenan los dos caminos parciales. Se devuelve el primer par que funcione.
5. **Respaldo:** Si el camino necesita cruzar la línea de corte más de una vez (por ejemplo, en laberintos en serpiente), ninguna combinación simple lo encuentra. En ese caso se resuelve directamente sobre toda la región con BFS. El script reporta cuántas veces se usó este respaldo.

---

## 5. Casos de Prueba

Los tres scripts usan **los mismos 6 casos** (más un caso extremo opcional), en dos familias.

### 5.1 Casos "trampa" (escala extrema)

Desde el inicio `(0, 0)`, la primera dirección probada es *abajo*, que entra a una **zona abierta de $k \times k$ sin salida**. Como el backtracking desmarca las casillas al retroceder, debe recorrer **todos los caminos posibles** dentro de esa zona antes de probar *derecha*, que es el pasillo real hacia la meta (borde superior y última columna).

- **$k$ controla el tiempo:** la cantidad de caminos crece de forma explosiva con $k$.
- **Las dimensiones del tablero** controlan el tamaño en memoria y la profundidad de la recursión (el pasillo mide $N + M - 2$ casillas).

| Caso | Dimensiones | Casillas | Zona trampa | Inicio | Fin |
|---|---|---|---|---|---|
| **Pequeño** | $5 \times 5$ | 25 | — | `(0, 0)` | `(4, 4)` |
| **Mediano** | $1.000 \times 1.000$ | 1.000.000 | $5 \times 5$ | `(0, 0)` | `(999, 999)` |
| **Grande** | $3.000 \times 3.000$ | 9.000.000 | $6 \times 6$ | `(0, 0)` | `(2999, 2999)` |
| **Extremo** *(opcional)* | $5.000 \times 5.000$ | 25.000.000 | $7 \times 7$ | `(0, 0)` | `(4999, 4999)` |

El caso **Extremo** está desactivado por defecto en fuerza bruta y backtracking (`INCLUIR_EXTREMO = False`) porque tardaría horas. En divide y vencerás está activado.

### 5.2 Casos rectangulares ($N \neq M$)

Laberintos definidos manualmente, con un único camino posible entre inicio y meta, sobre tableros no cuadrados.

| Caso | Dimensiones | Inicio | Fin |
|---|---|---|---|
| **Rectangular ancho** | $3 \times 15$ | `(0, 0)` | `(2, 14)` |
| **Rectangular alto** | $15 \times 3$ | `(0, 0)` | `(14, 2)` |
| **Rectangular extra ancho** | $7 \times 21$ | `(0, 0)` | `(6, 20)` |

---

## 6. Análisis de Complejidad

### 6.1 Fuerza bruta y backtracking

Ambas versiones comparten algoritmo, así que tienen la misma complejidad.

**Tiempo: $O(4^{N \times M})$ en el peor caso.**
- En una zona abierta, desde cada casilla se pueden intentar hasta 4 ramificaciones, y la profundidad está acotada por el número de casillas. Como las casillas se desmarcan al retroceder, se exploran todos los caminos simples posibles.
- En los casos trampa, el costo está dominado por la zona $k \times k$: medimos 155.745 casillas visitadas con $k = 5$ y 31.817.177 con $k = 6$, es decir, **aproximadamente 200 veces más por cada unidad que aumenta $k$**.

**Espacio: $O(N \times M)$.**
- La pila de llamadas puede llegar a tener tantos niveles como casillas transitables. En los casos trampa la profundidad es la longitud del camino (1.999 y 5.999 niveles), lo que obliga a subir el límite de recursión de Python y ejecutar en un hilo con pila grande.

### 6.2 Divide y vencerás

- **Caso base:** BFS sobre una región de a lo sumo 16 casillas, costo constante.
- **Recurrencia:** cada nivel parte la región en dos mitades y revisa los pares de casillas de la línea de corte. En los casos trampa el primer par probado (el pasillo superior) es el correcto, así que la recursión baja por una sola rama.
- **Resultado medido:** las casillas visitadas son del orden de la **longitud del camino** (2.001 para el mediano, 6.000 para el grande, 10.003 para el extremo), sin importar el tamaño de la zona trampa.
- **Peor caso:** si muchos pares de la línea de corte fallan, o si se activa el respaldo, el costo crece (el respaldo recorre toda la región con BFS). No se demuestra aquí una cota ajustada para el peor caso; la comparación es empírica.
- **Limitación:** al resolver cada mitad por separado, un camino que cruza la línea de corte varias veces solo se encuentra mediante el respaldo. El resultado siempre es correcto, pero en laberintos en serpiente la división aporta menos.

---

## 7. Medición Empírica de Tiempos

Medidos en una sola ejecución (los tiempos varían según el equipo).

| Caso | Dimensiones | Zona trampa | Fuerza bruta: tiempo | Backtracking: tiempo | Divide y vencerás: tiempo | Casillas visitadas (FB = BT) | Casillas visitadas (DV) |
|---|---|---|---|---|---|---|---|
| Pequeño | $5 \times 5$ | — | ~0.00002 s | ~0.00003 s | ~0.00009 s | 17 | 24 |
| Mediano | $1.000 \times 1.000$ | $5 \times 5$ | ~0.20 s | ~0.23 s | ~0.16 s | 155.745 | 2.001 |
| Grande | $3.000 \times 3.000$ | $6 \times 6$ | **~32 s** | **~45 s** | ~0.03 s | 31.817.177 | 6.000 |
| Extremo | $5.000 \times 5.000$ | $7 \times 7$ | **~2,5 horas (estimado, no ejecutado)** | **~2,5 horas (estimado, no ejecutado)** | ~0.04 s | ~6.500 millones (estimado) | 10.003 |

> **Notas:**
> - El tiempo del mediano en divide y vencerás (~0.16 s) incluye trabajo fijo de Python sobre un tablero de un millón de casillas. Lo relevante es la columna de casillas visitadas: 2.001 contra 155.745.
> - La estimación del caso extremo en backtracking extrapola el factor de ~200 que se midió entre $k = 5$ y $k = 6$. No fue ejecutado.
> - Fuerza bruta y backtracking visitan **exactamente las mismas casillas**; la diferencia de tiempo entre ellas (32 s contra 45 s en el caso Grande) viene de la variación entre ejecuciones y de las llamadas extra de la versión refactorizada, no de una mejora algorítmica.
> - En los casos pequeños y en los rectangulares (todos de menos de 50 casillas de camino) ambos algoritmos son instantáneos. La diferencia solo aparece cuando hay una zona abierta grande que explorar.

---

## 8. Instrucciones de Ejecución

```bash
python laberinto_fuerza_bruta.py
python laberinto_backtracking.py
python laberinto_divide_y_venceras.py
```

- Fuerza bruta y backtracking tardan entre 30 y 45 segundos por el caso Grande. Para añadir el caso Extremo, cambia `INCLUIR_EXTREMO = True` (no recomendado: horas de ejecución).
- Los tableros de 5.000 × 5.000 usan cientos de MB de memoria. Si tu equipo tiene poca RAM, desactiva `INCLUIR_EXTREMO` en `laberinto_divide_y_venceras.py`.
- Los tres scripts suben el límite de recursión y ejecutan en un hilo con 512 MB de pila. Si tu sistema no lo permite, reduce `threading.stack_size` o las dimensiones.
python laberinto_backtracking.py
python laberinto_divide_y_venceras.py
```

- El backtracking tarda unos 45 segundos por el caso Grande. Para añadir el caso Extremo, cambia `INCLUIR_EXTREMO = True` (no recomendado: horas de ejecución).
- Los tableros de 5.000 × 5.000 usan cientos de MB de memoria. Si tu equipo tiene poca RAM, desactiva `INCLUIR_EXTREMO` en `laberinto_divide_y_venceras.py`.
- Los scripts suben el límite de recursión y ejecutan en un hilo con 512 MB de pila. Si tu sistema no lo permite, reduce `threading.stack_size` o las dimensiones.

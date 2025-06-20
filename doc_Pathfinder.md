---

# Documentación - Pathfinding

Este módulo implementa funciones para la generación y visualización de rutas (caminos) utilizando un grafo generado con PRM (Probabilistic Roadmap) y búsqueda A\*.

---

## Funciones

### `get_path(game, home, goal, path_length=200)`

Calcula un camino desde una posición inicial (`home`) hasta una posición objetivo (`goal`) en el mapa del juego.

* **Parámetros:**

  * `game`: Objeto que contiene el estado del juego (nodos, obstáculos, posiciones).
  * `home`: Lista o tupla con coordenadas `[x, y]` del punto de inicio.
  * `goal`: Lista o tupla con coordenadas `[x, y]` del objetivo.
  * `path_length`: Número entero que limita la longitud máxima del camino resultante (por defecto 200).

* **Retorna:**

  * Una lista de nodos que representan el camino desde `home` hasta `goal`, limitada en tamaño por `path_length`.
  * Retorna una lista vacía si no se encontró camino válido.

* **Descripción:**

  * La función realiza una búsqueda tipo A\* sobre un grafo de nodos pre-generados (`game.nodes`).
  * Selecciona un nodo vecino válido más cercano al inicio que no colisione con obstáculos.
  * Explora nodos abiertos hasta encontrar un nodo desde el cual se puede llegar al objetivo sin colisiones.
  * Reconstruye el camino desde el nodo objetivo hacia el inicio usando referencias a nodos padres.
  * Ordena la lista de nodos abiertos según heurística (distancia estimada al objetivo).
  * Retorna el camino calculado o vacío si no hay ruta.

---

### `show_path_legacy(game, on=False)`

Dibuja en pantalla el camino almacenado en `game.whale.path`.

* **Parámetros:**

  * `game`: Objeto con el estado del juego y pantalla.
  * `on`: Booleano que activa o desactiva el dibujo del camino.

* **Comportamiento:**

  * Si `on` es `True` y existe un camino (`game.whale.path`), dibuja un círculo rojo en cada nodo del camino.
  * Dibuja líneas rojas que conectan nodos consecutivos para visualizar la ruta.

---

### `show_path_legacy_1(game, entity, on=False)`

Muestra el camino de una entidad específica dibujando los nodos y las conexiones en la pantalla.

* **Parámetros:**

  * `game`: Objeto del juego.
  * `entity`: Objeto con atributo `path`, que contiene una lista de posiciones `[x, y]`.
  * `on`: Booleano para activar/desactivar la visualización.

* **Comportamiento:**

  * Si `on` es `True` y `entity.path` no está vacío, dibuja círculos rojos en las posiciones del camino.
  * Dibuja líneas rojas entre cada par de nodos consecutivos para visualizar la ruta.

---

### `show_path_legacy_2(game, entity, on=False)`

Función variante para mostrar caminos usando rutas almacenadas en atributos del juego, enfocada en rutas de jugador y no jugador.

* **Parámetros:**

  * `game`: Estado del juego.
  * `entity`: Entidad que contiene ruta.
  * `on`: Booleano para activar/desactivar la visualización.

* **Comportamiento:**

  * Si `on` es `True` y la entidad tiene ruta, dibuja en pantalla los nodos y conexiones en rojo.
  * Utiliza rutas almacenadas en `game.not_player.path` y `game.player.path`.

---
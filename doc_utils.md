---

# utils.py - Documentación

Este módulo contiene funciones utilitarias para la generación de rutas, cálculo de distancias y visualización gráfica en un entorno de juego con Pygame. Incluye funciones para manejo de entidades móviles, detección de colisiones y visualización de nodos y caminos.

---

## Funciones

### `gen_next_route(entity, speed, m=5)`

Genera una lista de posiciones interpoladas desde la posición actual de la entidad hasta los siguientes `m` nodos en su camino.

* **Parámetros:**

  * `entity`: Objeto que posee atributos `position` (posición actual) y `path` (lista de nodos destino).
  * `speed`: Velocidad usada para determinar la cantidad de pasos entre nodos.
  * `m` (opcional): Número máximo de nodos siguientes para generar la ruta (default=5).

* **Funcionamiento:**

  * Para cada nodo en los próximos `m` nodos del camino:

    * Calcula la diferencia horizontal y vertical entre la posición actual y el nodo.
    * Determina el número de pasos necesarios para llegar al nodo, garantizando al menos 1.
    * Utiliza interpolación lineal (`np.linspace`) para generar las posiciones intermedias.
    * Añade estas posiciones a `entity.path_positions`.
  * Actualiza la posición actual al nodo recién procesado.

---

### `set_pos(entity, position)`

Actualiza la posición de una entidad y mueve el rectángulo de colisión de Pygame a esa posición.

* **Parámetros:**

  * `entity`: Objeto con atributos `position` y `rect`.
  * `position`: Nueva posición (tupla o lista con coordenadas x, y).

---

### `d(p_a, p_b)`

Calcula la distancia euclidiana entre dos puntos `p_a` y `p_b`.

* **Parámetros:**

  * `p_a`: Punto 1 como tupla o lista (x, y).
  * `p_b`: Punto 2 como tupla o lista (x, y).

* **Retorna:**

  * Distancia float entre los dos puntos.

---

### `dist(node_a, node_b)`

Calcula la distancia entre dos nodos basándose en sus posiciones.

* **Parámetros:**

  * `node_a`: Objeto nodo con atributo `.pos` (x, y).
  * `node_b`: Objeto nodo con atributo `.pos` (x, y).

* **Retorna:**

  * Distancia float entre nodos o infinito si alguno es `None`.

---

### `show_graph(game, on=False)`

Dibuja en pantalla las conexiones del grafo entre nodos.

* **Parámetros:**

  * `game`: Objeto que contiene la pantalla (`game.screen`) y lista de nodos (`game.nodes`).
  * `on`: Booleano que indica si dibujar el grafo (default False).

* **Funcionamiento:**

  * Por cada nodo, dibuja líneas blancas a sus nodos hijos.
  * Dibuja un círculo morado para cada nodo.

---

### `show_path(game, entity, on=False)`

Dibuja el camino actual de una entidad en la pantalla.

* **Parámetros:**

  * `game`: Objeto juego con atributo `screen`.
  * `entity`: Objeto con atributo `path` (lista de nodos).
  * `on`: Booleano para activar/desactivar el dibujo (default False).

* **Funcionamiento:**

  * Dibuja círculos rojos en cada nodo del camino.
  * Dibuja líneas rojas entre nodos consecutivos.

---

### `show_menu(screen)`

Muestra el menú de pausa con un fondo blanco semitransparente y texto con controles.

* **Parámetros:**

  * `screen`: Pantalla de Pygame donde se dibuja el menú.

* **Funcionamiento:**

  * Obtiene dimensiones de la pantalla.
  * Renderiza título grande "P A U S A".
  * Renderiza las instrucciones de controles en texto más pequeño.
  * Dibuja un rectángulo con fondo blanco semitransparente y borde negro redondeado.
  * Centra el texto en la pantalla.

---

### `show_score(game)`

Dibuja en pantalla el puntaje actual del juego en la esquina superior izquierda.

* **Parámetros:**

  * `game`: Objeto que contiene `screen` y atributo `score`.

* **Funcionamiento:**

  * Renderiza el texto del puntaje (dividido entre 10 y convertido a entero).
  * Posiciona el texto en coordenadas (10, 10) (superior izquierda).

---

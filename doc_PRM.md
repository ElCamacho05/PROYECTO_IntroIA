# Documentación: Módulo de Nodos y Generación de Grafo PRM

Este módulo define la clase `Nodo` y funciones auxiliares para generar muestras aleatorias de nodos y conectarlos usando el método Probabilistic Roadmap (PRM). Incluye funcionalidades para verificar colisiones entre trayectorias, generar vecinos válidos y construir el grafo de conexiones.

## Clase `Nodo`

Representa un punto en el espacio de estados utilizado para planificación de rutas.

### Atributos:

* `pos`: Posición (x, y) del nodo.
* `papa`: Nodo padre (referencia al nodo anterior en el camino).
* `hijos`: Lista de nodos conectados como vecinos.
* `h`: Heurística (valor comparativo, por ejemplo, distancia a la meta).
* `costo`: Costo acumulado desde el nodo origen hasta este nodo.

### Métodos:

* `__eq__`, `__lt__`, `__str__`: Para comparaciones y visualización.

## Funciones Auxiliares

### `in_collision(pos, game)`

Verifica si una posición (x, y) está fuera de la pantalla o colisiona con algún obstáculo.

### `trajectory_collided(node_a, node_b, obstacles, step=5)`

Comprueba si el camino entre dos nodos colisiona con obstáculos. Se divide en pasos y se verifica cada punto intermedio.

### `trajectory_collided_legacy_1(...)`, `trajectory_collided_legacy_2(...)`

Versiones alternativas para verificar colisiones a lo largo de una trayectoria.

### `gen_samples(game, samples=200)`

Genera una lista de nodos aleatorios no colisionantes dentro del entorno definido en `game`.

### `d(p_a, p_b)` / `dist(node_a, node_b)`

Calcula la distancia euclidiana entre dos puntos o nodos.

### `get_nearest_neighbors(node, nodes, obstacles, k=5)`

Devuelve los `k` vecinos más cercanos al nodo dado, sin colisión en la trayectoria.

### `get_nearest_node(node, nodes, obstacles)`

Retorna el nodo más cercano entre un conjunto de nodos.

### `gen_graph(game, samples=200, k=20)`

Función principal del módulo que:

1. Genera `samples` nodos usando `gen_samples`.
2. Encuentra hasta `k` vecinos válidos para cada nodo.
3. Construye el grafo conectando los nodos con sus vecinos no colisionantes.

## Dependencias

* `pygame`: Para manejo de colisiones por rectángulos.
* `numpy`: Para cálculos vectoriales (interpolaciones).
* `Settings`: Clase externa que provee configuraciones como tamaño y velocidad de la ballena.

## Aplicación

Este módulo se utiliza principalmente para planificación de caminos en entornos con obstáculos, especialmente en simulaciones donde una entidad (como una ballena o nave) debe navegar un espacio 2D evitando colisiones.

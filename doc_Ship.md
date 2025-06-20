
---

# Clase Ship

La clase **Ship** representa la nave controlada por el jugador en el juego. Esta clase gestiona la posición, movimiento, colisiones y la inteligencia artificial para calcular rutas de navegación.

---

## Constructor `__init__(self, game)`

Inicializa la nave con referencia a la pantalla, configuraciones del juego y carga la imagen. También inicializa variables de control para el movimiento por teclado y para la IA.

* `game`: Instancia del juego que contiene pantalla, configuraciones, y elementos como nodos, obstáculos y otros.

Variables inicializadas importantes:

* `self.position`: Posición actual de la nave (lista con coordenadas `[x, y]`).
* `self.rect`: Rectángulo de Pygame asociado a la imagen para dibujar y colisiones.
* `self.moving_up`, `self.moving_down`, `self.moving_left`, `self.moving_right`: Flags para controlar movimiento vía teclado.
* `self.scaler_x`, `self.scaler_y`, `self.model`: Variables para la IA de navegación (escaladores y modelo ML).
* `self.path`, `self.path_positions`: Listas para guardar la ruta calculada y los pasos intermedios.
* `self.max_path`: Número máximo de nodos considerados para generar pasos.
* `self.move`: Indica si la nave puede moverse.
* `self.recalculating`: Flag que indica si se está calculando una ruta en segundo plano.

---

## Método `set_pos(self, position)`

Actualiza la posición de la nave y el rectángulo para que el dibujo y colisiones coincidan.

* `position`: Lista o tupla `[x, y]` con la nueva posición.

---

## Método `update_player(self, game)`

Actualiza la posición de la nave según las teclas de movimiento presionadas, verificando colisiones contra obstáculos y límites de pantalla. Además, incrementa la puntuación del juego con cada movimiento válido.

* `game`: Instancia del juego para acceder a obstáculos y actualizar puntuación.

---

## Método `gen_next_route(self, m=1)`

Genera posiciones intermedias (interpoladas) para moverse suavemente entre nodos del camino.

* `m`: Número máximo de nodos del camino a utilizar para generar posiciones (por defecto 1).

Utiliza `numpy.linspace` para interpolar posiciones entre la posición actual y los nodos objetivo.

---

## Método `get_vector(self, game)`

Construye el vector de características que será usado como entrada para la IA. Este vector incluye:

* Posiciones de todos los nodos del mapa.

* Posición actual de la nave (home).

* Posición actual de la ballena (goal).

* `game`: Instancia del juego para acceder a nodos y entidades.

Retorna una lista con todas las posiciones concatenadas.

---

## Método `get_path_AI(self, game)`

Genera un camino usando el modelo de inteligencia artificial entrenado:

1. Obtiene el vector de entrada y lo escala.
2. Predice la ruta en el espacio escalado.
3. Invierte la escala para obtener posiciones reales.
4. Construye el camino con pares `(x, y)` de posiciones y agrega el objetivo final.

* `game`: Instancia del juego.

Retorna una lista de posiciones que forman el camino.

---

## Método `calculate_path_async(self, game)`

Calcula la ruta en un hilo separado para evitar congelar el hilo principal del juego.

1. Marca el estado de cálculo como activo (`recalculating`).
2. Obtiene el camino usando la IA.
3. Genera las posiciones intermedias para el movimiento suave.
4. Marca el cálculo como terminado y habilita el movimiento.

* `game`: Instancia del juego.

---

## Método `update_AI(self, game)`

Actualiza el movimiento de la nave controlada por IA. Recalcula el camino si:

* No existe un camino.
* No hay posiciones intermedias para avanzar.
* El objetivo está demasiado lejos del final del camino actual.

Si se tiene camino y posiciones, avanza al siguiente paso, verificando colisiones para evitar obstáculos.

* `game`: Instancia del juego.

---

## Método `blit(self)`

Dibuja la imagen de la nave en la pantalla en la posición actual.

---

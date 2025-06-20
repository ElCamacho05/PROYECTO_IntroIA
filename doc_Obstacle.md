# Documentación - Obstáculo y generación de obstáculos en el juego

## Clase `Obstacle`

### Descripción

Representa un obstáculo visual dentro del juego. Cada obstáculo tiene una posición específica, una imagen asociada que se renderiza en pantalla, y un rectángulo (`pygame.Rect`) que define su área para detectar colisiones.

### Atributos

- `screen` (pygame.Surface): Pantalla del juego donde se dibuja el obstáculo.
- `screen_rect` (pygame.Rect): Rectángulo que representa los límites de la pantalla.
- `position` (tuple): Coordenadas (x, y) donde se coloca el centro del obstáculo.
- `image` (pygame.Surface): Imagen del obstáculo cargada y escalada.
- `rect` (pygame.Rect): Rectángulo que delimita la imagen para posicionamiento y colisiones.

### Métodos

- `__init__(position, game)`: Constructor que recibe la posición y referencia al juego para configurar el obstáculo.
- `blit()`: Dibuja la imagen del obstáculo en la pantalla del juego en su posición actual.

---

## Función `generate_obstacles`

### Descripción

Genera y posiciona aleatoriamente una cantidad dada de obstáculos dentro del área visible del juego. Evita que nuevos obstáculos se superpongan con otros objetos ya existentes al chequear colisiones con rectángulos previamente almacenados.

### Parámetros

- `total` (int): Número total de obstáculos a generar.
- `screen_range` (tuple): Tamaño máximo (ancho, alto) del área en la pantalla donde se pueden colocar los obstáculos.
- `rects` (list): Lista de `pygame.Rect` de objetos ya ubicados para evitar solapamientos.
- `game` (Game): Instancia del juego que contiene la pantalla y configuración.

### Funcionamiento

- Para cada obstáculo a generar:
  - Se elige una posición aleatoria dentro de los límites dados.
  - Se crea un nuevo objeto `Obstacle` en esa posición.
  - Si la posición genera colisión con algún rectángulo existente, se busca otra posición aleatoria hasta encontrar una válida.
  - Se añade el obstáculo y su rectángulo a las listas correspondientes en el juego para futuras comprobaciones.

---

## Notas

- La función usa `pygame.Rect.collidelist()` para detectar colisiones entre rectángulos.
- El tamaño de los obstáculos es escalado según la configuración almacenada en el objeto `game.settings`.
- El uso de `random()` permite generar posiciones flotantes dentro de la pantalla, que luego se usan para centrar el rectángulo de cada obstáculo.

---
---

# Settings.py - Documentación de la clase `Settings`

## Descripción general

La clase `Settings` contiene la configuración global para el juego. Define parámetros clave que afectan el comportamiento visual y funcional, como el tamaño de la ventana, las velocidades y dimensiones de objetos, la cantidad de obstáculos y opciones para mostrar elementos gráficos.

---

## Atributos

### Dimensiones y colores de pantalla

* **`screen_width`** (`int`):
  Ancho de la ventana del juego en píxeles.
  *Valor por defecto:* `1200`

* **`screen_height`** (`int`):
  Altura de la ventana del juego en píxeles.
  *Valor por defecto:* `600`

* **`bg_color`** (`tuple`):
  Color de fondo de la pantalla en formato RGB.
  *Valor por defecto:* `(20, 109, 218)`

---

### Configuración de la nave (Ship)

* **`ship_size`** (`tuple`):
  Tamaño de la nave en píxeles (ancho, alto).
  *Valor por defecto:* `(25, 25)`

* **`ship_speed`** (`float`):
  Velocidad de movimiento de la nave.
  *Valor por defecto:* `0.20`

---

### Configuración de la ballena (Whale)

* **`whale_size`** (`tuple`):
  Tamaño de la ballena enemiga en píxeles (ancho, alto).
  *Valor por defecto:* `(25, 25)`

* **`whale_speed`** (`float`):
  Velocidad de movimiento de la ballena.
  *Valor por defecto:* `0.25`

---

### Configuración de los obstáculos

* **`total_obstacles`** (`int`):
  Cantidad total de obstáculos a generar en el mapa.
  *Valor por defecto:* `50`

* **`obstacle_size`** (`tuple`):
  Tamaño de cada obstáculo en píxeles (ancho, alto).
  *Valor por defecto:* `(30, 30)`

---

### Opciones de visualización

* **`show_graph`** (`bool`):
  Indica si se debe mostrar el grafo de navegación (usado principalmente para depuración).
  *Valor por defecto:* `False`

* **`show_path`** (`bool`):
  Indica si se debe mostrar el camino calculado por la IA.
  *Valor por defecto:* `False`

---

### Control de recálculo de rutas

* **`last_path_time`** (`int`):
  Último timestamp en milisegundos en el que se calculó un nuevo camino.
  *Valor por defecto:* `0`

* **`path_interval`** (`int`):
  Intervalo mínimo en milisegundos entre recalculaciones de ruta para evitar cálculos excesivos.
  *Valor por defecto:* `100`

---

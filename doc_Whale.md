
---

# Clase Whale

La clase `Whale` representa la ballena enemiga en el juego.
Esta clase maneja la imagen, posición, movimientos, y cálculo de rutas para perseguir la nave del jugador usando distintas técnicas de inteligencia artificial.

---

## Métodos y atributos principales

### `__init__(self, game)`

Inicializa la ballena:

* Carga la imagen y la escala.
* Define la posición inicial en la esquina superior derecha.
* Inicializa variables para el pathfinding, movimiento y manejo de hilos.
* Registra eventos de teclado para movimiento manual.

---

### `set_pos(self, position)`

Actualiza la posición actual de la ballena y sincroniza su rectángulo para el dibujo y colisiones.

**Argumentos:**

* `position`: Lista o tupla con las coordenadas `[x, y]`.

---

### `calculate_path_async(self, game)`

Calcula de forma asíncrona (en un hilo aparte) la ruta desde la ballena hasta la nave, utilizando el algoritmo de pathfinding (A\*).
Durante el cálculo se bloquea el movimiento y se actualiza la ruta cuando termina.

---

### `simple_pursue(self, game)`

Implementa un movimiento simple hacia la nave:

* Se mueve en los ejes X y Y para acercarse a la nave.
* Verifica colisiones con obstáculos para evitar superposiciones.
* Actualiza la posición si no hay colisión.

---

### `gen_next_route(self, m=5)`

Genera puntos interpolados para las próximas `m` posiciones en la ruta, permitiendo un movimiento continuo y más natural.

---

### `update_AI(self, game, t="s")`

Actualiza la IA y movimiento de la ballena dependiendo del tipo:

* `'s'` para movimiento simple directo (simple\_pursue).
* `'a*'` para cálculo de ruta y seguimiento con pathfinding.

  * Recalcula ruta si es necesario.
  * Avanza a la siguiente posición interpolada.

---

### `update_player(self, game)`

Actualiza la posición en base a entradas manuales del jugador (teclas).
Previene colisiones con obstáculos y evita salirse de la pantalla.

---

### `blit(self)`

Dibuja la imagen de la ballena en la pantalla en la posición actual.

---

# Resumen

La clase `Whale` combina gestión gráfica, detección de colisiones y algoritmos de pathfinding para crear un enemigo dinámico que persigue al jugador usando IA básica o avanzada.
El uso de threading para el cálculo de rutas permite mantener fluidez en el juego sin congelar la interfaz.

---

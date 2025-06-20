# Documentación de la clase `MyGame`

## Descripción general

La clase `MyGame` es el núcleo del juego desarrollado con Pygame. Maneja la inicialización del entorno, la lógica principal del juego, el control de eventos, el entrenamiento y ejecución de la IA, y el renderizado en pantalla.

---

## Métodos y atributos detallados

### `__init__(self)`

Inicializa la instancia principal del juego:

- Configura Pygame y la ventana.
- Carga configuraciones generales desde la clase `Settings`.
- Instancia las entidades principales (nave, ballena).
- Genera obstáculos evitando colisiones iniciales.
- Crea el grafo para el pathfinding con 200 nodos.
- Inicializa variables para puntuación, IA, estados y etapas de juego.

---

### `gen_dataset_legacy(self)`

Genera un dataset en formato legacy basado en el conjunto `self.set`.

- Combina posiciones estáticas del mapa, puntos de inicio y objetivo, y caminos.
- Rellena los caminos incompletos con valores `[-1, -1]`.
- Retorna dos listas: `X` con datos de entrada y `y` con datos de salida.

---

### `gen_dataset(self, s)`

Genera un dataset moderno a partir de una lista de diccionarios que contienen mapa, punto inicial (`home`), objetivo (`goal`) y camino (`path`).

- Procesa cada subconjunto y concatena las posiciones correspondientes.
- Para caminos incompletos rellena con `[-1, -1]`.
- Retorna `X` y `y` como listas de datos para entrenamiento.

---

### `gen_synthetic_samples_legacy_1(self, sample_count=200)`

Genera muestras sintéticas (versión legacy) para el entrenamiento de la IA.

- Evita que las posiciones de la ballena, la nave y obstáculos colisionen.
- Crea un conjunto de datos con mapas, obstáculos, posiciones iniciales y caminos.
- Retorna datasets `X_n` y `y_n`.

---

### `gen_synthetic_samples(self, sample_count=200)`

Genera muestras sintéticas modernas para el entrenamiento.

- Similar a la versión legacy, pero con lógica actualizada y sin incluir obstáculos en el dataset.
- Asegura caminos válidos entre ballena y nave.
- Retorna datasets para entrenamiento.

---

### `train_AI(self)`

Entrena un modelo de red neuronal MLP utilizando muestras sintéticas.

- Escala los datos con `MinMaxScaler`.
- Configura una red profunda con varias capas ocultas.
- Ajusta el modelo a los datos escalados.
- Asigna el modelo y los escaladores a la instancia `ship` para su uso futuro.
- Retorna el modelo entrenado.

---

### `parallel_training(self)`

Ejecuta el entrenamiento de la IA en un hilo separado para no bloquear el hilo principal.

- Crea y arranca un hilo que ejecuta `train_AI`.

---

### `run_game(self)`

Bucle principal del juego que se ejecuta infinitamente.

- Gestiona eventos (teclado, cierre).
- Actualiza la pantalla.
- Controla la lógica del juego según la etapa:
  - **Etapa 1:** Ballena IA persigue nave controlada por jugador.
  - **Etapa 2:** Nave IA persigue ballena controlada por jugador.
- Maneja colisiones, reinicios y cambio de roles IA/jugador.

---

### `_check_events(self)`

Escucha y maneja eventos de Pygame:

- Salida del juego.
- Pulsaciones y liberaciones de teclas.

---

### `_chek_keydown(self, event)`

Procesa pulsaciones de teclas para:

- Movimiento (flechas y WASD).
- Mostrar u ocultar grafo (`E`).
- Mostrar u ocultar ruta (`R`).
- Pausar o continuar el juego (`P` o ESC).
- Salir del juego (`Q`).

---

### `_chek_keyup(self, event)`

Procesa liberaciones de teclas para detener movimientos.

---

### `_update_screen(self)`

Redibuja la pantalla en cada frame:

- Fondo, obstáculos, nave y ballena.
- Muestra puntuación, grafo y ruta si están habilitados.
- Muestra menú de pausa si está activado.
- Actualiza el display.

---

## Uso

El juego se inicia ejecutando el script directamente, creando una instancia de `MyGame` y llamando a `run_game()`.

```python
if __name__ == "__main__":
    md = MyGame()
    md.run_game()

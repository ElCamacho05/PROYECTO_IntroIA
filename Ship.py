from PRM import d, in_collision
import numpy as np
import pygame.image
import threading


class Ship:
    def __init__(self, game):
        """
        Inicializa la nave del jugador dentro del contexto del juego.

        Args:
            game: Objeto que contiene el estado general del juego,
                  incluyendo pantalla, configuraciones y elementos.
        """
        # Referencia a la pantalla y su rectángulo para límites y dibujo
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Configuraciones globales del juego (tamaños, velocidades, etc.)
        self.settings = game.settings

        # Carga la imagen de la nave, y la escala al tamaño configurado
        self.image = pygame.image.load('images/boat.bmp')
        self.image = pygame.transform.scale(self.image, self.settings.ship_size)

        # Obtiene el rectángulo asociado a la imagen para posición y colisiones
        self.rect = self.image.get_rect()
        # Posiciona inicialmente la nave en la esquina inferior izquierda de la pantalla
        self.rect.bottomleft = self.screen_rect.bottomleft
        self.position = list(self.rect.center)

        # Variables para controlar el movimiento vía teclado
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

        # Variables para escaladores y modelo de IA (Machine Learning)
        self.scaler_x = None  # Escalador de entrada (features)
        self.scaler_y = None  # Escalador de salida (labels)
        self.model = None  # Modelo ML que predice la ruta

        # Variables para almacenar el camino generado por la IA
        self.path = []  # Lista de nodos o posiciones destino
        self.path_positions = []  # Lista de posiciones intermedias para moverse suavemente
        self.max_path = 5  # Número máximo de nodos a considerar para generar posiciones
        self.move = False  # Indica si la nave está en movimiento
        self.path_model = None  # Referencia adicional para el modelo de ruta (si aplica)
        self.path_thread = None  # Hilo para calcular rutas en segundo plano

        # Control para evitar cálculos simultáneos de rutas
        self.recalculating = False

    def set_pos(self, position):
        """
        Actualiza la posición actual de la nave y su rectángulo para el dibujo.

        Args:
            position: Lista o tupla con coordenadas [x, y]
        """
        self.position = position
        self.rect.center = position

    def update_player(self, game):
        """
        Actualiza la posición de la nave según las teclas presionadas y evitando colisiones.

        Args:
            game: Estado actual del juego, usado para acceso a obstáculos y puntuación.
        """
        obstacles = game.obstacles

        # Movimiento hacia arriba con verificación de colisiones y límites de pantalla
        if self.moving_up and self.rect.bottom > self.settings.ship_size[1]:
            future_rect = self.rect.copy()
            future_rect.centery = self.position[1] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] -= self.settings.ship_speed
                game.score += self.settings.ship_speed

        # Movimiento hacia abajo
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            future_rect = self.rect.copy()
            future_rect.centery = self.position[1] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] += self.settings.ship_speed
                game.score += self.settings.ship_speed

        # Movimiento hacia la derecha
        if self.moving_right and self.rect.right < self.screen_rect.right:
            future_rect = self.rect.copy()
            future_rect.centerx = self.position[0] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] += self.settings.ship_speed
                game.score += self.settings.ship_speed

        # Movimiento hacia la izquierda
        if self.moving_left and self.rect.left > 0:
            future_rect = self.rect.copy()
            future_rect.centerx = self.position[0] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] -= self.settings.ship_speed
                game.score += self.settings.ship_speed

        # Actualiza el rectángulo para que coincida con la posición actual
        self.rect.center = self.position

    def gen_next_route(self, m=1):
        """
        Genera las posiciones intermedias para moverse suavemente hacia los siguientes nodos del camino.

        Args:
            m: Número máximo de nodos a usar para generar posiciones intermedias (por defecto 1).
        """
        current_pos = self.position

        # Itera sobre los primeros m nodos del camino para generar puntos de interpolación
        for i, node in enumerate(self.path[:min(len(self.path), m)]):
            dx = abs(node[0] - current_pos[0])
            dy = abs(node[1] - current_pos[1])

            # Calcula cuántos pasos hacer según la distancia y la velocidad
            num = max(
                int(dx / self.settings.ship_speed),
                int(dy / self.settings.ship_speed),
                1
            )

            # Crea listas de posiciones interpoladas en x e y usando numpy.linspace
            x_arr = np.linspace(current_pos[0], node[0], num)
            y_arr = np.linspace(current_pos[1], node[1], num)

            # Combina las listas de x y y en posiciones y las agrega a path_positions
            self.path_positions += [list(par) for par in zip(x_arr, y_arr)]
            current_pos = node

    def get_vector(self, game):
        """
        Construye el vector de características (features) para la IA a partir de posiciones de nodos y entidades.

        Args:
            game: Estado actual del juego con nodos y entidades.

        Returns:
            Lista con valores concatenados representando las posiciones relevantes del juego.
        """
        X = []
        # Añade las posiciones de todos los nodos al vector
        for nodo in game.nodes:
            X += nodo.pos

        # Se pueden incluir las posiciones de obstáculos si se quiere (comentado)
        # for obs in game.obstacles:
        #     X += obs.rect.center

        # Añade la posición actual de la nave (home) y de la ballena (goal)
        X += self.rect.center
        X += game.whale.rect.center

        return X

    def get_path_AI(self, game):
        """
        Obtiene una ruta predicha por el modelo de IA a partir de las posiciones actuales.

        Args:
            game: Estado actual del juego.

        Returns:
            Lista de posiciones que representan el camino generado por la IA.
        """
        # Obtiene el vector de características y lo escala con scaler_x
        X_input = self.get_vector(game)
        X_s = self.scaler_x.transform([X_input])

        # Predice la ruta en el espacio escalado y la transforma de vuelta
        y_s = self.model.predict(X_s)
        y = self.scaler_y.inverse_transform(y_s)[0]

        # Construye el camino con puntos discretos (pares de coordenadas) y añade el objetivo final
        path = [self.rect.center]
        path += [(int(y[i]), int(y[i + 1])) for i in
                 range(0, 2, 10)]  # Nota: aquí parece un error en rango, usualmente 0 a len(y) con paso 2
        path.append(game.whale.rect.center)
        return path

    def calculate_path_async(self, game):
        """
        Calcula la ruta en un hilo separado para no bloquear el hilo principal del juego.

        Args:
            game: Estado actual del juego.
        """

        def run():
            self.recalculating = True
            self.move = False
            # Obtiene el camino generado por IA
            self.path = self.get_path_AI(game)

            if self.path:
                self.current_target_index = 0
                self.path_positions = []
                # Genera las posiciones intermedias para moverse suavemente
                self.gen_next_route(self.max_path)
            else:
                print("no se pudo generar una ruta")

            self.recalculating = False
            self.move = True

        # Inicia el hilo para cálculo asíncrono de ruta
        self.path_thread = threading.Thread(target=run)
        self.path_thread.start()

    def update_AI(self, game):
        """
        Actualiza la posición de la nave controlada por IA, recalculando la ruta si es necesario.

        Args:
            game: Estado actual del juego.
        """
        need_new_path = False

        # Verifica condiciones para recalcular la ruta
        if not self.path:
            need_new_path = True
            print("no hay camino")
        elif not self.path_positions:
            need_new_path = True
            print("no hay pasos")
        elif d(self.path[-1], game.player.position) > 100:
            need_new_path = True
            print("muy lejos")

        # Si se necesita ruta nueva y no está recalculando, la calcula asíncronamente
        if need_new_path and not self.recalculating:
            self.path_positions = []
            self.calculate_path_async(game)

        # Si hay posiciones para moverse y se permite movimiento, avanza al siguiente paso
        if self.path_positions and self.move:
            print("generando paso")
            next_pos = self.path_positions.pop(0)
            if not in_collision(next_pos, game):
                print("no hay paso" if not next_pos else next_pos)
                self.set_pos(next_pos)
            else:
                # Si la posición siguiente colisiona, reinicia la lista de posiciones para recalcular
                self.path_positions = []

    def blit(self):
        """
        Dibuja la imagen de la nave en la pantalla.
        """
        self.screen.blit(self.image, self.rect)

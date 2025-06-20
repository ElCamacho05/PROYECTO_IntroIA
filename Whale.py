import pygame.image
from Pathfinder import get_path, d
import numpy as np
import threading


class Whale:
    """
    Clase que representa la ballena enemiga en el juego.

    La ballena puede moverse, calcular rutas para perseguir la nave del jugador usando
    algoritmos de pathfinding (como A*), y actualizar su posición en base a la IA seleccionada.
    """

    def __init__(self, game):
        """
        Inicializa la ballena con referencias a la pantalla, configuraciones y carga su imagen.

        Args:
            game: Instancia principal del juego que contiene pantalla, configuraciones y objetos.
        """
        self.screen = game.screen  # Pantalla donde se dibuja la ballena
        self.screen_rect = game.screen.get_rect()  # Rectángulo límite de la pantalla

        self.settings = game.settings  # Configuraciones globales del juego

        # Carga y escala la imagen de la ballena
        self.image = pygame.image.load('images/whale.png')
        self.image = pygame.transform.scale(self.image, self.settings.whale_size)

        # Obtiene el rectángulo que delimita la imagen para posicionarla y detectar colisiones
        self.rect = self.image.get_rect()

        # Inicialmente la posiciona en la esquina superior derecha de la pantalla
        self.rect.topright = self.screen_rect.topright

        # Posición central actual como lista mutable [x, y]
        self.position = list(self.rect.center)

        # Atributos para pathfinding y movimiento
        self.path = []  # Lista de nodos del camino calculado
        self.max_path = 5  # Máximo número de nodos para planificar ruta parcial
        self.path_positions = []  # Lista de posiciones detalladas a lo largo del camino
        self.current_target_index = 0  # Índice del nodo objetivo actual en el camino

        # Variables para manejo de threading (calcular rutas en segundo plano)
        self.recalculating = False  # Indica si está recalculando la ruta actualmente
        self.path_thread = None  # Hilo para calcular ruta
        self.move = False  # Controla si la ballena debe moverse

        # Variables para detectar eventos de teclado (movimiento manual)
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def set_pos(self, position):
        """
        Actualiza la posición de la ballena y sincroniza su rectángulo.

        Args:
            position (list or tuple): Nueva posición (x, y).
        """
        self.position = position
        self.rect.center = position

    def calculate_path_async(self, game):
        """
        Inicia un hilo para calcular la ruta hacia la nave sin bloquear el hilo principal.

        Usa la función `get_path` para obtener el camino desde la ballena hasta la nave.

        Args:
            game: Instancia principal del juego.
        """
        def run():
            self.recalculating = True  # Marca que está calculando
            self.move = False  # Detiene movimiento durante cálculo

            # Obtiene lista de nodos que representan el camino
            path_nodes = get_path(game, game.whale.rect.center, game.ship.rect.center)

            if path_nodes:
                # Guarda datos del mapa, ruta, inicio y meta para análisis/debug
                new_entry = {
                    "map": [nodo.pos[:] for nodo in game.nodes],
                    "home": game.whale.rect.center[:],
                    "goal": game.ship.rect.center[:],
                    "path": [path_nodes[1].pos]  # Nodo siguiente al inicio
                }
                game.set.append(new_entry)

                # Convierte los nodos a posiciones y reinicia el índice del objetivo
                self.path = [node.pos for node in path_nodes]
                self.current_target_index = 0

                # Genera posiciones detalladas para moverse suavemente a lo largo del camino
                self.gen_next_route(self.max_path)

            else:
                print("no se pudo generar una ruta")

            self.recalculating = False  # Marca que terminó el cálculo
            self.move = True  # Permite movimiento

        # Inicia el hilo para el cálculo de ruta
        self.path_thread = threading.Thread(target=run)
        self.path_thread.start()

    def simple_pursue(self, game):
        """
        Movimiento básico para perseguir la nave con movimiento directo y evitando obstáculos simples.

        La ballena intenta moverse en dirección a la nave por separado en ejes X e Y,
        verificando colisiones contra obstáculos antes de moverse.

        Args:
            game: Instancia principal del juego.
        """
        ship = game.ship
        obstacles = game.obstacles

        # Movimiento vertical hacia arriba si la ballena está por debajo de la nave
        if self.position[1] > ship.position[1] and self.rect.bottom > self.settings.ship_size[1]:
            future_rect = self.rect.copy()
            future_rect.y = self.position[1] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] -= self.settings.ship_speed

        # Movimiento vertical hacia abajo si la ballena está por encima de la nave
        elif self.position[1] < ship.position[1] and self.rect.bottom < self.screen_rect.bottom:
            future_rect = self.rect.copy()
            future_rect.y = self.position[1] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] += self.settings.ship_speed

        # Movimiento horizontal hacia la derecha si la ballena está a la izquierda de la nave
        if self.position[0] < ship.position[0] and self.rect.right < self.screen_rect.right:
            future_rect = self.rect.copy()
            future_rect.x = self.position[0] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] += self.settings.ship_speed

        # Movimiento horizontal hacia la izquierda si la ballena está a la derecha de la nave
        elif self.position[0] > ship.position[0] and self.rect.left > 0:
            future_rect = self.rect.copy()
            future_rect.x = self.position[0] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] -= self.settings.ship_speed

        # Actualiza el rectángulo de la ballena a la nueva posición
        self.set_pos(self.position)

    def gen_next_route(self, m=5):
        """
        Genera posiciones interpoladas para los próximos `m` nodos del camino actual.

        Esto permite planificar y mover la ballena suavemente por tramos del camino calculado.

        Args:
            m (int): Número máximo de nodos a planificar en esta generación de ruta.
        """
        current_pos = self.position
        # Itera por hasta m nodos siguientes del camino
        for i, node in enumerate(self.path[:min(len(self.path), m)]):
            dx = abs(node[0] - current_pos[0])
            dy = abs(node[1] - current_pos[1])
            num = max(
                int(dx / self.settings.whale_speed),
                int(dy / self.settings.whale_speed),
                1
            )
            x_arr = np.linspace(current_pos[0], node[0], num)
            y_arr = np.linspace(current_pos[1], node[1], num)
            self.path_positions += [list(par) for par in zip(x_arr, y_arr)]
            current_pos = node  # Actualiza posición para el siguiente nodo

    def update_AI(self, game, t="s"):
        """
        Actualiza el comportamiento y movimiento de la ballena según el tipo de IA seleccionado.

        - 's': Movimiento simple directo hacia la nave.
        - 'a*': Movimiento usando cálculo de ruta con A* y seguimiento del camino.

        Args:
            game: Instancia principal del juego.
            t (str): Tipo de IA ('s' para simple, 'a*' para pathfinding).
        """
        if t == "s":
            self.simple_pursue(game)

        elif t == "a*":
            need_new_path = False

            # Decide si es necesario recalcular ruta
            if not self.path:
                need_new_path = True
            elif not self.path_positions:
                need_new_path = True
            elif d(self.path[-1], game.ship.position) > 100:
                need_new_path = True

            # Si debe recalcular y no está ya en proceso, lanza cálculo
            if need_new_path and not self.recalculating:
                self.path_positions = []
                self.calculate_path_async(game)

            # Si hay posiciones generadas y puede moverse, avanza al siguiente punto
            if self.path_positions and self.move:
                next_pos = self.path_positions.pop(0)
                self.set_pos(next_pos)

    def update_player(self, game):
        """
        Actualiza la posición de la ballena en base a entradas del jugador (movimiento manual).

        Se asegura que la ballena no colisione con obstáculos y que permanezca dentro de la pantalla.

        Args:
            game: Instancia principal del juego.
        """
        obstacles = game.obstacles

        # Movimiento hacia arriba si la tecla está activa y no colisiona
        if self.moving_up and self.rect.bottom > self.settings.ship_size[1]:
            future_rect = self.rect.copy()
            future_rect.centery = self.position[1] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] -= self.settings.ship_speed
                game.score += self.settings.whale_speed

        # Movimiento hacia abajo
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            future_rect = self.rect.copy()
            future_rect.centery = self.position[1] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] += self.settings.ship_speed
                game.score += self.settings.whale_speed

        # Movimiento hacia derecha
        if self.moving_right and self.rect.right < self.screen_rect.right:
            future_rect = self.rect.copy()
            future_rect.centerx = self.position[0] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] += self.settings.ship_speed
                game.score += self.settings.whale_speed

        # Movimiento hacia izquierda
        if self.moving_left and self.rect.left > 0:
            future_rect = self.rect.copy()
            future_rect.centerx = self.position[0] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] -= self.settings.ship_speed
                game.score += self.settings.whale_speed

        # Actualiza la posición del rectángulo para el siguiente frame
        self.rect.center = self.position

    def blit(self):
        """
        Dibuja la ballena en pantalla en su posición actual.
        """
        self.screen.blit(self.image, self.rect)

import sys
import threading

import pygame

from Settings import Settings
from Ship import Ship
from Obstacle import *
from Whale import Whale
from PRM import gen_graph
from Pathfinder import get_path
from os import system
from utils import d, show_graph, show_path, show_menu, show_score

from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler


class MyGame:
    def __init__(self):
        """
        Inicializa la instancia principal del juego:
        - Configura Pygame y la pantalla.
        - Crea las entidades principales (nave, ballena).
        - Genera obstáculos y grafos para pathfinding.
        - Inicializa variables para IA, puntuación, y estados de juego.
        """
        pygame.init()

        # Carga configuraciones generales del juego
        self.settings = Settings()

        # Configura la pantalla con las dimensiones definidas en settings
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # Ajusta los valores de ancho y alto para que sean consistentes con la pantalla real
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()
        self.settings.show_path = False  # Control para mostrar o no la ruta
        self.settings.show_graph = False  # Control para mostrar o no el grafo

        # Instancia la nave controlada por el jugador
        self.ship = Ship(self)

        # Instancia la ballena controlada por IA
        self.whale = Whale(self)

        # Variables que determinan quién es jugador y quién IA (pueden intercambiarse)
        self.player = self.ship
        self.not_player = self.whale
        self.score = 0  # Puntuación inicial

        # Para la generación de obstáculos, excluye las posiciones de nave y ballena
        rects = [self.ship.rect, self.whale.rect]
        self.obstacles = []
        screen_range = [self.settings.screen_width - self.settings.obstacle_size[0],
                        self.settings.screen_height - self.settings.obstacle_size[1]]

        # Genera los obstáculos en el mapa evitando colisiones con nave y ballena
        generate_obstacles(self.settings.total_obstacles, screen_range, rects, self)

        # Define el título de la ventana
        pygame.display.set_caption("PROYECTO - IA")

        # Genera el grafo de nodos para pathfinding, con 200 nodos
        print("Generando mundo")
        self.nodes, self.graph = gen_graph(self, 200)
        print("Grafo generado...")

        self.pause = True  # Estado de pausa inicial

        # Variables para almacenamiento de datos para IA
        self.set = []
        self.X = []
        self.y = []

        self.stage = 1  # Etapa inicial del juego (definida para controlar la lógica)

        # Escaladores y modelo para el entrenamiento de IA
        self.scaler_x = StandardScaler()
        self.scaler_y = StandardScaler()
        self.model = None

    def gen_dataset_legacy(self):
        """
        Genera un dataset en formato antiguo basado en el conjunto self.set.
        Este dataset contiene las posiciones del mapa, obstáculos, punto inicio (home), objetivo (goal) y caminos.

        Retorna:
            X (lista): datos de entrada (posiciones concatenadas).
            y (lista): datos de salida (caminos representados por posiciones).
        """
        X = []
        y = []

        static = []
        if self.set:
            static += [coord for pos in self.set[0]["map"] for coord in pos]

        for entry in self.set:
            row = static.copy()

            row += entry["home"]
            row += entry["goal"]

            X.append(row)

            path_vector = []
            max_path_len = 5
            for i in range(max_path_len):
                if i < len(entry["path"]):
                    path_vector += entry["path"][i]
                else:
                    path_vector += [-1, -1]

            y.append(path_vector)

        return X, y

    def gen_dataset(self, s):
        """
        Genera dataset moderno a partir de un conjunto dado con diccionarios que incluyen
        mapa, home, goal y camino.

        Args:
            s (lista): lista de diccionarios con los datos.

        Retorna:
            X (lista): datos de entrada.
            y (lista): datos de salida (caminos).
        """
        X = []
        y = []

        for subset in s:
            row_x = []
            row_y = []

            for k, v in subset.items():
                if k == "map":
                    for node in v:
                        row_x += node
                elif k == "home":
                    row_x += v
                elif k == "goal":
                    row_x += v
                elif k == "path":
                    for i in range(5):
                        if i >= len(v):
                            row_y += [-1, -1]
                        else:
                            row_y += v[i]
            X.append(row_x)
            y.append(row_y)

        return X, y

    def gen_synthetic_samples_legacy_1(self, sample_count=200):
        """
        Genera muestras sintéticas (versión legacy) para entrenamiento,
        asegurando que posiciones de ballena, nave y obstáculos no colisionen.

        Args:
            sample_count (int): número deseado de muestras sintéticas.

        Retorna:
            X_n, y_n: datasets de entrada y salida para entrenamiento.
        """
        print("generando ejemplos")
        synthetic_set = []

        while len(synthetic_set) < sample_count:
            print(len(synthetic_set))
            rects = [obs.rect for obs in self.obstacles]

            w = pygame.Rect(0, 0, Settings().whale_size[0], Settings().whale_size[1])
            w.center = [random() * self.screen.get_width(), random() * self.screen.get_height()]

            while w.collidelist(rects) != -1:
                for r in rects:
                    if d(w.center, r.center) < 50:
                        w.center = [random() * self.screen.get_width(), random() * self.screen.get_height()]
                    else:
                        break
            print("w agregado")
            rects.append(w)

            ship_rect = pygame.Rect(0, 0, self.settings.ship_size[0], self.settings.ship_size[1])
            ship_rect.center = [random() * self.screen.get_width(), random() * self.screen.get_height()]

            while ship_rect.collidelist(rects) != -1:
                for r in rects:
                    if d(ship_rect.center, r.center) < 50:
                        ship_rect.center = [random() * self.screen.get_width(), random() * self.screen.get_height()]
                    else:
                        break

            print("s agregado")
            rects.append(ship_rect)

            path = get_path(self, w.center, ship_rect.center, 2)
            new_entry = {
                "map": [nodo.pos for nodo in self.nodes],
                "obstacles": [obs.rect.center for obs in self.obstacles],
                "home": w.center,
                "goal": ship_rect.center,
                "path": [path[1].pos]
            }
            synthetic_set.append(new_entry)

        X_n, y_n = self.gen_dataset(synthetic_set)
        return X_n, y_n

    def gen_synthetic_samples(self, sample_count=200):
        """
        Genera muestras sintéticas modernas para entrenamiento de la IA,
        evitando colisiones y garantizando caminos válidos.

        Args:
            sample_count (int): número deseado de muestras sintéticas.

        Retorna:
            X_n, y_n: datasets de entrada y salida para entrenamiento.
        """
        print("generando ejemplos sinteticos")
        set_t = []

        print(len(set_t))
        while len(set_t) < sample_count:
            if len(set_t) % 10 == 0:
                print(f"{int(len(set_t) / sample_count * 100)} % ")
            rects = [obs.rect for obs in self.obstacles]

            whale = pygame.Rect(0, 0, Settings().whale_size[0], Settings().whale_size[1])
            whale.center = [random() * self.screen.get_width(), random() * self.screen.get_height()]

            while whale.collidelist(rects) != -1:
                whale.center = [random() * self.screen.get_width(), random() * self.screen.get_height()]
            rects.append(whale)

            ship = pygame.Rect(0, 0, Settings().ship_size[0], Settings().ship_size[1])
            ship.center = [random() * self.screen.get_width(), random() * self.screen.get_height()]

            while ship.collidelist(rects) != -1:
                ship.center = [random() * self.screen.get_width(), random() * self.screen.get_height()]
            rects.append(ship)

            path = get_path(self, whale.center, ship.center)

            if not path:
                continue
            new_entry = {
                "map": [nodo.pos for nodo in self.nodes],
                "home": whale.center,
                "goal": ship.center,
                "path": [nodo.pos for nodo in path]
            }
            set_t.append(new_entry)
        X_n, y_n = self.gen_dataset(set_t)
        print("ejemplos generados con exito")
        return X_n, y_n

    def train_AI(self):
        """
        Entrena el modelo de IA utilizando muestras sintéticas generadas en tiempo real.
        Usa una red neuronal MLP con múltiples capas y escaladores MinMax.

        Retorna:
            model: modelo entrenado.
        """
        print("Entrenando IA...")

        scaler_x = MinMaxScaler()
        scaler_y = MinMaxScaler()

        X_n, y_n = self.gen_synthetic_samples(500)

        self.X += X_n
        self.y += y_n
        X_scaled = scaler_x.fit_transform(self.X)
        y_scaled = scaler_y.fit_transform(self.y)

        # Definición del modelo MLP con arquitectura profunda
        model = MLPRegressor(hidden_layer_sizes=(256, 128, 64, 32, 16), max_iter=4000)
        model.fit(X_scaled, y_scaled)

        # Asigna el modelo y escaladores a la nave para uso posterior
        self.ship.model = model
        self.ship.scaler_x = scaler_x
        self.ship.scaler_y = scaler_y

        print(f"Entrenamiento finalizado con {len(self.X)} ejemplos")

        return self.ship.model

    def parallel_training(self):
        """
        Ejecuta el entrenamiento de la IA en un hilo paralelo para no bloquear el hilo principal.
        """

        def run():
            print("entrenando IA en segundo plano...")
            model = self.train_AI()
            print("IA entrenada!!!")
            return model

        self.ship.path_model = threading.Thread(target=run)
        self.ship.path_model.start()

    def run_game(self):
        """
        Bucle principal del juego que maneja:
        - Eventos (teclado, cierre).
        - Actualización de estado y pantalla.
        - Lógica de juego según la etapa actual.
        """
        while True:
            self._check_events()
            self._update_screen()

            if self.stage == 1:  # Etapa 1: ballena IA persigue nave jugador
                if not self.pause:
                    # Verifica colisión para cambiar etapa y reiniciar condiciones
                    if self.whale.rect.colliderect(self.ship.rect):
                        print("TE HAN ALCANZADO... moviendo a la etapa 2...")
                        self.pause = True
                        self.stage = 2

                        # Genera dataset y entrena IA para la nueva etapa
                        self.X, self.y = self.gen_dataset(self.set)
                        self.train_AI()

                        # Reposiciona ballena y nave a posiciones iniciales
                        self.whale.rect.topright = self.whale.screen_rect.topright
                        self.whale.position = list(self.whale.rect.center)

                        self.ship.rect.bottomleft = self.ship.screen_rect.bottomleft
                        self.ship.position = list(self.ship.rect.center)

                        # Ajusta velocidades para la nueva etapa
                        diff = self.settings.whale_speed - self.settings.ship_speed
                        self.settings.whale_speed -= diff
                        self.settings.ship_speed += diff

                        # Intercambia control de jugador y IA
                        self.player = self.whale
                        self.not_player = self.ship

                    # Actualiza movimientos y lógica de ambos jugadores
                    self.ship.update_player(self)
                    self.whale.update_AI(self, "a*")

            if self.stage == 2:  # Etapa 2: nave IA persigue ballena jugador
                if not self.pause:
                    if self.whale.rect.colliderect(self.ship.rect):
                        print("TE HAN ALCANZADO... moviendo a la etapa 2...")
                        self.pause = True
                    self.ship.update_AI(self)
                    self.whale.update_player(self)

    def _check_events(self):
        """
        Escucha eventos de Pygame como teclado o cierre de ventana.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._chek_keydown(event)
            elif event.type == pygame.KEYUP:
                self._chek_keyup(event)

    def _chek_keydown(self, event):
        """
        Procesa pulsaciones de teclas para controlar el movimiento o funciones especiales.

        Teclas:
            Flechas o WASD -> movimiento.
            E -> alternar visualización del grafo.
            R -> alternar visualización de la ruta.
            P o ESC -> pausar o reanudar.
            Q -> salir del juego y limpiar consola.
        """
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.player.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.player.moving_down = True
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player.moving_left = True

        elif event.key == pygame.K_e:
            self.settings.show_graph = not self.settings.show_graph
        elif event.key == pygame.K_r:
            self.settings.show_path = not self.settings.show_path
            print("Mostrando ruta.." if self.settings.show_path else "No mostrar ruta")

        elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
            self.pause = not self.pause
        elif event.key == pygame.K_q:
            system("cls")
            sys.exit()

    def _chek_keyup(self, event):
        """
        Procesa la liberación de teclas para detener movimientos.
        """
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.player.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.player.moving_down = False
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player.moving_left = False

    def _update_screen(self):
        """
        Redibuja todos los elementos de la pantalla en cada frame:
        - Fondo, obstáculos, nave, ballena.
        - Muestra puntuación, grafo y ruta si están activados.
        - Muestra menú de pausa si está pausado.
        - Actualiza la pantalla con pygame.display.flip().
        """
        self.screen.fill(self.settings.bg_color)
        for obstacle in self.obstacles:
            obstacle.blit()
        self.ship.blit()
        self.whale.blit()
        show_score(self)

        show_graph(self, self.settings.show_graph)
        if self.not_player == self.whale:
            show_path(self, self.whale, self.settings.show_path)
        else:
            show_path(self, self.ship, self.settings.show_path)

        if self.pause:
            show_menu(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    md = MyGame()
    md.run_game()

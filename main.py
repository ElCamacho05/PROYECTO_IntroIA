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
        pygame.init()

        # call the settings from existing settings class
        self.settings = Settings()

        # define screen settings
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()
        self.settings.show_path = False
        self.settings.show_graph = False

        # instance ship (player)
        self.ship = Ship(self)

        # instance whale
        self.whale = Whale(self)

        # player / IA
        self.player = self.ship
        self.not_player = self.whale
        self.score = 0

        # temporal for obstacle generation
        rects = [self.ship.rect, self.whale.rect]
        # define obstacles
        self.obstacles = []
        screen_range = [self.settings.screen_width - self.settings.obstacle_size[0],
                        self.settings.screen_height - self.settings.obstacle_size[1]]
        generate_obstacles(self.settings.total_obstacles, screen_range, rects, self)

        # display title
        pygame.display.set_caption("PROYECTO - IA")

        # graph generation
        print("Generando mundo")
        self.nodes, self.graph = gen_graph(self, 200)
        print("Grafo generado...")

        # pause
        self.pause = True

        # dataset
        self.set = []
        self.X = []
        self.y = []

        # stages
        self.stage = 1

        # scaler (for AI)
        self.scaler_x = StandardScaler()
        self.scaler_y = StandardScaler()
        self.model = None
        # self.parallel_training()

    def gen_dataset_legacy(self):
        X = []
        y = []

        static = []
        if self.set:
            static += [coord for pos in self.set[0]["map"] for coord in pos]
            # static += [coord for obs in self.set[0]["obstacles"] for coord in obs]

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
        X = []
        y = []

        for subset in s:
            row_x = []
            row_y = []

            for k, v in subset.items():
                if k == "map":
                    for node in v:
                        row_x += node
                # elif k == "obstacles":
                #     for obs in v:
                #         row_x += obs
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
                # "path": [nodo.pos for nodo in path]
                "path": [path[1].pos]
            }
            synthetic_set.append(new_entry)

        X_n, y_n = self.gen_dataset(synthetic_set)
        return X_n, y_n

    def gen_synthetic_samples(self, sample_count=200):
        print("generando ejemplos sinteticos")
        set_t = []

        print(len(set_t))
        while len(set_t) < sample_count:
            if len(set_t) % 10 == 0:
                print(f"{int(len(set_t)/sample_count*100)} % ")
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
                # "obstacles": [obs.rect.center for obs in self.obstacles],
                "home": whale.center,
                "goal": ship.center,
                "path": [nodo.pos for nodo in path]
            }
            set_t.append(new_entry)
        X_n, y_n = self.gen_dataset(set_t)
        print("ejemplos generados con exito")
        return X_n, y_n

    def train_AI(self):
        print("Entrenando IA...")

        scaler_x = MinMaxScaler()
        scaler_y = MinMaxScaler()

        X_n, y_n = self.gen_synthetic_samples(500)

        self.X += X_n
        self.y += y_n
        X_scaled = scaler_x.fit_transform(self.X)
        y_scaled = scaler_y.fit_transform(self.y)

        model = MLPRegressor(hidden_layer_sizes=(256, 128, 64, 32, 16), max_iter=4000)
        model.fit(X_scaled, y_scaled)

        self.ship.model = model
        self.ship.scaler_x = scaler_x
        self.ship.scaler_y = scaler_y

        print(f"Entrenamiento finalizado con {len(self.X)} ejemplos")

        return self.ship.model

    def parallel_training(self):
        def run():
            print("entrenando IA en segundo plano...")
            model = self.train_AI()
            print("IA entrenada!!!")
            return model
        self.ship.path_model = threading.Thread(target=run)
        self.ship.path_model.start()

    def run_game(self):
        # self._update_screen()
        while True:
            self._check_events()
            self._update_screen()
            if self.stage == 1:  # whale (AI) -> boat (player)
                if not self.pause:
                    if self.whale.rect.colliderect(self.ship.rect):
                        print("TE HAN ALCANZADO... moviendo a la etapa 2...")
                        self.pause = True
                        self.stage = 2

                        # dataset generation and ai training
                        self.X, self.y = self.gen_dataset(self.set)
                        self.train_AI()

                        # reset whale
                        self.whale.rect.topright = self.whale.screen_rect.topright
                        self.whale.position = list(self.whale.rect.center)

                        # reset ship
                        self.ship.rect.bottomleft = self.ship.screen_rect.bottomleft
                        self.ship.position = list(self.ship.rect.center)

                        # change speed
                        diff = self.settings.whale_speed - self.settings.ship_speed
                        self.settings.whale_speed -= diff
                        self.settings.ship_speed += diff

                        # change players character
                        self.player = self.whale
                        self.not_player = self.ship

                    self.ship.update_player(self)

                    self.whale.update_AI(self, "a*")

                    # self._update_screen()

            if self.stage == 2:  # boat (AI) -> whale (player)
                # print("entrando a la etappa 2")
                if not self.pause:
                    if self.whale.rect.colliderect(self.ship.rect):
                        print("TE HAN ALCANZADO... moviendo a la etapa 2...")
                        self.pause = True
                    # print("jugando la etapa 2")
                    self.ship.update_AI(self)
                    self.whale.update_player(self)

    def _check_events(self):
        for event in pygame.event.get():
            # keyboard/mouse events
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._chek_keydown(event)

            elif event.type == pygame.KEYUP:
                self._chek_keyup(event)

    def _chek_keydown(self, event):
        """Key presses"""
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
        """Key releases"""
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.player.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.player.moving_down = False
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player.moving_left = False
        # elif event.key == pygame.K_e:
        #     self.settings.show_graph = not self.settings.show_graph
        # elif event.key == pygame.K_r:
        #     self.settings.show_path = not self.settings.show_path

    def _update_screen(self):
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

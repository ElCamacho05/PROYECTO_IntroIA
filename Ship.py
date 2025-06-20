from PRM import d, in_collision
from utils import gen_next_route
import numpy as np

import pygame.image

import threading


class Ship:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Settings
        self.settings = game.settings

        # ship image and in screen position
        self.image = pygame.image.load('images/boat.bmp')
        self.image = pygame.transform.scale(self.image, self.settings.ship_size)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.screen_rect.bottomleft
        self.position = list(self.rect.center)

        # Keyboard events
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

        # AI scalers and model
        self.scaler_x = None
        self.scaler_y = None
        self.model = None

        # path form AI
        self.path = []
        self.path_positions = []
        self.max_path = 5
        self.move = False
        self.path_model = None
        self.path_thread = None

        # threading config
        self.recalculating = False

    def set_pos(self, position):
        self.position = position
        self.rect.center = position

    def update_player(self, game):
        obstacles = game.obstacles
        if self.moving_up and self.rect.bottom > self.settings.ship_size[1]:
            future_rect = self.rect.copy()
            future_rect.centery = self.position[1] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] -= self.settings.ship_speed
                game.score += self.settings.ship_speed

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            future_rect = self.rect.copy()
            future_rect.centery = self.position[1] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] += self.settings.ship_speed
                game.score += self.settings.ship_speed

        if self.moving_right and self.rect.right < self.screen_rect.right:
            future_rect = self.rect.copy()
            future_rect.centerx = self.position[0] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] += self.settings.ship_speed
                game.score += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            future_rect = self.rect.copy()
            future_rect.centerx = self.position[0] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] -= self.settings.ship_speed
                game.score += self.settings.ship_speed

        self.rect.center = self.position

    def gen_next_route(self, m=1):
        current_pos = self.position
        for i, node in enumerate(self.path[:min(len(self.path), m)]):
            dx = abs(node[0] - current_pos[0])
            dy = abs(node[1] - current_pos[1])
            num = max(
                int(dx / self.settings.ship_speed),
                int(dy / self.settings.ship_speed),
                1
            )
            x_arr = np.linspace(current_pos[0], node[0], num)
            y_arr = np.linspace(current_pos[1], node[1], num)
            self.path_positions += [list(par) for par in zip(x_arr, y_arr)]
            current_pos = node

    def get_vector(self, game):
        X = []
        for nodo in game.nodes:
            X += nodo.pos
        # for obs in game.obstacles:
        #     X += obs.rect.center
        # X += [node.pos for node in game.nodes]
        # X += [obs for obs in game.obstacles]
        X += self.rect.center  # home
        X += game.whale.rect.center  # goal

        return X

    def get_path_AI(self, game):
        X_input = self.get_vector(game)
        X_s = self.scaler_x.transform([X_input])

        y_s = self.model.predict(X_s)
        y = self.scaler_y.inverse_transform(y_s)[0]

        path = [self.rect.center]
        path += [(int(y[i]), int(y[i + 1])) for i in range(0, 2, 10)]  # 5 pares
        path.append(game.whale.rect.center)
        return path

    def calculate_path_async(self, game):
        def run():
            self.recalculating = True
            self.move = False
            self.path = self.get_path_AI(game)

            if self.path:
                self.current_target_index = 0
                # print("camino: ", self.path)
                self.path_positions = []
                self.gen_next_route(self.max_path)

            else:
                print("no se pudo generar una ruta")
            self.recalculating = False
            self.move = True

        self.path_thread = threading.Thread(target=run)
        self.path_thread.start()

    def update_AI(self, game):
        need_new_path = False
        if not self.path:
            need_new_path = True
            print("no hay camino")
        elif not self.path_positions:
            need_new_path = True
            print("no hay pasos")
        elif d(self.path[-1], game.player.position) > 100:
            print("muy lejos")
            need_new_path = True

        if need_new_path and not self.recalculating:
            self.path_positions = []
            self.calculate_path_async(game)

        if self.path_positions and self.move:
            print("generando paso")
            next_pos = self.path_positions.pop(0)
            if not in_collision(next_pos, game):
                print("no hay paso" if not next_pos else next_pos)
                self.set_pos(next_pos)
            else:
                self.path_positions = []

    def update_AI_legacy_1(self, game):
        need_new_path = False
        if not self.path:
            need_new_path = True
        elif not self.path_positions:
            need_new_path = True
        elif d(self.path[-1], game.player.position) > 100:
            need_new_path = True

        if need_new_path:
            self.path_positions = []
            print("Calculando camino...")
            self.path = self.get_path_AI(game)
            print(f"camino: {self.path}")

            self.gen_next_route(5)
            print("Camino calculado disponible" if self.path_positions else "no hay camino disponible")

        if self.path_positions:
            next_pos = self.path_positions.pop(0)
            print("Posiciones generadas" if next_pos else "no se pudo generar posiciones")
            self.set_pos(next_pos)

    def blit(self):
        self.screen.blit(self.image, self.rect)

import pygame.image
from Pathfinder import get_path, d
import numpy as np
import threading


class Whale:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Settings
        self.settings = game.settings

        # ship image and in screen position
        self.image = pygame.image.load('images/whale.png')
        self.image = pygame.transform.scale(self.image, self.settings.whale_size)
        self.rect = self.image.get_rect()
        self.rect.topright = self.screen_rect.topright
        self.position = list(self.rect.center)

        self.path = []
        self.max_path = 5
        self.path_positions = []
        self.current_target_index = 0

        # for threading
        self.recalculating = False
        self.path_thread = None
        self.move = False

        # Keyboard events
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def set_pos(self, position):
        self.position = position
        self.rect.center = position

    def calculate_path_async(self, game):
        def run():
            self.recalculating = True
            self.move = False
            path_nodes = get_path(game, game.whale.rect.center, game.ship.rect.center)

            if path_nodes:
                new_entry = {
                    "map": [nodo.pos[:] for nodo in game.nodes],
                    # "obstacles": [obs.rect.center[:] for obs in game.obstacles],
                    "home": game.whale.rect.center[:],
                    "goal": game.ship.rect.center[:],
                    # "path": [nodo.pos[:] for nodo in path_nodes]
                    "path": [path_nodes[1].pos]

                }
                # print(new_entry)
                game.set.append(new_entry)

                self.path = [node.pos for node in path_nodes]
                self.current_target_index = 0
                # print("camino: ", self.path)
                self.gen_next_route(self.max_path)

            else:
                print("no se pudo generar una ruta")
            self.recalculating = False
            self.move = True

        self.path_thread = threading.Thread(target=run)
        self.path_thread.start()

    def simple_pursue(self, game):
        ship = game.ship
        obstacles = game.obstacles
        if self.position[1] > ship.position[1] and self.rect.bottom > self.settings.ship_size[1]:
            future_rect = self.rect.copy()
            future_rect.y = self.position[1] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] -= self.settings.ship_speed

        elif self.position[1] < ship.position[1] and self.rect.bottom < self.screen_rect.bottom:
            future_rect = self.rect.copy()
            future_rect.y = self.position[1] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] += self.settings.ship_speed

        if self.position[0] < ship.position[0] and self.rect.right < self.screen_rect.right:
            future_rect = self.rect.copy()
            future_rect.x = self.position[0] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] += self.settings.ship_speed

        elif self.position[0] > ship.position[0] and self.rect.left > 0:
            future_rect = self.rect.copy()
            future_rect.x = self.position[0] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] -= self.settings.ship_speed

        self.set_pos(self.position)

    def move_to_pos_legacy(self):
        if not self.path or self.current_target_index >= len(self.path):
            return

        target = self.path[self.current_target_index]
        x, y = self.position
        dx = target[0] - x
        dy = target[1] - y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < 2:
            self.current_target_index += 1
            return

        dx /= dist
        dy /= dist

        speed = self.settings.whale_speed
        x += dx * speed
        y += dy * speed

        self.set_pos([x, y])

    def gen_next_route_legacy(self):
        current_pos = self.position
        meta = self.path.pop(0)

        dx = abs(meta[0] - current_pos[0])
        dy = abs(meta[1] - current_pos[1])
        num = max(
            int(dx / self.settings.whale_speed),
            int(dy / self.settings.whale_speed),
            1
        )
        x_arr = np.linspace(current_pos[0], meta[0], num)
        y_arr = np.linspace(current_pos[1], meta[1], num)
        self.path_positions += [list(par) for par in zip(x_arr, y_arr)]

    def gen_next_route(self, m=5):
        current_pos = self.position
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
            current_pos = node

    def update_AI(self, game, t="s"):
        if t == "s":
            self.simple_pursue(game)

        elif t == "a*":
            need_new_path = False
            if not self.path:
                need_new_path = True
            elif not self.path_positions:
                need_new_path = True
            elif d(self.path[-1], game.ship.position) > 100:
                need_new_path = True

            if need_new_path and not self.recalculating:
                self.path_positions = []
                self.calculate_path_async(game)

            if self.path_positions and self.move:
                next_pos = self.path_positions.pop(0)
                self.set_pos(next_pos)
            # elif self.path:
            #     self.gen_next_route()

    def update_player(self, game):
        obstacles = game.obstacles
        if self.moving_up and self.rect.bottom > self.settings.ship_size[1]:
            future_rect = self.rect.copy()
            future_rect.centery = self.position[1] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] -= self.settings.ship_speed
                game.score += self.settings.whale_speed

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            future_rect = self.rect.copy()
            future_rect.centery = self.position[1] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[1] += self.settings.ship_speed
                game.score += self.settings.whale_speed

        if self.moving_right and self.rect.right < self.screen_rect.right:
            future_rect = self.rect.copy()
            future_rect.centerx = self.position[0] + self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] += self.settings.ship_speed
                game.score += self.settings.whale_speed

        if self.moving_left and self.rect.left > 0:
            future_rect = self.rect.copy()
            future_rect.centerx = self.position[0] - self.settings.ship_speed
            if not any(future_rect.colliderect(ob.rect) for ob in obstacles):
                self.position[0] -= self.settings.ship_speed
                game.score += self.settings.whale_speed

        self.rect.center = self.position

    def update_legacy_1(self, game, t="s"):
        if t == "s":
            self.simple_pursue(game)
        elif t == "a*":
            # Recalculate path if reached the end or ship moved significantly
            # if len(self.path) == 0 or len(self.path_positions) == 0:
            # if len(self.path) == 0:
            if len(self.path_positions) == 0:
                # d_end_ship = d(game.ship.position, self.path_positions[-1])
                # if self.path_positions[-1]:
                path_nodes = get_path(game, game.whale.rect.center, game.ship.rect.center)
                self.path = path_nodes

            # if (not self.path or self.current_target_index >= len(self.path)) and not self.recalculating:
            #     self.calculate_path_async(game)

            self.gen_next_route(self.settings.whale_speed)
            next_pos = self.path_positions.pop(0)
            self.position = next_pos
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]

    def update_legacy_2(self, game, t="s"):
        if t == "s":
            self.simple_pursue(game)
        elif t == "a*":
            if not self.path or self.current_target_index >= len(self.path) or \
                    ((game.ship.position - self.path[-1][0]) ** 2 + (
                            game.ship.position - self.path[-1][1]) ** 2) ** 0.5 > 50:
                path_nodes = get_path(game, game.whale.rect.center, game.ship.rect.center)
                if path_nodes:
                    self.path = [node.pos for node in path_nodes]
                    self.current_target_index = 0
                    print("Nueva ruta generada:", self.path)
                else:
                    print("No se pudo generar una ruta")
            self.move_to_pos_legacy()
            # self.move_to_pos(game.ship.rect.center)
            # nxt = self.path.pop(0)
            # self.set_pos(nxt)

    def blit(self):
        self.screen.blit(self.image, self.rect)

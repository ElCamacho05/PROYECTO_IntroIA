import pygame.image
from random import random
from PRM import d


class Obstacle:
    def __init__(self, position, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.position = position
        self.image = pygame.image.load('images/rock.png')
        self.image = pygame.transform.scale(self.image, game.settings.obstacle_size)
        self.rect = self.image.get_rect()

        # self.rect.x = self.position[0]
        # self.rect.y = self.position[1]
        self.rect.center = self.position

    def blit(self):
        self.screen.blit(self.image, self.rect)


def generate_obstacles(total, screen_range, rects, game):
    for i in range(total):
        position = (random() * screen_range[0], random() * screen_range[1])
        obstacle = Obstacle(position, game)
        while obstacle.rect.collidelist(rects) != -1:
            position = (random() * screen_range[0], random() * screen_range[1])
            obstacle = Obstacle(position, game)
            # for r in rects:
            #     if d(position, r.center) > 50:
            #         obstacle = Obstacle(position, game)
            #     else:
            #         break
        game.obstacles.append(obstacle)
        rects.append(obstacle.rect)

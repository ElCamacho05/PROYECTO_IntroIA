import random
import pygame
import numpy as np

from Settings import Settings


class Nodo:
    def __init__(self, pos, papa=None):
        self.pos = list(pos[:])
        self.papa = papa
        self.hijos = []
        self.h = 0
        self.costo = self.papa.costo + Settings().whale_speed if self.papa else 0

    def __eq__(self, other):
        if not self or not other:
            return False
        return self.pos == other.pos

    def __lt__(self, other):
        return self.h < other.h

    def __str__(self):
        return f"[{self.pos}]"


def in_collision(pos, game):
    if pos[0] > game.screen.get_width() or pos[0] < 0 or pos[1] > game.screen.get_height() or pos[1] < 0:
        return True
    rect = pygame.Rect(0, 0, Settings().whale_size[0], Settings().whale_size[1])
    rect.center = pos
    return any(rect.colliderect(ob.rect) for ob in game.obstacles)


def trajectory_collided(node_a, node_b, obstacles, step=5):
    if not node_a or not node_b:
        return False

    settings = Settings()
    x1, y1 = node_a.pos
    x2, y2 = node_b.pos

    dx = x2 - x1
    dy = y2 - y1
    distance = (dx**2 + dy**2) ** 0.5
    steps = max(int(distance // (settings.whale_speed * step)), 1)

    for i in range(steps + 1):
        t = i / steps
        x = x1 + t * dx
        y = y1 + t * dy
        rect = pygame.Rect(0, 0, settings.whale_size[0], settings.whale_size[1])
        rect.center = (x, y)

        for ob in obstacles:
            if rect.colliderect(ob.rect):
                return True

    return False


def trajectory_collided_legacy_1(node_a, node_b, obstacles, step=5):
    if not node_a or not node_b:
        return False

    settings = Settings()

    dx = abs(node_a.pos[0] - node_b.pos[0])
    dy = abs(node_a.pos[1] - node_b.pos[1])
    num = int(dx/(settings.whale_speed * step))
    x_arr = np.linspace(node_a.pos[0], node_b.pos[0], num)
    y_arr = np.linspace(node_a.pos[1], node_b.pos[1], num)

    for i in range(num):
        rect = pygame.Rect(0, 0, settings.whale_size[0], settings.whale_size[1])
        rect.center = [x_arr[i], y_arr[i]]
        if any(rect.colliderect(ob.rect) for ob in obstacles):
            return True
    return False


def trajectory_collided_legacy_2(node_a, node_b, obstacles, step=5):
    settings = Settings()
    x1, y1 = node_a.pos
    x2, y2 = node_b.pos

    dx = x2 - x1
    dy = y2 - y1
    distance = (dx**2 + dy**2) ** 0.5

    if distance == 0:
        return False

    steps = max(int(distance // step), 1)

    for i in range(steps + 1):
        t = i / steps
        x = x1 + t * dx
        y = y1 + t * dy

        rect = pygame.Rect(0, 0, settings.whale_size[0], settings.whale_size[1])
        rect.center = (x, y)

        for ob in obstacles:
            if rect.colliderect(ob.rect):
                return True

    return False


def gen_samples(game, samples=200):
    nodes = []
    while len(nodes) != samples:
        n = Nodo([random.randint(0, game.settings.screen_width), random.randint(0, game.settings.screen_height)])
        if not in_collision(n.pos, game):
            # print(f"{int(len(nodes) / samples * 100)} % ")
            nodes.append(n)
    return nodes


def d(p_a, p_b):
    dx = p_a[0] - p_b[0]
    dy = p_a[1] - p_b[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance


def dist(node_a, node_b):
    if not node_a or not node_b:
        return float("inf")
    return d(node_a.pos, node_b.pos)


def get_nearest_neighbors(node, nodes, obstacles, k=5):
    valid_neighbors = []
    for t_n in nodes:
        if node == t_n:
            continue
        if trajectory_collided(node, t_n, obstacles):
            continue
        valid_neighbors.append((dist(node, t_n), t_n))

    # sort by distance
    valid_neighbors.sort(key=lambda x: x[0])
    return [n for _, n in valid_neighbors[:k]]


def get_nearest_node(node, nodes, obstacles):
    closest = nodes[0]
    distance = float("inf")
    for t_n in nodes:
        if node == t_n:
            continue
        if trajectory_collided(node, t_n, obstacles):
            continue
        d = dist(node, t_n)
        if d < distance:
            closest = t_n
            distance = d
    return closest


def gen_graph(game, samples=200, k=20):
    print("generando nodos...")
    nodes = gen_samples(game, samples)
    graph = {}

    print("creando enlaces...")
    for i, n in enumerate(nodes):
        neighbors = get_nearest_neighbors(n, nodes, game.obstacles, k)
        graph[i] = neighbors

        for neighbor in neighbors:
            if trajectory_collided(n, neighbor, game.obstacles):
                continue
            if neighbor not in n.hijos:
                n.hijos.append(neighbor)
                # if not neighbor.papa or dist(n, neighbor) < dist(neighbor, neighbor.papa):
                #     neighbor.papa = n
            if n not in neighbor.hijos:
                neighbor.hijos.append(n)

    return nodes, graph

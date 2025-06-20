import random
import pygame
import numpy as np

from Settings import Settings


# Clase Nodo usada para representar un punto en el grafo PRM
class Nodo:
    def __init__(self, pos, papa=None):
        self.pos = list(pos[:])        # Posición del nodo
        self.papa = papa               # Nodo padre en el camino (útil para reconstrucción de rutas)
        self.hijos = []                # Lista de nodos hijos (adyacentes en el grafo)
        self.h = 0                     # Heurística (opcional para algoritmos de búsqueda)
        self.costo = self.papa.costo + Settings().whale_speed if self.papa else 0  # Costo acumulado

    # Comparación por igualdad entre nodos (basado en la posición)
    def __eq__(self, other):
        if not self or not other:
            return False
        return self.pos == other.pos

    # Comparación por heurística, útil para estructuras de prioridad
    def __lt__(self, other):
        return self.h < other.h

    # Representación en texto del nodo
    def __str__(self):
        return f"[{self.pos}]"


# Verifica si una posición colisiona con los límites de la pantalla o con un obstáculo
def in_collision(pos, game):
    if pos[0] > game.screen.get_width() or pos[0] < 0 or pos[1] > game.screen.get_height() or pos[1] < 0:
        return True  # Está fuera del área visible
    rect = pygame.Rect(0, 0, Settings().whale_size[0], Settings().whale_size[1])
    rect.center = pos
    return any(rect.colliderect(ob.rect) for ob in game.obstacles)  # Colisión con obstáculos


# Verifica si la trayectoria entre dos nodos colisiona con algún obstáculo
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
                return True  # Hay colisión en el trayecto

    return False  # Trayectoria libre


# Genera una lista de nodos válidos (que no colisionen) dentro del mapa
def gen_samples(game, samples=200):
    nodes = []
    while len(nodes) != samples:
        n = Nodo([random.randint(0, game.settings.screen_width), random.randint(0, game.settings.screen_height)])
        if not in_collision(n.pos, game):
            nodes.append(n)
    return nodes


# Calcula la distancia euclidiana entre dos posiciones
def d(p_a, p_b):
    dx = p_a[0] - p_b[0]
    dy = p_a[1] - p_b[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance


# Calcula la distancia entre dos nodos
def dist(node_a, node_b):
    if not node_a or not node_b:
        return float("inf")
    return d(node_a.pos, node_b.pos)


# Devuelve los k vecinos más cercanos a un nodo, que no tengan colisión en el trayecto
def get_nearest_neighbors(node, nodes, obstacles, k=5):
    valid_neighbors = []
    for t_n in nodes:
        if node == t_n:
            continue
        if trajectory_collided(node, t_n, obstacles):
            continue
        valid_neighbors.append((dist(node, t_n), t_n))  # Se almacena como tupla (distancia, nodo)

    valid_neighbors.sort(key=lambda x: x[0])  # Ordenar por distancia
    return [n for _, n in valid_neighbors[:k]]  # Devolver solo los nodos


# Devuelve el nodo más cercano a un nodo dado (sin colisiones)
def get_nearest_node(node, nodes, obstacles):
    closest = nodes[0]
    distance = float("inf")
    for t_n in nodes:
        if node == t_n:
            continue
        if trajectory_collided(node, t_n, obstacles):
            continue
        d_ = dist(node, t_n)
        if d_ < distance:
            closest = t_n
            distance = d_
    return closest


# Genera el grafo PRM conectando nodos entre sí si no hay colisión en el trayecto
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
            # Conexión bidireccional
            if neighbor not in n.hijos:
                n.hijos.append(neighbor)
            if n not in neighbor.hijos:
                neighbor.hijos.append(n)

    return nodes, graph

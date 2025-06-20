from PRM import *


def get_path(game, home, goal, path_length=200):
    """
    Versión mejorada del cálculo de ruta para encontrar camino desde 'home' hasta 'goal'.
    Utiliza búsqueda A* sobre nodos pre-generados.

    Parámetros:
    - game: objeto con estado del juego.
    - home: posición inicial [x, y].
    - goal: posición objetivo [x, y].
    - path_length: longitud máxima del camino a retornar (para limitar tamaño).

    Retorna:
    - Lista de nodos que representan el camino, limitada por path_length, o lista vacía si no hay ruta.
    """

    start = Nodo(home)
    end = Nodo(goal)
    obstacles = game.obstacles
    nodes = game.nodes

    # Buscar un nodo vecino al inicio que tenga línea de visión sin colisión
    first_node_neighbors = get_nearest_neighbors(start, nodes, obstacles, k=20)

    for neighbor in first_node_neighbors:
        if not trajectory_collided(start, neighbor, obstacles):
            first_node = neighbor
            first_node.papa = start
            break
    else:
        # Si no hay nodo vecino accesible, retornar vacío
        return []

    opened = [start, first_node]
    closed = []

    # Búsqueda A* principal
    while opened:
        current = opened.pop(0)

        # Si la trayectoria de nodo actual a nodo final no colisiona, se encontró ruta
        if not trajectory_collided(current, end, obstacles):
            path = [end, current]
            parent = current.papa

            # Reconstrucción del camino
            while parent:
                path.append(parent)
                parent = parent.papa

            path.reverse()
            # Limitar longitud del camino para evitar listas muy largas
            path = path[:min(len(path), path_length)]
            return path

        if current in closed:
            continue

        # Explorar hijos vecinos
        for hijo in current.hijos:
            if hijo not in closed:
                hijo.h = dist(hijo, end)  # heurística distancia al objetivo
                hijo.papa = current
                opened.append(hijo)

        opened.sort()
        closed.append(current)

    print("No se encontró meta")
    return []

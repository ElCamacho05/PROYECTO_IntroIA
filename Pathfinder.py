from PRM import *


def get_path_legacy(game):
    i = 0
    start = Nodo(game.whale.rect.center)
    end = Nodo(game.ship.rect.center)
    obstacles = game.obstacles
    nodes = game.nodes

    first_node_neighbors = get_nearest_neighbors(start, nodes, obstacles, k=20)
    if not first_node_neighbors:
        return
    first_node = first_node_neighbors[0]
    first_node.papa = start

    opened = [start, first_node]
    closed = []

    while opened:
        if trajectory_collided(opened[0], opened[0].papa, obstacles):
            closed.append(opened.pop(0))
        n = opened.pop(0)
        if not trajectory_collided(n, end, obstacles) or n == end:

            path = [end, n]
            parent = n.papa
            print("gemerando camino... ", end="")
            while parent:
                i += 1

                path.append(parent)
                parent = parent.papa
            path.reverse()
            # path = path[0:4]
            print(f"META ENCONTRADA... retornando camino {len(path)}")
            return path

        if n in closed:
            continue

        for c in n.hijos:
            if c not in closed:
                opened.append(c)
                c.h = dist(c, end)
                c.papa = n
        opened.sort()
        closed.append(n)
    print("No se encontro meta")
    return []


def get_path(game, home, goal, path_length=200):
    # print("realizando busqueda")
    # print(game.ship.rect.center)
    # print(game.whale.rect.center)
    start = Nodo(home)
    end = Nodo(goal)
    obstacles = game.obstacles
    nodes = game.nodes

    first_node_neighbors = get_nearest_neighbors(start, nodes, obstacles, k=20)

    for neighbor in first_node_neighbors:
        if not trajectory_collided(start, neighbor, obstacles):
            first_node = neighbor
            first_node.papa = start
            break
    else:
        return []

    opened = [start, first_node]
    closed = []

    while opened:
        current = opened.pop(0)

        if not trajectory_collided(current, end, obstacles):

            path = [end, current]
            parent = current.papa

            # print("gemerando camino... ", end="")
            while parent:
                path.append(parent)
                parent = parent.papa

            path.reverse()
            # print(f"META ENCONTRADA... retornando camino {len(path)}")
            path = path[:min(len(path), path_length)]
            return path

        if current in closed:
            continue

        for hijo in current.hijos:
            if hijo not in closed:
                hijo.h = dist(hijo, end)
                hijo.papa = current
                opened.append(hijo)

        opened.sort()
        closed.append(current)

    print("No se encontro meta")
    return []


def show_path_legacy(game, on=False):
    if on and game.whale.path:
        for i, node in enumerate(game.whale.path):
            pygame.draw.circle(game.screen, (255, 0, 0), node, 3)
            if i+1 < len(game.whale.path):
                pygame.draw.line(game.screen, (255, 0, 0), node, game.whale.path[i+1], 1)


def show_path_legacy_1(game, entity, on=False):
    path = entity.path
    print(path)
    print(on)
    if on and entity.path:
        print("mostrando camino")
        for i in range(len(entity.path)):
            pos = (path[i][0], path[i][1])
            pygame.draw.circle(game.screen, (255, 0, 0), pos, 3)

            if i + 1 < len(entity.path):
                next_pos = (path[i + 1][0], path[i + 1][1])
                pygame.draw.line(game.screen, (255, 0, 0), pos, next_pos, 1)
    else:
        print("no se pudo mostrar camino")


def show_path_legacy_2(game, entity, on=False):
    path = game.not_player.path
    print(path)
    if on and game.player.path:
        print("mostrando camino")
        for i in range(len(game.player.path)):
            pos = (path[i][0], path[i][1])
            pygame.draw.circle(game.screen, (255, 0, 0), pos, 3)

            if i + 1 < len(game.player.path):
                next_pos = (path[i + 1][0], path[i + 1][1])
                pygame.draw.line(game.screen, (255, 0, 0), pos, next_pos, 1)
    else:
        print("no se pudo mostrar camino")



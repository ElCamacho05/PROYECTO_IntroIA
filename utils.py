import numpy as np
import pygame

# Genera la siguiente ruta paso a paso desde la posición actual hasta un subconjunto del camino total.
# Divide la ruta en pequeños pasos de acuerdo a la velocidad para movimiento suave.
def gen_next_route(entity, speed, m=5):
    current_pos = entity.position
    for i, node in enumerate(entity.path[:min(len(entity.path), m)]):
        dx = abs(node[0] - current_pos[0])
        dy = abs(node[1] - current_pos[1])
        num = max(
            int(dx / speed),
            int(dy / speed),
            1  # Asegura al menos un paso
        )
        # Interpola coordenadas entre el punto actual y el nodo destino
        x_arr = np.linspace(current_pos[0], node[0], num)
        y_arr = np.linspace(current_pos[1], node[1], num)

        # Agrega las posiciones interpoladas al buffer de movimiento
        entity.path_positions += [list(par) for par in zip(x_arr, y_arr)]

        # Actualiza la posición de referencia
        current_pos = node

# Actualiza la posición del objeto y su rectángulo en pantalla
def set_pos(entity, position):
    entity.position = position
    entity.rect.center = position

# Calcula distancia euclidiana entre dos puntos
def d(p_a, p_b):
    dx = p_a[0] - p_b[0]
    dy = p_a[1] - p_b[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance

# Calcula la distancia entre dos nodos (usando sus posiciones)
def dist(node_a, node_b):
    if not node_a or not node_b:
        return float("inf")  # Si alguno no es válido, retorna distancia infinita
    return d(node_a.pos, node_b.pos)

# Dibuja las conexiones del grafo en pantalla (si está activado)
def show_graph(game, on=False):
    if on:
        for node in game.nodes:
            for hijo in node.hijos:
                # Dibuja líneas entre nodos conectados
                pygame.draw.line(game.screen, (255, 255, 255), node.pos, hijo.pos, 1)
            # Dibuja los nodos como círculos
            pygame.draw.circle(game.screen, (125, 0, 125), node.pos, 3)

# Dibuja el camino calculado por la IA (si está activado)
def show_path(game, entity, on=False):
    path = entity.path
    if on and entity.path:
        for current, next_pos in zip(path, path[1:]):
            pygame.draw.circle(game.screen, (255, 0, 0), current, 3)
            pygame.draw.line(game.screen, (255, 0, 0), current, next_pos, 1)

        # Dibuja el nodo final del camino
        pygame.draw.circle(game.screen, (255, 0, 0), path[-1], 3)

# Muestra el menú de pausa con fondo semitransparente
def show_menu(screen):
    screen_width, screen_height = screen.get_size()

    # Fuente para título y controles
    title_font = pygame.font.SysFont(None, 120)
    info_font = pygame.font.SysFont(None, 36)

    # Renderiza el texto del título
    title_text = title_font.render("P A U S A", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(int(screen_width / 2), int(screen_height / 2 - 100)))

    # Texto de los controles
    controls_lines = [
        "Controles:",
        "MOVIMIENTO: W, A, S, D / UP, LEFT, DOWN, RIGHT",
        "SALIR: Q",
        "MOSTRAR MAPA: E",
        "MOSTRAR CAMINO: R"
    ]
    controls_surfs = [info_font.render(line, True, (50, 50, 50)) for line in controls_lines]

    # Calcula tamaño del cuadro de fondo
    content_width = max(title_rect.width, max(s.get_width() for s in controls_surfs)) + 80
    content_height = title_rect.height + len(controls_surfs) * 80 + 60

    # Rectángulo del menú central
    bg_rect = pygame.Rect(
        int((screen_width - content_width) / 2),
        int((screen_height - content_height) / 2),
        content_width,
        content_height
    )

    # Crea fondo blanco semitransparente
    transparent_box = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    transparent_box.fill((255, 255, 255, 150))  # Blanco con 150/255 de opacidad

    # Dibuja fondo y borde
    screen.blit(transparent_box, (bg_rect.x, bg_rect.y))
    pygame.draw.rect(screen, (0, 0, 0), bg_rect, width=3, border_radius=12)

    # Dibuja el título
    screen.blit(title_text, title_rect)

    # Dibuja cada línea de controles
    for i, surf in enumerate(controls_surfs):
        line_rect = surf.get_rect(center=(int(screen_width / 2), int(screen_height / 2 + i * 50)))
        screen.blit(surf, line_rect)

# Muestra el puntaje en la esquina superior izquierda
def show_score(game):
    screen = game.screen
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score: {int(game.score/10)}", True, (255, 255, 255))
    text_rect = text.get_rect(topleft=(10, 10))
    screen.blit(text, text_rect)

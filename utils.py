import numpy as np
import pygame


def gen_next_route(entity, speed, m=5):
    current_pos = entity.position
    for i, node in enumerate(entity.path[:min(len(entity.path), m)]):
        dx = abs(node[0] - current_pos[0])
        dy = abs(node[1] - current_pos[1])
        num = max(
            int(dx / speed),
            int(dy / speed),
            1
        )
        x_arr = np.linspace(current_pos[0], node[0], num)
        y_arr = np.linspace(current_pos[1], node[1], num)
        entity.path_positions += [list(par) for par in zip(x_arr, y_arr)]
        current_pos = node


def set_pos(entity, position):
    entity.position = position
    entity.rect.center = position


def d(p_a, p_b):
    dx = p_a[0] - p_b[0]
    dy = p_a[1] - p_b[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance


def dist(node_a, node_b):
    if not node_a or not node_b:
        return float("inf")
    return d(node_a.pos, node_b.pos)


def show_graph(game, on=False):
    if on:
        for node in game.nodes:
            for hijo in node.hijos:
                pygame.draw.line(game.screen, (255, 255, 255), node.pos, hijo.pos, 1)
                #pygame.draw.lines()
            pygame.draw.circle(game.screen, (125, 0, 125), node.pos, 3)


def show_path(game, entity, on=False):
    path = entity.path
    if on and entity.path:
        # print("mostrando camino")
        for current, next_pos in zip(path, path[1:]):
            pygame.draw.circle(game.screen, (255, 0, 0), current, 3)
            pygame.draw.line(game.screen, (255, 0, 0), current, next_pos, 1)

        pygame.draw.circle(game.screen, (255, 0, 0), path[-1], 3)


def show_menu(screen):
    screen_width, screen_height = screen.get_size()

    title_font = pygame.font.SysFont(None, 120)
    info_font = pygame.font.SysFont(None, 36)

    title_text = title_font.render("P A U S A", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(int(screen_width / 2), int(screen_height / 2 - 100)))

    controls_lines = [
        "Controles:",
        "MOVIMIENTO: W, A, S, D / UP, LEFT, DOWN, RIGHT",
        "SALIR: Q",
        "MOSTRAR MAPA: E",
        "MOSTRAR CAMINO: R"
    ]
    controls_surfs = [info_font.render(line, True, (50, 50, 50)) for line in controls_lines]

    content_width = max(title_rect.width, max(s.get_width() for s in controls_surfs)) + 80
    content_height = title_rect.height + len(controls_surfs) * 80 + 60

    bg_rect = pygame.Rect(
        int((screen_width - content_width) / 2),
        int((screen_height - content_height) / 2),
        content_width,
        content_height
    )

    transparent_box = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    transparent_box.fill((255, 255, 255, 150))  # Blanco con opacidad

    screen.blit(transparent_box, (bg_rect.x, bg_rect.y))
    pygame.draw.rect(screen, (0, 0, 0), bg_rect, width=3, border_radius=12)

    screen.blit(title_text, title_rect)

    for i, surf in enumerate(controls_surfs):
        line_rect = surf.get_rect(center=(int(screen_width / 2), int(screen_height / 2 + i * 50)))
        screen.blit(surf, line_rect)


def show_score(game):
    screen = game.screen
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score: {int(game.score/10)}", True, (255, 255, 255))
    text_rect = text.get_rect(topleft=(10, 10))
    screen.blit(text, text_rect)

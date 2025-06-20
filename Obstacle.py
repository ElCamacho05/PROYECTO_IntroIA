import pygame.image
from random import random


class Obstacle:
    """
    Clase que representa un obstáculo visual en el juego.
    Cada obstáculo tiene una posición, una imagen y un rectángulo para detectar colisiones.
    """

    def __init__(self, position, game):
        """
        Inicializa el obstáculo.

        Args:
            position (tuple): Posición (x, y) donde se colocará el obstáculo en pantalla.
            game (Game): Instancia principal del juego que contiene la pantalla y configuración.
        """
        # Referencia a la pantalla donde se dibujará el obstáculo
        self.screen = game.screen
        # Rectángulo que representa los límites de la pantalla (para posibles validaciones)
        self.screen_rect = game.screen.get_rect()

        # Guardar posición como una tupla (x, y)
        self.position = position

        # Cargar la imagen del obstáculo desde archivos (por ejemplo, una roca)
        self.image = pygame.image.load('images/rock.png')

        # Escalar la imagen al tamaño definido en la configuración del juego
        self.image = pygame.transform.scale(self.image, game.settings.obstacle_size)

        # Obtener el rectángulo que delimita la imagen para poder manipular la posición y colisiones
        self.rect = self.image.get_rect()

        # Colocar el rectángulo centrado en la posición deseada
        self.rect.center = self.position

    def blit(self):
        """
        Dibuja el obstáculo en la pantalla en su posición actual.
        """
        self.screen.blit(self.image, self.rect)


def generate_obstacles(total, screen_range, rects, game):
    """
    Genera múltiples obstáculos distribuidos aleatoriamente en la pantalla, evitando colisiones con
    otros rectángulos ya existentes.

    Args:
        total (int): Número total de obstáculos a generar.
        screen_range (tuple): Tamaño máximo (ancho, alto) del área de la pantalla donde pueden colocarse.
        rects (list): Lista de pygame.Rect de objetos ya colocados para evitar superposiciones.
        game (Game): Instancia principal del juego que contiene la pantalla y configuración.
    """
    for i in range(total):
        # Generar una posición aleatoria dentro del rango válido de pantalla
        position = (random() * screen_range[0], random() * screen_range[1])

        # Crear el obstáculo con la posición generada
        obstacle = Obstacle(position, game)

        # Mientras el obstáculo colisione con algún rectángulo existente en 'rects', buscar una nueva posición
        while obstacle.rect.collidelist(rects) != -1:
            position = (random() * screen_range[0], random() * screen_range[1])
            obstacle = Obstacle(position, game)
            # Nota: Se podría agregar lógica para evitar posiciones demasiado cercanas, comentada abajo

        # Una vez que se tiene una posición válida sin colisiones, agregar el obstáculo a la lista del juego
        game.obstacles.append(obstacle)
        # También guardar su rectángulo en la lista para futuras comprobaciones de colisión
        rects.append(obstacle.rect)

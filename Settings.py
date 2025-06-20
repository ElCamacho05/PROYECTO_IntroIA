class Settings:
    """
    Clase de configuración global para el juego.

    Esta clase contiene todos los parámetros que definen el comportamiento visual y lógico
    del juego, como las dimensiones de pantalla, la velocidad y tamaño de los objetos, y
    la visualización de rutas o gráficos.
    """

    def __init__(self):
        # 📺 Dimensiones y color de la pantalla
        self.screen_width = 1200
        """Ancho de la ventana del juego en píxeles."""

        self.screen_height = 600
        """Altura de la ventana del juego en píxeles."""

        self.bg_color = (20, 109, 218)
        """Color de fondo de la pantalla en formato RGB."""

        # 🚢 Configuración de la nave (Ship)
        self.ship_size = (25, 25)
        """Tamaño de la nave en píxeles (ancho, alto)."""

        self.ship_speed = 0.20
        """Velocidad de movimiento de la nave."""

        # 🐋 Configuración de la ballena (Whale)
        self.whale_size = (25, 25)
        """Tamaño de la ballena enemiga en píxeles (ancho, alto)."""

        self.whale_speed = 0.25
        """Velocidad de movimiento de la ballena."""

        # 🧱 Configuración de los obstáculos
        self.total_obstacles = 50
        """Cantidad total de obstáculos a generar en el mapa."""

        self.obstacle_size = (30, 30)
        """Tamaño de cada obstáculo en píxeles (ancho, alto)."""

        # 🗺️ Opciones de visualización
        self.show_graph = False
        """Indica si se debe mostrar el grafo de navegación (usado en depuración)."""

        self.show_path = False
        """Indica si se debe mostrar el camino calculado por la IA."""

        # 🕒 Control de recálculo de rutas
        self.last_path_time = 0
        """Último timestamp en milisegundos en el que se calculó un nuevo camino."""

        self.path_interval = 100
        """Intervalo de tiempo mínimo (en milisegundos) entre recalculaciones de ruta."""

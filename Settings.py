class Settings:
    def __init__(self):
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (20, 109, 218)

        # Ship settings
        self.ship_size = (25, 25)
        self.ship_speed = 0.20

        # Whale settings
        self.whale_size = (25, 25)
        self.whale_speed = 0.25

        # Obstacle settings
        self.total_obstacles = 50
        self.obstacle_size = (30, 30)

        # show graph / path
        self.show_graph = False
        self.show_path = False

        # Pathfinding interval
        self.last_path_time = 0
        self.path_interval = 100

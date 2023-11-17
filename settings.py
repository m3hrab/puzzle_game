import pygame
class Settings():
    """A class to store all settings for the game""" 

    def __init__(self) -> None:
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (255, 255, 255)

        # Grid settings
        self.grid_size = 5
        self.cell_size = 80
        self.grid_color = (0, 50, 5)
        self.grid_line_width = 2
        self.grid_top_left = (200, 50)

        self.font = pygame.font.SysFont(None, 48)

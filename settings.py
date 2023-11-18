import pygame
pygame.mixer.init()
class Settings():
    """A class to store all settings for the game""" 

    def __init__(self) -> None:
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (255, 255, 255)

        # Grid settings
        self.grid_size = 5
        self.cell_size = 60
        self.cell_gap = 2
        self.grid_color = (255, 255, 255)
        self.grid_line_width = 2
        self.grid_top_left = (250, 90)

        self.font = pygame.font.SysFont(None, 36)


        # Button settings
        self.button_font = pygame.font.SysFont(None, 24)
        self.button_sound = pygame.mixer.Sound('assets/sounds/btn.wav')



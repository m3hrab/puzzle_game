import pygame, random 

class Grid():
    def __init__(self, screen, settings) -> None:
        self.screen = screen
        self.settings = settings
        self.grid = [[0 for x in range(self.settings.grid_size)] for y in range(self.settings.grid_size)]
        self.grid[random.randint(0, self.settings.grid_size - 1)][random.randint(0, self.settings.grid_size - 1)] = 1
        self.grid_top_left = settings.grid_top_left

    def draw_grid(self):
        for x in range(self.settings.grid_size):
            for y in range(self.settings.grid_size):
                rect = pygame.Rect(self.grid_top_left[0] + x * self.settings.cell_size, 
                                   self.grid_top_left[1] + y * self.settings.cell_size, 
                                    self.settings.cell_size, 
                                    self.settings.cell_size)
                
                pygame.draw.rect(self.screen, self.settings.grid_color, rect, self.settings.grid_line_width)
                if self.grid[x][y] != 0:
                    text = self.settings.font.render(str(self.grid[x][y]), True, (255, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.center = rect.center
                    self.screen.blit(text, text_rect)
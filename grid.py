import pygame, random 

class Grid():
    def __init__(self, screen, settings) -> None:
        self.screen = screen
        self.settings = settings
        self.grid = [[None for x in range(self.settings.grid_size)] for y in range(self.settings.grid_size)]
        self.grid[random.randint(0, self.settings.grid_size - 1)][random.randint(0, self.settings.grid_size - 1)] = 1
        self.grid_top_left = ((self.settings.screen_width - self.settings.grid_size * self.settings.cell_size) // 2,
                              (self.settings.screen_height - self.settings.grid_size * self.settings.cell_size) // 2)

    def draw_grid(self):
        for x in range(self.settings.grid_size):
            for y in range(self.settings.grid_size):
                rect = pygame.Rect(self.grid_top_left[0] + x * self.settings.cell_size, 
                                   self.grid_top_left[1] + y * self.settings.cell_size, 
                                    self.settings.cell_size, 
                                    self.settings.cell_size)
                
                pygame.draw.rect(self.screen, self.settings.grid_color, rect, self.settings.grid_line_width)
                if self.grid[x][y] is not None:
                    text = self.settings.font.render(str(self.grid[x][y]), True, (255, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.center = rect.center
                    self.screen.blit(text, text_rect)
import pygame
import sys

class Button:
    def __init__(self, screen, settings, text, x, y, function=None):
        self.screen = screen
        self.settings = settings
        self.text = text
        self.x = x
        self.y = y
        self.width = 100
        self.height = 50
        self.color = (0, 255, 0)
        self.hover_color = (200, 200, 200)
        self.function = function 
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self):
        mouse = pygame.mouse.get_pos()
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            pygame.draw.rect(self.screen, self.hover_color, (self.x, self.y, self.width, self.height))
            if pygame.mouse.get_pressed()[0] and self.function is not None:
                self.function()
        else:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

        text_surface = self.settings.button_font.render(self.text, True, (0, 0, 0))
        self.screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, self.y + (self.height - text_surface.get_height()) // 2))
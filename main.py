import pygame 
import sys 
from grid import Grid
from settings import Settings
def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Number puzzle")

    grid = Grid(screen, settings)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            grid.handle_event(event)

        grid.update()
        screen.fill(settings.bg_color)
        grid.draw_grid()
        pygame.display.flip()

run_game()
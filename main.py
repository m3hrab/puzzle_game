import pygame

# Initialize pygame
pygame.init()

# Define screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Define grid size
GRID_SIZE = 5

# Calculate cell size
CELL_SIZE = 80

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_grid():
    # Calculate the top left x and y coordinates to center the grid
    top_left_x = (SCREEN_WIDTH - (CELL_SIZE * GRID_SIZE)) // 2
    top_left_y = (SCREEN_HEIGHT - (CELL_SIZE * GRID_SIZE)) // 2

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            pygame.draw.rect(screen, (255, 255, 255), (top_left_x + i * CELL_SIZE, top_left_y + j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    draw_grid()
    pygame.display.update()

pygame.quit()
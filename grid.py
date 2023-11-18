import pygame
import time
import random
import json
from button import Button

class Grid():
    def __init__(self, screen, settings) -> None:
        self.screen = screen
        self.settings = settings
        self.grid_top_left = settings.grid_top_left
        self.load_grid()
        self.selected_cell = None

        self.key_buffer = ''
        self.key_time = 0
        
        # Add two buttons to the screen
        self.save_button = Button(screen, settings, "Save", 285, 500)
        self.reset_button = Button(screen, settings, "Reset", 395, 500)



    def load_grid(self):
        """Load the grid from a file, or initialize a new one if the file doesn't exist."""
        try:
            with open('grid.txt', 'r') as f:
                self.grid = json.loads(f.read())
        except FileNotFoundError:
            self.initialize_grid()

    def initialize_grid(self):
        """Initialize a new grid with a random cell set to 1."""
        self.grid = [[0 for _ in range(self.settings.grid_size)] for _ in range(self.settings.grid_size)]
        self.grid[random.randint(0, self.settings.grid_size - 1)][random.randint(0, self.settings.grid_size - 1)] = 1

    def save(self):
        """Save the current grid to a file."""
        with open('grid.txt', 'w') as f:
            f.write(json.dumps(self.grid))

    def reset(self):
        """Reset the grid to its initial state."""
        self.initialize_grid()

    

    def update(self):
        """Update the grid based on the key buffer."""
        if self.key_buffer and time.time() - self.key_time > 0.5:  # 0.5 seconds
            number = int(self.key_buffer)
            if 1 < number < 26:
                self.grid[self.selected_cell[0]][self.selected_cell[1]] = number
            self.key_buffer = ''


    # def handle_event(self, event):
    #     """Handle a mouse button down event and keyboard events."""
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         mouse_pos = pygame.mouse.get_pos()
    #         if self.save_button.rect.collidepoint(mouse_pos):
    #             self.settings.button_sound.play()
    #             self.save()
    #         elif self.reset_button.rect.collidepoint(mouse_pos):
    #             self.settings.button_sound.play()
    #             self.reset()
    #         else:
    #             self.select_cell(mouse_pos)
            # elif event.type == pygame.KEYDOWN:
            # if self.selected_cell is not None and event.unicode.isdigit():
            #     self.settings.button_sound.play()
            #     self.key_buffer += event.unicode
            #     self.key_time = time.time()
            # else:
            #     print("Invalid keypress")

    def handle_event(self, event):
        """Handle a mouse button down event and keyboard events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_event(event)
        elif event.type == pygame.KEYDOWN:
            self.handle_keyboard_event(event)
    
    def handle_mouse_event(self, event):
        """Handle a mouse button down event."""
        mouse_pos = pygame.mouse.get_pos()
        if self.save_button.rect.collidepoint(mouse_pos):
            self.settings.button_sound.play()
            self.save()
        elif self.reset_button.rect.collidepoint(mouse_pos):
            self.settings.button_sound.play()
            self.reset()
        else:
            self.select_cell(mouse_pos)

    def handle_keyboard_event(self, event):
        """Handle keyboard events."""
        if event.key == pygame.K_BACKSPACE and self.select_cell is not None:
            self.key_buffer = ''
            self.grid[self.selected_cell[0]][self.selected_cell[1]] = 0
        elif event.key == pygame.K_RETURN:
            if self.key_buffer != '':
                number = int(self.key_buffer)
                if 1 < number < 26:
                    self.grid[self.selected_cell[0]][self.selected_cell[1]] = number
                self.key_buffer = ''
        elif event.unicode.isdigit():
            self.key_buffer += event.unicode
            self.key_time = time.time()
        else:   
            print("Invalid keypress")



    def select_cell(self, mouse_pos):
        """Select a cell based on the mouse position."""
        grid_x = (mouse_pos[0] - self.grid_top_left[0]) // self.settings.cell_size
        grid_y = (mouse_pos[1] - self.grid_top_left[1]) // self.settings.cell_size
        if 0 <= grid_x < self.settings.grid_size and 0 <= grid_y < self.settings.grid_size:
            if self.grid[grid_x][grid_y] != 1:  # Only select the cell if its value is not 1
                self.selected_cell = (grid_x, grid_y)

    def draw_grid(self):
        """Draw the grid on the screen."""
        self.draw_background()
        self.draw_cells()
        self.save_button.draw()
        self.reset_button.draw()

    def draw_background(self):
        """Draw the background of the grid."""
        bg_rect = pygame.Rect(self.grid_top_left[0]-2, self.grid_top_left[1]-2, 
                              self.settings.grid_size * self.settings.cell_size + 2, 
                              self.settings.grid_size * self.settings.cell_size + 2)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)

    def draw_cells(self):
        """Draw the cells of the grid."""
        for x in range(self.settings.grid_size):
            for y in range(self.settings.grid_size):
                rect = pygame.Rect(self.grid_top_left[0] + x * self.settings.cell_size, 
                                   self.grid_top_left[1] + y * self.settings.cell_size, 
                                    self.settings.cell_size - self.settings.cell_gap, 
                                    self.settings.cell_size - self.settings.cell_gap)
                
                # Draw the cell
                pygame.draw.rect(self.screen, self.settings.grid_color, rect)
                if self.grid[x][y] != 0:
                    self.draw_cell_text(x, y, rect)

                # Draw a highlight for the selected cell
                if self.selected_cell == (x, y):
                    pygame.draw.rect(self.screen, (255,0,0), rect, self.settings.grid_line_width)

    def draw_cell_text(self, x, y, rect):
        """Draw the text for a cell."""
        if self.grid[x][y] == 1:
            text = self.settings.font.render('1', True, (255, 0, 0))
        else:
            text = self.settings.font.render(str(self.grid[x][y]), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = rect.center
        self.screen.blit(text, text_rect)
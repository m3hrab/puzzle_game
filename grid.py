import pygame
import time
import random
import json
from button import Button

class Grid():
    def __init__(self, screen, settings) -> None:
        self.screen = screen
        self.settings = settings
        self.load_grid()
        self.selected_cell = None

        self.key_buffer = ''
        self.key_time = 0
        
        # Invalid key message
        self.invalid_key_message = ''
        self.invalid_key_time = 0
        
        self.last_selected_cell = None
        self.last_number = 1

        # Add two buttons to the screen
        self.save_button = Button(screen, settings, "Save", 285, 520)
        self.reset_button = Button(screen, settings, "Reset", 395, 520)


    def load_grid(self):
        """Load the grid and level from a file, or initialize a new one if the file doesn't exist."""
        try:
            with open('grid.txt', 'r') as f:
                save_data = json.loads(f.read())
                self.grid = save_data["grid"]
                self.level = save_data["level"]

                if self.level == 2 or self.level == 3:
                    self.settings.grid_top_left = (190, 30)
                    self.settings.grid_size = 7
                    # self.expand_grid() 
                else:
                    self.settings.grid_size = 5
                    self.settings.grid_top_left = (250, 90)


        except FileNotFoundError:
            self.initialize_grid()
            self.level = 1
            self.settings.grid_size = 5
            self.settings.grid_top_left = (250, 90)

    def initialize_grid(self):
        """Initialize a new grid with a random cell set to 1."""
        self.grid = [[0 for _ in range(self.settings.grid_size)] for _ in range(self.settings.grid_size)]
        self.grid[random.randint(0, self.settings.grid_size - 1)][random.randint(0, self.settings.grid_size - 1)] = 1


    # Save and Reset 
    def save(self):
        """Save the current grid and level to a file."""
        with open('grid.txt', 'w') as f:
            save_data = {
                "grid": self.grid,
                "level": self.level
            }
            f.write(json.dumps(save_data))


    def reset(self):
        """Reset the grid to its initial state."""
        self.level = 1
        self.settings.grid_size = 5
        self.settings.grid_top_left = (250, 90)
        self.initialize_grid()
        self.selected_cell = None
        self.save()

    def draw_next_level_button(self):
        """Draw the next level button on the screen."""
        msg = 'Level ' + str(self.level) + ' complete!'
        text = self.settings.font.render(msg, True, (0, 255, 0))
        text_rect = text.get_rect()
        text_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 - 50)

        next_level_button = Button(self.screen, self.settings, "Next level", 350, 450)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if next_level_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.level += 1
                        if self.level == 2:
                            self.settings.grid_top_left = (190, 30)
                            self.expand_grid()
                        
                        return

                self.screen.fill((255, 255, 255))
                self.screen.blit(text, text_rect)
                next_level_button.draw()
                    
            pygame.display.flip()

    # Level complete and grid expansion
    def is_level_complete(self):
        """Check if the level is complete."""
        if self.level == 1:
            for col in range(self.settings.grid_size):
                column = [row[col] for row in self.grid]
                temp = [cell for cell in column if cell != 1]
                if 0 in temp or temp != sorted(temp):
                    return False
            

            self.draw_next_level_button()
            return True  
            
        elif self.level == 2:
            # check the outer cells is not 0
            for i in range(self.settings.grid_size):
                if self.grid[0][i] == 0 or self.grid[self.settings.grid_size - 1][i] == 0 or self.grid[i][0] == 0 or self.grid[i][self.settings.grid_size - 1] == 0:
                    return False
            
            # Level 2 is complete, hide all the numbers expect 1 from the 5x5 grid
            for i in range(1,6):
                for j in range(1,6):
                    if self.grid[i][j] != 1:
                        self.grid[i][j] = 0

            self.draw_next_level_button
            return True

        elif self.level == 3:
            for i in range(1,6):
                for j in range(1,6):
                    if self.grid[i][j] == 0:
                        return False
            
            self.display_game_complete_screen()        
            
    
    def display_game_complete_screen(self):
        """Display the game complete screen."""
        self.screen.fill((255, 255, 255))
        text = self.settings.font.render('Congratulations!', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 - 50)
        self.screen.blit(text, text_rect)

        text = self.settings.font.render('You have completed all the levels.', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2)
        self.screen.blit(text, text_rect)

        # Play again button
        play_again_button = Button(self.screen, self.settings, "Play again", 350, 520)
        play_again_button.draw()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.reset()
                        return
                    
            pygame.display.flip()


            
    def expand_grid(self):
        """Expand the grid by adding a ring of empty cells around it."""
        new_grid = [[0 for _ in range(self.settings.grid_size + 2)] for _ in range(self.settings.grid_size + 2)]
        for i in range(self.settings.grid_size):
            for j in range(self.settings.grid_size):
                new_grid[i+1][j+1] = self.grid[i][j]
        self.grid = new_grid
        self.settings.grid_size += 2

        # Update grid_top_left
        self.grid_top_left = ((self.settings.screen_width - self.settings.grid_size * self.settings.cell_size) // 2,30)

    def draw_level_complete_message(self):
        """Draw the level complete message on the screen."""
        if self.is_level_complete():
            text = self.settings.font.render('Level complete!', True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.settings.screen_width // 2, 490)
            self.screen.blit(text, text_rect)

    

    def is_corner_cell(self, cell):
        """Return True if the cell is a corner cell, False otherwise."""
        return (cell[0] == 0 and cell[1] == 0) or (cell[0] == 0 and cell[1] == self.settings.grid_size - 1) or (cell[0] == self.settings.grid_size - 1 and cell[1] == 0) or (cell[0] == self.settings.grid_size - 1 and cell[1] == self.settings.grid_size - 1)
    
    def number_exists_in_inner_grid_diagonal(self, number, corner):
        """Check if a number exists in the specific diagonal of the inner 5x5 grid."""
        corner = (corner[0], corner[1])
        if corner == (0, 0):
            for i in range(1, 6):
                if self.grid[i][i] == number:
                    return True
        elif corner == (0, self.settings.grid_size - 1):
            for i in range(1, 6):
                if self.grid[i][6 - i] == number:
                    return True
        elif corner == (self.settings.grid_size - 1, 0):
            for i in range(1, 6):
                if self.grid[6 - i][i] == number:
                    return True
        elif corner == (self.settings.grid_size - 1, self.settings.grid_size - 1):
            for i in range(1, 6):
                if self.grid[6 - i][6 - i] == number:
                    return True
        return False

    def number_exists_in_inner_grid_column(self, number, column):
        """Check if a number exists in a specific column in the inner 5x5 grid."""
        for i in range(1, 6):
            if self.grid[i][column] == number:
                return True
        return False

    def number_exists_in_inner_grid_row(self, number, row):
        """Check if a number exists in a specific row in the inner 5x5 grid."""
        for i in range(1, 6):
            if self.grid[row][i] == number:
                return True
        return False
    
    def number_exists_in_row_or_column_ends(self, number):
        """Check if a number exists at either end of the row or column of a cell."""
        x, y = self.selected_cell[0], self.selected_cell[1]
        return self.grid[x][0] == number or self.grid[x][6] == number or self.grid[0][y] == number or self.grid[6][y] == number

    def number_exists_in_diagonal_ends(self, number):
        """Check if a number exists at either end of the diagonal of the grid."""
        return self.grid[0][0] == number or self.grid[0][self.settings.grid_size - 1] == number or self.grid[self.settings.grid_size - 1][0] == number or self.grid[self.settings.grid_size - 1][self.settings.grid_size - 1] == number    
    def is_inner_cell(self, cell):
        """Return True if the cell is an inner cell, False otherwise."""
        return 1 < cell[0] < self.settings.grid_size - 2 and 1 < cell[1] < self.settings.grid_size - 2

    def number_exists_in_inner_grid(self, number):
        for i in range(1, 5):
            for j in range(1,5):
                if self.grid[i][j] == number:
                    return True
        return False
    

    def update(self):
        """Update the grid based on the key buffer."""
        if self.key_buffer and time.time() - self.key_time > 0.5:  # 0.5 seconds
            number = int(self.key_buffer)
            if 1 < number < 26:
                if self.level == 2 and (self.selected_cell[0] == 0 or self.selected_cell[0] == self.settings.grid_size - 1 or self.selected_cell[1] == 0 or self.selected_cell[1] == self.settings.grid_size - 1):
                    # In level 2, outer cells accept all values between 2 and 25
                    if not self.number_exists_in_grid(number):
                        if self.number_exists_in_inner_grid_column(number,
                                                                    self.selected_cell[1]) or self.number_exists_in_inner_grid_row(number, 
                                                                    self.selected_cell[0]) or (self.is_corner_cell(self.selected_cell) and self.number_exists_in_inner_grid_diagonal(number,
                                                                                                                                                                    self.selected_cell)):
                            self.grid[self.selected_cell[0]][self.selected_cell[1]] = number
                            self.key_buffer = ''
                        else:
                            self.invalid_key_message = 'Invalid number'
                            self.invalid_key_time = time.time()
                    else:
                        self.invalid_key_message = str(number) + ' is already exists.'
                        self.invalid_key_time = time.time()


                elif self.level == 3:
                    if not self.number_exists_in_grid(number):
                        if self.is_adjacent_to_predecessor(number):
                            if self.number_exists_in_row_or_column_ends(number):
                                self.grid[self.selected_cell[0]][self.selected_cell[1]] = number
                                self.key_buffer = ''

                            elif self.number_exists_in_diagonal_ends(number):
                                self.grid[self.selected_cell[0]][self.selected_cell[1]] = number
                                self.key_buffer = ''
                            
                            else:
                                self.invalid_key_message = 'Invalid number'
                                self.invalid_key_time = time.time()
                        else:
                            self.invalid_key_message = 'Invalid number'
                            self.invalid_key_time = time.time()

                    else:
                        self.invalid_key_message = str(number) + ' is already exists.'
                        self.invalid_key_time = time.time()

                # Level 1
                else:
                    if not self.number_exists_in_grid(number):
                        if self.is_adjacent_to_predecessor(number):
                            self.grid[self.selected_cell[0]][self.selected_cell[1]] = number
                            self.key_buffer = ''
                        else:
                            self.invalid_key_message = 'Invalid location or number'
                            self.invalid_key_time = time.time()
                    else:
                        self.invalid_key_message = str(number) + ' is already exists in the grid'
                        self.invalid_key_time = time.time()

            else:
                self.invalid_key_message = 'Only numbers between 2 and 25 are allowed'
                self.invalid_key_time = time.time()
            
            self.key_buffer = ''
            
            if self.invalid_key_message and (time.time() - self.invalid_key_time > 2):
                self.invalid_key_message = ''
            elif self.selected_cell != self.last_selected_cell:
                self.last_selected_cell = self.selected_cell
                # time.sleep(0.2)  # delay before clearing the message
                self.invalid_key_message = ''


    def is_adjacent_to_predecessor(self, number):
        """Check if the selected cell is adjacent to the cell containing the predecessor number."""
        if self.level == 1:
            predecessor = number - 1
            for i in range(self.settings.grid_size):
                for j in range(self.settings.grid_size):
                    if self.grid[i][j] == predecessor:
                        return abs(self.selected_cell[0] - i) <= 1 and abs(self.selected_cell[1] - j) <= 1
            return False
        
        elif self.level == 3:
            predecessor = number - 1
            for i in range(1,6):
                for j in range(1,6):
                    if self.grid[i][j] == predecessor:
                        return abs(self.selected_cell[0] - i) <= 1 and abs(self.selected_cell[1] - j) <= 1
            return False


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

        elif event.unicode.isdigit():
            self.key_buffer += event.unicode
            self.key_time = time.time() 
            self.invalid_key_message = ''
        else:   
            self.invalid_key_message = 'Invalid keypress'
            self.invalid_key_time = time.time()


    def number_exists_in_grid(self, number):
        """Return True if the number exists in the grid, False otherwise."""

        if self.level == 1:
            for row in self.grid:
                if number in row:
                    return True
        # return False
        elif self.level == 2:
            for i in range(self.settings.grid_size):
                for j in range(self.settings.grid_size):
                    if self.level == 2 and (i == 0 or i == self.settings.grid_size - 1 or j == 0 or j == self.settings.grid_size - 1):
                        if self.grid[i][j] == number:
                            return True
                        
        elif self.level == 3:
            for i in range(1,6):
                for j in range(1,6):
                    if self.grid[i][j] == number:
                        return True
        return False
    
    def select_cell(self, mouse_pos):
        """Select a cell based on the mouse position."""
        grid_x = (mouse_pos[0] - self.settings.grid_top_left[0]) // self.settings.cell_size
        grid_y = (mouse_pos[1] - self.settings.grid_top_left[1]) // self.settings.cell_size
        if 0 <= grid_x < self.settings.grid_size and 0 <= grid_y < self.settings.grid_size:
            if self.level == 2 and 1 <= grid_x <= 5  and 1 <= grid_y <= 5:
                return
            if self.grid[grid_x][grid_y] != 1:  # Only select the cell if its value is not 1
                self.last_selected_cell = self.selected_cell
                self.selected_cell = (grid_x, grid_y)


    def draw_grid(self):
        """Draw the grid on the screen."""
        self.draw_background()
        self.draw_cells()
        self.save_button.draw()
        self.reset_button.draw()
        self.draw_invalid_key_message()
        self.draw_level_complete_message()


    def draw_background(self):
        """Draw the background of the grid."""
        bg_rect = pygame.Rect(self.settings.grid_top_left[0]-2, self.settings.grid_top_left[1]-2, 
                              self.settings.grid_size * self.settings.cell_size + 2, 
                              self.settings.grid_size * self.settings.cell_size + 2)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)

    def draw_cells(self):
        """Draw the cells of the grid."""
        for x in range(self.settings.grid_size):
            for y in range(self.settings.grid_size):
                rect = pygame.Rect(self.settings.grid_top_left[0] + x * self.settings.cell_size, 
                                self.settings.grid_top_left[1] + y * self.settings.cell_size, 
                                    self.settings.cell_size - self.settings.cell_gap, 
                                    self.settings.cell_size - self.settings.cell_gap)
                
                # Determine the cell color
                if (self.level == 2 or self.level == 3) and (x == 0 or x == self.settings.grid_size - 1 or y == 0 or y == self.settings.grid_size - 1):
                    cell_color = (0, 0, 255)  # Blue for outer cells in level 2
                    if (x == 0 and y == 0) or (x == 0 and y == self.settings.grid_size - 1) or (x == self.settings.grid_size - 1 and y == 0) or (x == self.settings.grid_size - 1 and y == self.settings.grid_size - 1):
                        cell_color = (255, 255, 0)  # Yellow for corner cells
                else:
                    cell_color = (255, 255, 255)  # White for other cells

                # Draw the cell
                pygame.draw.rect(self.screen, cell_color, rect)
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

    def draw_invalid_key_message(self):
        """Draw the invalid key message on the screen."""
        if self.invalid_key_message:
            text = self.settings.font.render(self.invalid_key_message, True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.settings.screen_width // 2, 490)
            self.screen.blit(text, text_rect)
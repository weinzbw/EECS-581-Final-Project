"""
Program Name: startscreen.py
Description: Provide a launch screen for the game
Programmer(s): Ben Weinzirl
Date Made: 10/22/2024
Date(s) Revised:
10/26/2024: Added correct button functionality, setup for savedata, and updated header comment
10/27/2024: Added title
11/5/2024: Connects to front
11/7/2024: Properly loads and deletes saves
11/16/2024: Scales button placement to window size
11/23/24: Added saving handling to pass to function
11/24/24: Added title animation
12/2/2024: Added Inventory Class Initialization
12/3/2024: Fixed Load Save
12/7/2024: Deleted "state" variable, added more states to savestate
Preconditions: No inputs or outputs
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: Creates a data.txt file that stores the save data of the user
Invariants: Start Game button loads into a new save. Load game buttons loads a previous save.
Known Faults: N/A
"""
# Imports
import pygame
import sys
import os
from front_room import front
import helper
import objects
import win_lose

pygame.font.init()
pygame.init()

clock = pygame.time.Clock()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Inconvenient Escape")

# Define colors
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Set up fonts
font = pygame.font.SysFont('Arial', 32)


# Create a function to draw a button
def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    # Button click state
    button_clicked = False

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Check if the mouse is over the button
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))

        if click[0] == 1 and not button_clicked:
            button_clicked = True  # Set flag to prevent repeated clicks
            if action is not None:
                action()

        if click[0] == 0:  # Detect mouse release to reset the flag
            button_clicked = False
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    # Render the text on the button
    button_text = font.render(text, True, BLACK)
    screen.blit(button_text, (x + (width // 2 - button_text.get_width() // 2), y + (height // 2 - button_text.get_height() // 2)))

# Function to start new game
def start_game():
    game_state = win_lose.GameState()
    file_path = "savedata.txt"

    if os.path.exists(file_path): # IF save exists
        open(file_path, "w").close() # Delete contents
    inventory = objects.Inventory()
    
    front(game_state, [0,0,0,0,0], inventory) # Start new session

# Function to load game from save
def load_save():

    game_state = win_lose.GameState()
    file_path = "savedata.txt"

    if os.path.exists(file_path): # If save exists
        savestate = helper.handle_save(file_path, game_state)
        inventory = objects.Inventory()
        i = 6 # Number of non-inventory variables stored in save
        while i < len(savestate): # Iterate through inventory
            inventory.add_item(str(savestate[i])) # Add saved items to inventory
            i += 1
        front(win_lose.GameState, savestate, inventory) # Launch saved session
    else: # If save does not exist
        inventory = objects.Inventory() 
        front(win_lose.GameState(), [0, 0, 0, 0, 0], inventory) # Start new session
        pass

# Main function
def start():
    # Stylistic choices for fonts and title
    screen.fill(WHITE)

    toptext = font.render('INCONVENIENT', True, BLACK)
    bottomtext = font.render("ESCAPE", True, BLACK)

    toptextRect = toptext.get_rect()
    bottomtextRect = bottomtext.get_rect()

    count = 0 # Set start for animation of title

    while True:
        screen.fill(WHITE)

        # Draw the button (text, x, y, width, height, inactive color, active color, action)
        screen_width, screen_height = screen.get_size()
        button_width, button_height = 200, 50

        start_button_y = screen_height // 3
        load_button_y = start_button_y + button_height + 20

        draw_button("Start Game", (screen_width - button_width) // 2, start_button_y, button_width, button_height, GRAY, DARK_GRAY, start_game)
        draw_button("Load Game", (screen_width - button_width) // 2, load_button_y, button_width, button_height, GRAY, DARK_GRAY, load_save)

        if count == 0: # Only run once
            for i in range(400): # Iterate through pixel placements
                # Move "INCONVENIENT" from left to right and "ESCAPE" from right to left
                other_side = 800 - i
                screen.fill(WHITE)
                clock.tick(150)
                toptextRect.center = (i, 50)
                bottomtextRect.center = (other_side, 80)
                screen.blit(toptext, toptextRect)
                screen.blit(bottomtext, bottomtextRect)
                pygame.display.flip()
            count += 1
        else: # AFter running once
            # Display normally
            screen.blit(toptext, toptextRect)
            screen.blit(bottomtext, bottomtextRect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

start()
"""
Program Name: main.py
Description: Provide a launch screen for the game
Programmer(s): Ben Weinzirl
Date Made: 10/22/2024
Date(s) Revised:
10/26/2024: Added correct button functionality, setup for savedata, and updated header comment
10/27/2024: Added title
11/5/2024: Connects to front
Preconditions: No inputs or outputs
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: Creates a data.txt file that stores the save data of the user
Invariants: Start Game button loads into a new save. Load game buttons loads a previous save.
Known Faults: N/A
"""

import pygame
import sys
import os
from front_room import front

pygame.init()

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

# Button click state
button_clicked = False

# Create a function to draw a button
def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    global button_clicked
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

# Define the action function to be triggered when the button is clicked
def load_save():
    file_path = "data.txt"

    if os.path.exists(file_path):
        print("File exists")
    else:
        front
        pass
# Initialize Pygame

def start():
    screen.fill(WHITE)
# Run the game loop
    text = font.render('INCONVENIENT ESCAPE', True, BLACK)

    textRect = text.get_rect()

    textRect.center = (400, 50)

    while True:
        screen.fill(WHITE)

        screen.blit(text, textRect)
        # Draw the button (text, x, y, width, height, inactive color, active color, action)
        draw_button("Start Game", 300, 150, 200, 50, GRAY, DARK_GRAY, front)
        draw_button("Load Game", 300, 250, 200, 50, GRAY, DARK_GRAY, load_save)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

start()
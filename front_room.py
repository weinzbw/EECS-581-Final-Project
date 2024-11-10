"""
Program Name: front_room.py
Description: Provide the front view of the room. Currently a template with placeholder image and object interaction.
Programmer(s): Naran Bat
Date Made: 10/26/2024
Date(s) Revised: 10/27/2024: Added placeholder image and object interaction
                 11/10/2024: Added win_lose conditions
Preconditions: Requires a JPEG image located in the same directory as the program.
Postconditions: A graphical window displaying the room background with interactive objects. Users can hover and click on objects to see visual feedback
Errors/Exceptions: No intended errors/exceptions
Side Effects: Opens a graphical Pygame window that requires user input to close.
Invariants: The screen dimensions are constant at 800x600 pixels. Interactive object areas are fixed and defined as rectangles within the room.
Known Faults:
"""

import pygame
import sys
import win_lose
import time


pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Front View")

# Load room image
room_image = pygame.image.load("front_room.jpeg") 
room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))

# Define font
font = pygame.font.SysFont(None, 36)
interaction_text = ""
interaction_time = 0

# Define objects
objects = {
    "monitor": pygame.Rect(100, 250, 100, 100),
    "printer": pygame.Rect(400, 200, 100, 100),
    "shredder": pygame.Rect(330, 410, 60, 90),
    "safe": pygame.Rect(600, 250, 100, 100)
}

# Colors
HIGHLIGHT_COLOR = (255, 255, 0)
TRANSPARENT_COLOR = (0, 0, 255, 100)

# Initialize game state
game_state = win_lose.GameState() # 1-hour timer and locked door initially

# Function to draw a transparent overlay on a rectangle
def draw_transparent_overlay(rect, color):
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA) 
    overlay.fill(color)
    screen.blit(overlay, rect.topleft)

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    # Check win/fail conditions
    status = game_state.update()
    if status == "win":
        win_lose.display_win_screen(screen)
        running = False
    elif status == "fail":
        win_lose.display_fail_screen(screen)
        running = False

    # Clear the screen and display room image
    screen.blit(room_image, (0, 0))

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Draw objects with hover effects
    for obj_name, obj_rect in objects.items():
        if obj_rect.collidepoint(mouse_pos):
            # Highlight object when hovering
            draw_transparent_overlay(obj_rect, HIGHLIGHT_COLOR + (100,))
            interaction_text = f"You are hovering over the {obj_name}."
            interaction_time = time.time()
        else:
            # Transparent overlay when not hovering
            draw_transparent_overlay(obj_rect, TRANSPARENT_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if player clicked on an object
            for obj_name, obj_rect in objects.items():
                if obj_rect.collidepoint(mouse_pos):
                    interaction_text = f"You clicked on the {obj_name}."
                    interaction_time = time.time()
                    # If the monitor is clicked, unlock the door (win condition)
                    if obj_name == "monitor":
                        game_state.unlock_door()  # Set win state

    # Check if interaction text should be cleared after 2 seconds
    if time.time() - interaction_time > 2:
        interaction_text = ""
    # Display interaction text
    text_surface = font.render(interaction_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(text_surface, text_rect)

    # Display the countdown timer
    win_lose.display_timer(screen, game_state.timer)

    # Update display and control frame rate
    pygame.display.flip()
    clock.tick(30)  # Cap the frame rate

# Quit Pygame when loop ends
pygame.quit()
sys.exit()

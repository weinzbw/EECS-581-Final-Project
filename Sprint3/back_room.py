"""
Program Name: front_room.py
Description: Provide the back view of the room. Currently a template with placeholder image and object interaction.
Programmer(s): Naran Bat
Date Made: 10/27/2024
Date(s) Revised: 10/27/2024: Added placeholder image and object interaction
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
import front_room

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Back View")

# Load room image
room_image = pygame.image.load("place_holder_back.jpeg")
room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))

# Define font
font = pygame.font.SysFont(None, 36)
interaction_text = ""

# Define objects
objects = {
    "stove": pygame.Rect(180, 260, 120, 250),
    "sink": pygame.Rect(460, 300, 120, 100),
}

# Colors
HIGHLIGHT_COLOR = (255, 255, 0)
TRANSPARENT_COLOR = (0, 0, 255, 100)
BUTTON_COLOR = (200, 0, 0)
BUTTON_HOVER_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Button for switching views
button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 60, 120, 40)

# Function to draw a transparent overlay on a rectangle
def draw_transparent_overlay(rect, color):
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    overlay.fill(color)
    screen.blit(overlay, rect.topleft)

# Main loop
def back(game_state):
    clock = pygame.time.Clock()
    running = True

    while running:
        # Clear the screen
        screen.blit(room_image, (0, 0))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw objects
        for obj_name, obj_rect in objects.items():
            if obj_rect.collidepoint(mouse_pos):
                draw_transparent_overlay(obj_rect, HIGHLIGHT_COLOR + (100,))
                interaction_text = f"You are hovering over the {obj_name}."
            else:
                draw_transparent_overlay(obj_rect, TRANSPARENT_COLOR)

        # Draw button
        button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, button_rect)
        button_text = font.render("Front View", True, TEXT_COLOR)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mouse_pos):
                    front_room.front(game_state)  # Switch to front view

        # Check win/lose conditions
        status = game_state.update()
        if status == "win":
            win_lose.display_win_screen(screen)
            running = False
        elif status == "fail":
            win_lose.display_fail_screen(screen)
            running = False

        # Display countdown timer
        win_lose.display_timer(screen, game_state.timer)

        # Update display
        pygame.display.flip()
        clock.tick(30)

# Run the back view
if __name__ == "__main__":
    game_state = win_lose.GameState()
    back(game_state)


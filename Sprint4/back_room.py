"""
Program Name: front_room.py
Description: Provide the back view of the room. Currently a template with placeholder image and object interaction.
Programmer(s): Naran Bat
Date Made: 10/27/2024
Date(s) Revised: 
10/27/2024: Added placeholder image and object interaction
11/24/2024: Added navigation
12/1/2024: Updated art
12/2/2024: Added Inventory Class Initalization. Removed left room from rotation
12/7/2024: Deleted "state" variable, added Sam's work on Task #5 for the blender, added portal and winning
Preconditions: Requires a JPEG image located in the same directory as the program.
Postconditions: A graphical window displaying the room background with interactive objects. Users can hover and click on objects to see visual feedback
Errors/Exceptions: No intended errors/exceptions
Side Effects: Opens a graphical Pygame window that requires user input to close.
Invariants: The screen dimensions are constant at 800x600 pixels. Interactive object areas are fixed and defined as rectangles within the room.
Known Faults:
"""

import pygame
import sys
import right
import front_room
import helper
from objects import Inventory
from win_lose import GameState, display_win_screen

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Back View")

# Load room image
left_image = pygame.image.load("Images/left_arrow_white.png")
right_image = pygame.image.load("Images/right_arrow_white.png")
left_image = pygame.transform.scale(left_image, (50, 50))
right_image = pygame.transform.scale(right_image, (50, 50))
leftRect = left_image.get_rect()
rightRect = right_image.get_rect()
leftRect.center = (50, 300)
rightRect.center = (750, 300)

# Define font
font = pygame.font.SysFont(None, 36)
interaction_text = ""

# Define objects
objects = {
    "fridge": pygame.Rect(80, 270, 150, 270),
    "blender": pygame.Rect(625, 200, 80, 150),
    "left": leftRect,
    "right": rightRect
}

# Colors
HIGHLIGHT_COLOR = (255, 255, 0)
TRANSPARENT_COLOR = (0, 0, 255, 100)

# Function to draw a transparent overlay on a rectangle
def draw_transparent_overlay(rect, color):
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA) 
    overlay.fill(color)
    screen.blit(overlay, rect.topleft)

# Main loop
def back(savestate, inventory):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Back Room")

    # task 5
    blender_clicked = False
    game_state = GameState()

    room_image = pygame.image.load("Images/back room.JPG")
    room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))

    if int(savestate[4]) == 1:
        room_image = pygame.image.load("Images/ExitHole.jpg") 
        room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))
    running = True
    while running:
        # Clear the screen
        screen.blit(room_image, (0, 0))
        screen.blit(left_image, leftRect)
        screen.blit(right_image, rightRect)

        if int(savestate[4]) == 1:
            objects["portal"] = pygame.Rect(300, 150, 210, 550)

        if inventory.visible:
            inventory.draw(screen)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw objects
        for obj_name, obj_rect in objects.items():
            if obj_rect.collidepoint(mouse_pos):
                # Highlight object when hovering
                draw_transparent_overlay(obj_rect, HIGHLIGHT_COLOR + (100,))  
                interaction_text = f"You are hovering over the {obj_name}."
            else:
                # Transparent object when not hovering
                draw_transparent_overlay(obj_rect, TRANSPARENT_COLOR)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if player clicked on an object
                for obj_name, obj_rect in objects.items():
                    if obj_rect.collidepoint(mouse_pos):
                        interaction_text = f"You clicked on the {obj_name}."
                        # adding functionality of task 5
                        if obj_name == "blender":
                            print("hi")
                            blender_clicked = True
                            # Print all items in the inventory
                            if inventory.items:
                                print("Inventory items:")
                                for item in inventory.items:
                                    print(f"- {item}")
                            else:
                                print("The inventory is empty.")
                        if obj_name == "portal":
                            game_state.unlock_door
                            display_win_screen(screen)
                            running = False
                        if obj_name == "right":
                            front_room.front(savestate, inventory)
                        if obj_name == "left":
                            right.right(savestate, inventory)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    helper.pause_menu(screen, font, "savedata.txt", savestate, inventory)
                if event.key == pygame.K_i:
                    inventory.toggle_visibility()
                if event.key == pygame.K_z:
                    inventory.handle_input(event)
                if event.key == pygame.K_x:
                    if blender_clicked == True:
                        inventory.handle_input(event)
                        if {"Thing 1/2", "Thing 2/2"}.issubset(inventory.selected_items):
                            savestate[4] = 1
                            objects["portal"] = pygame.Rect(300, 150, 210, 550)
                            room_image = pygame.image.load("Images/ExitHole.jpg") 
                            room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))
                            inventory.remove_item("Thing 1/2")
                            inventory.remove_item("Thing 2/2")

        # Display text
        text_surface = font.render(interaction_text, True, (0, 0, 0))
        screen.blit(text_surface, (20, 20))

        # Update display
        pygame.display.flip()
        clock.tick(30) # Cap the frame rate

    # Quit Pygame
    helper.save_state(savestate, inventory)
    pygame.quit()
    sys.exit()

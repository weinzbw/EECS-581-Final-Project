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
12/8/2024: Added interaction texts when hovering over items and removed transparent boxes
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
import win_lose

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Back View")

# Load left and right objects
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

def handle_hover(obj, savestate, inventory):
    if obj == "fridge":
        return "No time for snacking..."
    elif obj == "blender":
        return "Mixing everything into one, my favorite passtime"
    elif obj == "left":
        return "Go to the Right Room"
    elif obj == "right":
        return "Go to the Front Room"
    
# Main loop
def back(game_state, savestate, inventory):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Back Room")

    # Check win/fail conditions
    status = game_state.update()
    if status == "win":
        win_lose.display_win_screen(screen)
        running = False
    elif status == "fail":
        win_lose.display_fail_screen(screen)
        running = False

    # Initialize blender task variables
    blender_clicked = False

    # Determine room background based on savestate
    room_image = pygame.image.load("Images/back room.JPG")
    room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))

    if int(savestate[4]) == 1: # If blender task complete
        room_image = pygame.image.load("Images/ExitHole.jpg") 
        room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))

    running = True
    while running:
        # Clear the screen
        screen.blit(room_image, (0, 0))

        # Display the countdown timer
        win_lose.display_timer(screen, game_state.timer)
            
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
                interaction_text = handle_hover(obj_name, savestate, inventory)
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
                        if obj_name == "blender": # If blender clicked
                            blender_clicked = True
                        if obj_name == "portal": # If portal is clicked
                            # Game win condition
                            game_state.unlock_door
                            win_lose.display_win_screen(screen)
                            running = False
                        if obj_name == "right": # If right arrow is clicked
                            front_room.front(game_state, savestate, inventory) # Go to the front room
                        if obj_name == "left": # If left arrow is clicked
                            right.right(game_state, savestate, inventory) # Go to the right room
            elif event.type == pygame.KEYDOWN: # If a key is pressed
                if event.key == pygame.K_ESCAPE: # If ESC is pressed
                    helper.pause_menu(screen, font, "savedata.txt", game_state, savestate, inventory) # Show the pause menu
                if event.key == pygame.K_i: # If i is pressed
                    inventory.toggle_visibility() # Show or hide the inventory
                if event.key == pygame.K_z: # If z is pressed
                    inventory.handle_input(event) # Handle the input for inventory
                if event.key == pygame.K_x: # If x is pressed
                    if blender_clicked == True: # If the blender was clicked
                        inventory.handle_input(event) # Handle the input for inventory
                        if {"Thing 1/2", "Thing 2/2"}.issubset(inventory.selected_items): # If Thing 1/2 and Thing 2/2 are selected
                            savestate[4] = 1 # Portal shows up
                            # Create object for portal and update background
                            objects["portal"] = pygame.Rect(300, 150, 210, 550)
                            room_image = pygame.image.load("Images/ExitHole.jpg") 
                            room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))
                            # Remove used items
                            inventory.remove_item("Thing 1/2")
                            inventory.remove_item("Thing 2/2")

        # Display interaction text
        text_surface = font.render(interaction_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(800 // 2, 600 - 30))
        screen.blit(text_surface, text_rect)

        # Update display
        pygame.display.flip()
        clock.tick(30) # Cap the frame rate

    # Quit Pygame
    helper.save_state(game_state, savestate, inventory)
    pygame.quit()
    sys.exit()

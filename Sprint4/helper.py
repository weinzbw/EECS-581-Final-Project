"""
Program Name: helper.py
Description: Provide helper functions for PyGame objects on each screen.
Programmer(s): Ben Weinzirl, Sam Harrison, Mick Torres
Date Made: 10/23/2024
Date(s) Revised:
10/26/2024: Updated header comment
11/16/2024: Updated for Sam's portion which added sounds to objects. Added handle_save()
11/23/2024: Added Mick's pause menu addition
12/2/2024: Updated saving for Inventory Class
12/7/2024: Deleted "state" variable
Preconditions: Does not involve input or output
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: Updates objects within a room (separate file)
Invariants: An object has a unique action when clicked on
Known Faults: N/A
"""

import pygame
import sys
import front_room
from objects import Inventory
#pygame.mixer.init()  # ADDED

def handle_save(path):
    with open(path, "r") as save:
        savestate = save.read().splitlines()
        try:
            savestate[0]
            savestate[1]
            savestate[2]
            savestate[3]
            savestate[4]
        except:
            savestate = [0, 0, 0, 0, 0]

    with open(path, "w") as save:
        save.write(f"{savestate[0]}\n")
        save.write(f"{savestate[1]}\n")
        save.write(f"{savestate[2]}\n")
        save.write(f"{savestate[3]}\n")
        save.write(f"{savestate[4]}\n")
    
    return savestate

def save_state(savestate, inventory: Inventory):
    with open("savedata.txt", "w") as save:
        for line in savestate:
            save.write(str(line) + "\n")
        for item in inventory.items:
            save.write(str(f"{item}\n"))

def pause_menu(window, font, save_path, savestate, inventory):
    """Displays the pause menu and handles interactions using helper functions."""
    running = True
    menu_items = ["Load Save", "Delete Save", "Save and Exit"]
    selected_index = 0

    while running:
        # Draw menu background
        window.fill((0, 0, 0))  # Black background
        title_text = font.render("Pause Menu", True, (255, 255, 255))
        window.blit(title_text, (window.get_width() // 2 - title_text.get_width() // 2, 50))

        # Draw menu items
        for i, item in enumerate(menu_items):
            color = (255, 255, 0) if i == selected_index else (255, 255, 255)
            item_text = font.render(item, True, color)
            window.blit(item_text, (window.get_width() // 2 - item_text.get_width() // 2, 150 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    # Handle menu selection
                    if menu_items[selected_index] == "Load Save":
                        savestate[:] = handle_save(save_path)  # Reload the savestate
                        front_room.front(savestate, inventory)
                        running = False
                    elif menu_items[selected_index] == "Delete Save":
                        savestate = [0, 0, 0]  # Reset current state
                        inventory = Inventory()
                        front_room.front(savestate, inventory)
                        running = False
                    elif menu_items[selected_index] == "Save and Exit":
                        save_state(savestate, inventory)  # Save current state
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    running = False  # Exit the pause menu
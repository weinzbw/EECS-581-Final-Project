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
12/8/2024: Updated Load Save to function with all savestates and with game time
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
import win_lose

pygame.mixer.init()  # ADDED

def handle_save(path, game_state):
    with open(path, "r") as save:
        time = save.readline()
        try:
            if float(time) < 1:
                time = 5*60
        except:
            time = 5*60

        game_state.timer = win_lose.GameTimer(float(time))

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

def save_state(game_state, savestate, inventory: Inventory):
    with open("savedata.txt", "w") as save:
        save.write(str(game_state.timer.time_remaining()) + "\n")
        for line in savestate:
            save.write(str(line) + "\n")
        for item in inventory.items:
            save.write(str(f"{item}\n"))

def pause_menu(window, font, save_path, game_state, savestate, inventory):

    save_state(game_state, savestate, inventory)
    """Displays the pause menu and handles interactions using helper functions."""
    running = True
    menu_items = ["Return", "Help", "Load Save", "Delete Save", "Save and Exit"]
    selected_index = 0

    helping = False

    while running:
        # Draw menu background
        window.fill((0, 0, 0))  # Black background
        title_text = font.render("Pause Menu", True, (255, 255, 255))
        window.blit(title_text, (window.get_width() // 2 - title_text.get_width() // 2, 50))

        text = font.render("Use arrow keys and Enter", True, (255, 255, 255))
        window.blit(text, (0, 0))

        # Draw menu items
        for i, item in enumerate(menu_items):
            color = (255, 255, 0) if i == selected_index else (255, 255, 255)
            item_text = font.render(item, True, color)
            window.blit(item_text, (window.get_width() // 2 - item_text.get_width() // 2, 150 + i * 50))

        
        if helping:
            text_surface = font.render("To use an item:", True, (0, 255, 255))
            text_rect = text_surface.get_rect(center=(window.get_width() // 2, 430))
            window.blit(text_surface, (text_rect))

            text_surface = font.render("Use arrow keys to choose item. Enter to select", True, (0, 255, 255))
            text_rect = text_surface.get_rect(center=(window.get_width() // 2, 480))
            window.blit(text_surface, text_rect)

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
                    if menu_items[selected_index] == "Return":
                        running = False
                    if menu_items[selected_index] == "Load Save":
                        savestate[:] = handle_save(save_path, game_state)  # Reload the savestate
                        front_room.front(game_state, savestate, inventory)
                        running = False
                    elif menu_items[selected_index] == "Delete Save":
                        savestate = [0, 0, 0, 0, 0]  # Reset current state
                        inventory = Inventory()
                        game_state.timer = win_lose.GameTimer(5*60)
                        front_room.front(game_state, savestate, inventory)
                        running = False
                    elif menu_items[selected_index] == "Save and Exit":
                        save_state(game_state, savestate, inventory)  # Save current state
                        pygame.quit()
                        sys.exit()
                    elif menu_items[selected_index] == "Help":
                        helping = not helping
                        
                elif event.key == pygame.K_ESCAPE:
                    running = False  # Exit the pause menu
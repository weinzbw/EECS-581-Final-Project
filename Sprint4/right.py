"""
Program Name: right.py
Description: Right view of the escape room with interactive elements over a single background image.
Programmer(s): Mick Torres
Date Made:10/27/2024
Date(s) Revised:
11/24/2024: Added navigation
12/1/2024: Updated art
12/3/2024: Updated Hotspots
12/7/2024: Deleted "state" variable
12/8/2024: Updated to include timer and interaction text when hovering over objects
Preconditions: No inputs or outputs
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: None
Invariants: None
Known Faults: Keyboard Key sometimes doesn't go away after relaunch. Calling this module moves the windowed screen
"""

import pygame
import helper
import objects
import sys
import time
import front_room
import back_room
from objects import Inventory
import win_lose

# Initialize Pygame if not already initialized
pygame.init()
pygame.mixer.init()

font = pygame.font.SysFont(None, 36)
interaction_text = ""

# Load iamges
left_image = pygame.image.load("Images/left_arrow_white.png")
right_image = pygame.image.load("Images/right_arrow_white.png")
left_image = pygame.transform.scale(left_image, (50, 50))
right_image = pygame.transform.scale(right_image, (50, 50))
leftRect = left_image.get_rect()
rightRect = right_image.get_rect()
leftRect.center = (50, 300)
rightRect.center = (750, 300)

# def draw_transparent_overlay(rect, color, screen):
#     overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA) 
#     overlay.fill(color)
#     screen.blit(overlay, rect.topleft)
#     screen.blit(left_image, leftRect)
#     screen.blit(right_image, rightRect)

# Define interactive hotspots with click detection
class Hotspot:
    def __init__(self, x, y, width, height, action, hover):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.hover = hover

    def handle_click(self, pos, game_state, savestate, inventory):
        if self.rect.collidepoint(pos): # Check if the object was clicked
            self.action(game_state, savestate, inventory) # Do its specified action

# Actions for each hotspot
def dresser_action(game_state, savestate, inventory):
    drawer_sound = pygame.mixer.Sound("sounds/drawer.mp3")
    if savestate[1] == "1" and "Extremely Tiny Crowbar" not in inventory.items and not "Keybaord Key" in inventory.items: # If the dresser is open and the Extremely Tiny Crowbar nor Keyboard Key are not in the inventory
        drawer_sound.play()
        inventory.add_item("Extremely Tiny Crowbar")

def safe_action(game_state, savestate, inventory):
    if "Keyboard Key" in inventory.selected_items: # If the user has the Keyboard Key
        savestate[2] = 1 # The safe is open
        inventory.remove_item("Keyboard Key")
        inventory.selected_items = set()
    elif int(savestate[2]) == 1 and "Thing 1/2" not in inventory.items: # If the safe is open and the Thing 1/2 has not been collected
        inventory.add_item("Thing 1/2")

def left_action(game_state, savestate, inventory):
    front_room.front(game_state, savestate, inventory) # Go to the Front Room

def right_action(game_state, savestate, inventory):
    back_room.back(game_state, savestate, inventory) # Go to the Back Room

# Hover text for each object
def dresser_hover(game_state, savestate, inventory):
    if int(savestate[1]) == 1: # If chess has been completed
        return "Unlocked through the power of chess!"
    else:
        return "Locked"

def safe_hover(game_state, savestate, inventory):
    if int(savestate[2]) == 1: # If the safe has been opened
        if int(savestate[4]) == 0 and not "Thing 1/2" in inventory.items: # If the game has not been completed and the user does not have Thing 1/2
            return "There's a thing in here!"
        else:
            return "I really thought there would be cash in here"
    else:
        return "I've never seen a safe with a square keyhole before..."

def left_hover(game_state, savestate, inventory):
    return "Go to the Front Room"

def right_hover(game_state, savestate, inventory):
    return "Go to the Back Room"
    


class RightRoom(objects.Room):
    def __init__(self):
        super().__init__()
        # Define hotspots for each item (coordinates and sizes are placeholders based on image layout)
        self.hotspots = [
            Hotspot(80, 400, 130, 100, dresser_action, dresser_hover),  # Dresser
            Hotspot(550, 450, 120, 100, safe_action, safe_hover),      # Safe area
            Hotspot(leftRect.left, leftRect.top, leftRect.width, leftRect.height, left_action, left_hover),
            Hotspot(rightRect.left, rightRect.top, rightRect.width, rightRect.height, right_action, right_hover)
        ]

    def draw(self, surface, image):
        # Draw the background
        surface.blit(image, (0, 0))

    def handle_click(self, pos, game_state, savestate, inventory):
        for hotspot in self.hotspots:
            hotspot.handle_click(pos, game_state, savestate, inventory)

# Main function to display the front room, compatible with main.py
def right(game_state, savestate, inventory):

    interaction_time = 0

    # Load images for items
    crowbar = pygame.image.load("Images/Crowbar.png")
    crowbar = pygame.transform.scale(crowbar, (25, 25))
    thing1 = pygame.image.load("Images/Thing1.png")
    thing1 = pygame.transform.scale(thing1, (50, 50))

    # Find apt background based on savestate
    background_image = pygame.image.load('Images/right room.JPG')
    background_image = pygame.transform.scale(background_image, (800, 600))
    if int(savestate[1]) > 0: # Check if chess is complete
        background_image = pygame.image.load('Images/RightRoomOpenDresser.jpg')
        background_image = pygame.transform.scale(background_image, (800, 600))
        if int(savestate[2]) == 1: # Check if the safe is open
            background_image = pygame.image.load('Images/RightSafeOpen.jpg')
            background_image = pygame.transform.scale(background_image, (800, 600))

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Right Room")
    right_room_instance = RightRoom()

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((255, 255, 255))

        if int(savestate[2]) == 1: # If the safe is open
            background_image = pygame.image.load('Images/RightSafeOpen.jpg')
            background_image = pygame.transform.scale(background_image, (800, 600))

        # Draw the room and arrows
        right_room_instance.draw(screen, background_image)

        screen.blit(left_image, leftRect)
        screen.blit(right_image, rightRect)

        if not "Thing 1/2" in inventory.items and int(savestate[4]) == 0 and int(savestate[2]) == 1: # If the user has not collected Thing 1 and the game is not complete and the safe is open
            screen.blit(thing1, (600, 480)) # Draw Thing 1
        
        if int(savestate[1]) == 1 and not ("Extremely Tiny Crowbar" in inventory.items or "Keyboard Key" in inventory.items or "Thing 1/2" in inventory.items): # If the crowbar has not been collected and the dresser is open
            screen.blit(crowbar, (165, 460)) # Draw the Crowbar

        
        # Check if interaction text should be cleared after 2 seconds
        if time.time() - interaction_time > 2:
            interaction_text = ""
        # Display interaction text
        text_surface = font.render(interaction_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(800 // 2, 600 - 30))
        screen.blit(text_surface, text_rect)

        # Display the countdown timer
        win_lose.display_timer(screen, game_state.timer)

        # Check win/fail conditions
        status = game_state.update()
        if status == "win":
            win_lose.display_win_screen(screen)
            running = False
        elif status == "fail":
            win_lose.display_fail_screen(screen)
            running = False

        if inventory.visible:
            inventory.draw(screen)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Create interaction_text for hovering over items
        for hotspot in right_room_instance.hotspots:
            if hotspot.rect.collidepoint(mouse_pos):
                interaction_text = hotspot.hover(game_state, savestate, inventory)
                interaction_time = time.time()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                helper.save_state(game_state, savestate, inventory)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                right_room_instance.handle_click(mouse_pos, game_state, savestate, inventory)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    helper.pause_menu(screen, font, "savedata.txt", game_state, savestate, inventory)
                if event.key == pygame.K_i:
                    inventory.toggle_visibility()
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN: # If up or down arrows are pressed
                    inventory.handle_input(event) # Handle the input for inventory
                if event.key == pygame.K_RETURN: # If Enter is pressed
                    inventory.handle_input(event) # Handle the input for inventory
                    if len(inventory.selected_items) > 1:
                        inventory.selected_items = set()


        # Check if interaction text should be cleared after 2 seconds
        if time.time() - interaction_time > 2:
            interaction_text = ""
        # Display interaction text
        text_surface = font.render(interaction_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(800 // 2, 600 - 30))
        screen.blit(text_surface, text_rect)

        pygame.display.update()
        clock.tick(30)  # Cap the frame rate
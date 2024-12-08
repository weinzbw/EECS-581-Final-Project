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
Preconditions: No inputs or outputs
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: None
Invariants: None
Known Faults: Hitboxes for clicks is off. Need different background
"""

import pygame
import helper
import objects
import sys
import front_room
import back_room
from objects import Inventory

# Initialize Pygame if not already initialized
pygame.init()

font = pygame.font.SysFont(None, 36)

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
    def __init__(self, x, y, width, height, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def handle_click(self, pos, savestate, inventory):
        if self.rect.collidepoint(pos):
            self.action(savestate, inventory)

# Actions for each hotspot
def monitor_action(savestate, inventory):
    print("Monitor clicked! Display possible information or clues.")

def printer_action(savestate, inventory):
    print("Printer clicked! Perhaps it prints something useful.")

def dresser_action(savestate, inventory):
    if savestate[1] == "1" and "Extremely Tiny Crowbar" not in inventory.items:
        inventory.add_item("Extremely Tiny Crowbar")
    else:
        print("Dresser clicked! Maybe it hides something inside.")

def safe_action(savestate, inventory):
    print("Safe clicked! Requires a code to open.")

def left_action(savestate, inventory):
    front_room.front(savestate, inventory)

def right_action(savestate, inventory):
    back_room.back(savestate, inventory)

class RightRoom(objects.Room):
    def __init__(self):
        super().__init__()
        # Define hotspots for each item (coordinates and sizes are placeholders based on image layout)
        self.hotspots = [
            # Hotspot(100, 200, 150, 100, monitor_action),  # Monitor area
            # Hotspot(300, 180, 100, 150, printer_action),  # Printer area
            Hotspot(80, 400, 130, 100, dresser_action),  # Dresser
            Hotspot(550, 450, 120, 100, safe_action),      # Safe area
            Hotspot(leftRect.left, leftRect.top, leftRect.width, leftRect.height, left_action),
            Hotspot(rightRect.left, rightRect.top, rightRect.width, rightRect.height, right_action)
        ]

    def draw(self, surface, image):
        # Draw the background
        surface.blit(image, (0, 0))

    def handle_click(self, pos, savestate, inventory):
        for hotspot in self.hotspots:
            hotspot.handle_click(pos, savestate, inventory)

# Main function to display the front room, compatible with main.py
def right(savestate, inventory):

    background_image = pygame.image.load('Images/right room.JPG')
    background_image = pygame.transform.scale(background_image, (800, 600))
    if savestate[1] == "1": # Check if chess is complete
        if savestate[2] == "1":
            background_image = pygame.image.load('Images/RightSageOpen.jpg')
        background_image = pygame.image.load('Images/RightRoomOpenDresser.jpg')
        background_image = pygame.transform.scale(background_image, (800, 600))

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Right Room")
    right_room_instance = RightRoom()

    running = True
    while running:
        screen.fill((255, 255, 255))
        right_room_instance.draw(screen, background_image)
        screen.blit(left_image, leftRect)
        screen.blit(right_image, rightRect)

        if inventory.visible:
            inventory.draw(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                helper.save_state(savestate, inventory)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                right_room_instance.handle_click(pos, savestate, inventory)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    helper.pause_menu(screen, font, "savedata.txt", savestate, inventory)
                if event.key == pygame.K_i:
                    inventory.toggle_visibility()

        pygame.display.update()
"""
Program Name: left.py
Description: Left view of the escape room with interactive elements over a single background image.
Programmer(s): Mick Torres
Date Made: 10/27/2024
Date(s) Revised:
11/24/2024: Added navigation
Preconditions: No inputs or outputs
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: None
Invariants: None
Known Faults: Hitbox for clicks is off. Need different background
"""

import pygame
import helper
import objects
import sys
import back_room
import front_room

# Initialize Pygame if not already initialized
pygame.init()

font = pygame.font.SysFont(None, 36)

# Load the background image for the front room
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (800, 600))
left_image = pygame.image.load("Images/left_arrow_white.png")
right_image = pygame.image.load("Images/right_arrow_white.png")
left_image = pygame.transform.scale(left_image, (50, 50))
right_image = pygame.transform.scale(right_image, (50, 50))
leftRect = left_image.get_rect()
rightRect = right_image.get_rect()
leftRect.center = (50, 300)
rightRect.center = (750, 300)

# Define interactive hotspots with click detection
class Hotspot:
    def __init__(self, x, y, width, height, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def handle_click(self, pos, savestate, inventory, state):
        if self.rect.collidepoint(pos):
            self.action(savestate, inventory, state)

# Actions for each hotspot
def monitor_action(savestate, inventory, state):
    print("Monitor clicked! Display possible information or clues.")

def printer_action(savestate, inventory, state):
    print("Printer clicked! Perhaps it prints something useful.")

def shredder_action(savestate, inventory, state):
    print("Shredder clicked! Maybe it hides something inside.")

def safe_action(savestate, inventory, state):
    print("Safe clicked! Requires a code to open.")

def left_action(savestate, inventory, state):
    back_room.back(savestate, inventory, state)

def right_action(savestate, inventory, state):
    front_room.front(savestate, inventory, state)
# Define the front room
class LeftRoom(objects.Room):
    def __init__(self):
        super().__init__()
        # Define hotspots for each item (coordinates and sizes are placeholders based on image layout)
        self.hotspots = [
            Hotspot(100, 200, 150, 100, monitor_action),  # Monitor area
            Hotspot(300, 180, 100, 150, printer_action),  # Printer area
            Hotspot(350, 450, 100, 100, shredder_action),  # Shredder area
            Hotspot(500, 250, 120, 100, safe_action),      # Safe area
            Hotspot(leftRect.left, leftRect.top, leftRect.width, leftRect.height, left_action),
            Hotspot(rightRect.left, rightRect.top, rightRect.width, rightRect.height, right_action)
        ]

    def draw(self, surface):
        # Draw the background
        surface.blit(background_image, (0, 0))

    def handle_click(self, pos, savestate, inventory, state):
        for hotspot in self.hotspots:
            hotspot.handle_click(pos, savestate, inventory, state)

def left(savestate, inventory, state):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Left Room")
    left_room_instance = LeftRoom()

    while True:
        screen.fill((255, 255, 255))
        left_room_instance.draw(screen)
        screen.blit(left_image, leftRect)
        screen.blit(right_image, rightRect)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                helper.save_state(savestate, inventory, state)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                left_room_instance.handle_click(pos, savestate, inventory, state)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    helper.pause_menu(screen, font, "savedata.txt", savestate, inventory, state)

        pygame.display.update()
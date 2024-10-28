"""
Program Name: left.py
Description: Left view of the escape room with interactive elements over a single background image.
Programmer(s): Mick Torres
Date Made: 10/27/2024
Preconditions: No inputs or outputs
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: None
Invariants: None
Known Faults: Hitbox for clicks is off. Need different background
"""

import pygame
import helper
import sys

# Initialize Pygame if not already initialized
pygame.init()

# Load the background image for the front room
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (800, 600))

# Define interactive hotspots with click detection
class Hotspot:
    def __init__(self, x, y, width, height, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

# Actions for each hotspot
def monitor_action():
    print("Monitor clicked! Display possible information or clues.")

def printer_action():
    print("Printer clicked! Perhaps it prints something useful.")

def shredder_action():
    print("Shredder clicked! Maybe it hides something inside.")

def safe_action():
    print("Safe clicked! Requires a code to open.")

# Define the front room
class LeftRoom(helper.Room):
    def __init__(self):
        super().__init__()
        # Define hotspots for each item (coordinates and sizes are placeholders based on image layout)
        self.hotspots = [
            Hotspot(100, 200, 150, 100, monitor_action),  # Monitor area
            Hotspot(300, 180, 100, 150, printer_action),  # Printer area
            Hotspot(350, 450, 100, 100, shredder_action),  # Shredder area
            Hotspot(500, 250, 120, 100, safe_action)      # Safe area
        ]

    def draw(self, surface):
        # Draw the background
        surface.blit(background_image, (0, 0))

    def handle_click(self, pos):
        for hotspot in self.hotspots:
            hotspot.handle_click(pos)

def left():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Left Room")
    left_room_instance = LeftRoom()

    while True:
        screen.fill((255, 255, 255))
        left_room_instance.draw(screen)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                left_room_instance.handle_click(pos)

        pygame.display.update()

if __name__ == "__main__":
    left()

"""
Program Name: helper.py
Description: Provide helper functions for PyGame objects on each screen.
Programmer(s): Ben Weinzirl
Date Made: 10/23/2024
Date(s) Revised:
Preconditions:
Postconditions:
Errors/Exceptions:
Side Effects:
Invariants:
Known Faults:
"""

import pygame
import sys

class Room:
    def __init__(self):
        self.objects = []
    
    def add_object(self, obj):
        self.objects.append(obj)
    
    def remove_object(self, obj):
        self.objects.remove(obj)
    
    def update(self):
        pass
    
    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

    def handle_click(self, pos):
        for obj in self.objects:
            if obj.rect.collidepoint(pos):
                obj.handle_click()

class GameObject:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        pass

    def handle_click(self):
        pass
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

"""
Example of adding subclasses to the GameObject class to specialize handle_click():

class Button(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def handle_click(self):
        print("Button clicked! Performing button-specific action.")
"""
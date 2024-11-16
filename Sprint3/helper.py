"""
Program Name: helper.py
Description: Provide helper functions for PyGame objects on each screen.
Programmer(s): Ben Weinzirl, Sam Harrison
Date Made: 10/23/2024
Date(s) Revised:
10/26/2024: Updated header comment
11/16/2024: Updated for Sam's portion which added sounds to objects. Added handle_save()
Preconditions: Does not involve input or output
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: Updates objects within a room (separate file)
Invariants: An object has a unique action when clicked on
Known Faults: N/A
"""

import pygame
import sys

pygame.mixer.init()  # ADDED

def handle_save(path):
    with open(path, "r") as save:
        savestate = save.read().splitlines()
        try:
            savestate[0]
            savestate[1]
        except:
            savestate = [0, 0]

    with open(path, "w") as save:
        save.write(f"{savestate[0]}\n")
        save.write(f"{savestate[1]}\n")
    
    return savestate


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
    def __init__(self, x, y, image, sound=None):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.sound = sound  # ADDED
    
    def update(self):
        pass

    def handle_click(self):
        if self.sound:
            self.sound.play()  # ADDED

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def load_sound(file_path):  # ADDED
        try:
            return pygame.mixer.Sound(file_path)  # ADDED
        except pygame.error as e:  # ADDED
            print(f"Failed to load sound: {file_path}, Error: {e}")  # ADDED
            return None  # ADDED

"""
Example of adding subclasses to the GameObject class to specialize handle_click():

class Button(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def handle_click(self):
        print("Button clicked! Performing button-specific action.")
"""
# Program Name: helper.py
# Code Artifact 14
# Description: Provide helper functions for PyGame objects on each screen.
# Programmer(s): Ben Weinzirl and Sam Harrison
# Date Made: 10/23/2024
# Date(s) Revised: 10/26/2024: Updated header comment; 11/10/24: Added sound functionality
# Preconditions: Does not involve input or output
# Postconditions: No differing return values
# Errors/Exceptions: No intended errors/exceptions
# Side Effects: Updates objects within a room (separate file)
# Invariants: An object has a unique action when clicked on
# Known Faults: N/A

import pygame
import sys

pygame.mixer.init() # initializes mixer for audio

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
    def __init__(self, x, y, image, sound = None):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.sound = sound # sounds can be saved for each object

    def update(self):
        pass

    def handle_click(self):
        if self.sound:
            self.sound.play() # plays the sound for said object when clicked

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

def load_sound(file_path): # loads a sound file
    try:
        return pygame.mixer.Sound(file_path) # sound is successfully loaded
    # the sound couldn't be loaded
    except pygame.error as e:
        print(f"Failed to load sound: {file_path}, Error: {e}")
        return None 

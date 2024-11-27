"""
Program Name: objects.py
Description: Provide classes for GameObjects on each Room.
Programmer(s): Ben Weinzirl
Date Made: 11/27/2024
Date(s) Revised: N/A
Preconditions: Does not involve input or output
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: Updates objects within a room (separate file)
Invariants: An object has a unique action when clicked on
Known Faults: N/A
"""
import pygame

pygame.mixer.init()  # ADDED

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
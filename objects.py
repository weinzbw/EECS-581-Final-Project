"""
Program Name: objects.py
Description: Provide classes for GameObjects on each Room.
Programmer(s): Ben Weinzirl, Sam Harrison
Date Made: 11/27/2024
Date(s) Revised:
12/02/2024 - Added Inventory from Sam
Preconditions: Does not involve input or output
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: Updates objects within a room (separate file)
Invariants: An object has a unique action when clicked on
Known Faults: N/A
"""
import pygame

#pygame.mixer.init()  # ADDED

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

class Inventory:
    def __init__(self, items=None, font_size=24, padding=10):
        self.items = items if items else []
        self.visible = False
        self.font_size = font_size
        self.padding = padding

    def toggle_visibility(self):
        self.visible = not self.visible

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def calculate_dimensions(self):
        height = max(len(self.items) * (self.font_size + self.padding), 50) + 40 
        return 200, height

    def draw(self, screen):
        if not self.visible:
            return

        width, height = self.calculate_dimensions()
        inventory_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        inventory_surface.fill((0, 0, 0, 180))

        font = pygame.font.SysFont("Courier New", self.font_size)
        title_text = font.render("Inventory:", True, (255, 255, 255))
        inventory_surface.blit(title_text, (10, 10))

        y_offset = 40
        for item in self.items:
            font_size = self.font_size
            temp_font = pygame.font.SysFont("Courier New", font_size)
            item_text = temp_font.render(item, True, (255, 255, 255))
            while item_text.get_width() > width - 20 and font_size > 8: 
                font_size -= 1
                temp_font = pygame.font.SysFont("Courier New", font_size)
                item_text = temp_font.render(item, True, (255, 255, 255))
            inventory_surface.blit(item_text, (10, y_offset))
            y_offset += font_size + self.padding

        screen.blit(inventory_surface, (screen.get_width() - width - 20, 20))

"""
Example of adding subclasses to the GameObject class to specialize handle_click():

class Button(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def handle_click(self):
        print("Button clicked! Performing button-specific action.")
"""
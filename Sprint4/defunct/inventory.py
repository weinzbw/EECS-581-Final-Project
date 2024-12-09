# Inventory
# Code Artifact 8
# It's simple copy of the tasks.py for the inventory using the code in main.py.
# Name: Sam Harrison
# Creation Date: 11/24/24
# Preconditions: N/A
# Postconditions: N/A
# Error & Exceptions: N/A
# Side Effects: N/A
# Invariants: N/A
# Faults: N/A
import pygame

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

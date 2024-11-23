"""
Program Name: helper.py
Description: Provide helper functions for PyGame objects on each screen.
Programmer(s): Ben Weinzirl, Sam Harrison, Mick Torres
Date Made: 10/23/2024
Date(s) Revised:
10/26/2024: Updated header comment
11/16/2024: Updated for Sam's portion which added sounds to objects. Added handle_save()\
11/23/2024: Added Mick's pause menu addition
Preconditions: Does not involve input or output
Postconditions: No differing return values
Errors/Exceptions: No intended errors/exceptions
Side Effects: Updates objects within a room (separate file)
Invariants: An object has a unique action when clicked on
Known Faults: N/A
"""

import pygame
import sys
import front_room
#pygame.mixer.init()  # ADDED

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

def save_state(savestate, inventory, state):
    with open("savedata.txt", "w") as save:
        for line in savestate:
            save.write(str(line) + "\n")
        for item in inventory:
            if item not in state:
                save.write(str(f"{item}\n"))
                state.append(item)

def pause_menu(window, font, save_path, savestate, inventory, state):
    """Displays the pause menu and handles interactions using helper functions."""
    running = True
    menu_items = ["Load Save", "Delete Save", "Save and Exit"]
    selected_index = 0

    while running:
        # Draw menu background
        window.fill((0, 0, 0))  # Black background
        title_text = font.render("Pause Menu", True, (255, 255, 255))
        window.blit(title_text, (window.get_width() // 2 - title_text.get_width() // 2, 50))

        # Draw menu items
        for i, item in enumerate(menu_items):
            color = (255, 255, 0) if i == selected_index else (255, 255, 255)
            item_text = font.render(item, True, color)
            window.blit(item_text, (window.get_width() // 2 - item_text.get_width() // 2, 150 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    # Handle menu selection
                    if menu_items[selected_index] == "Load Save":
                        savestate[:] = handle_save(save_path)  # Reload the savestate
                        front_room.front(savestate, inventory, state)
                        running = False
                    elif menu_items[selected_index] == "Delete Save":
                        savestate = [0, 0]  # Reset current state
                        save_state(savestate, inventory, state)
                        running = False
                    elif menu_items[selected_index] == "Save and Exit":
                        save_state(savestate, inventory, state)  # Save current state
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    running = False  # Exit the pause menu

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
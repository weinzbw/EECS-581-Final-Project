# Task 5
# Code Artifact 20
# It's a simple file to implement the task 5.
# Name: Sam Harrison
# Creation Date: 11/24/24
# Preconditions: N/A
# Postconditions: N/A
# Error & Exceptions: N/A
# Side Effects: N/A
# Invariants: N/A
# Faults: N/A
import pygame
import time
from inventory import Inventory
from tasks import Tasks
from helper import load_sound

correct_sound = load_sound("test_1.mp3")
incorrect_sound = load_sound("test_2.mp3")

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stand Mixer Game")

stand_mixer_image = pygame.image.load("Images/stand_mixer.jpg")
stand_mixer_rect = stand_mixer_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

inventory = Inventory(items=["Long Item Name Test", "Ex 1", "Ex 2", "Ex 3"])

tasks = Tasks(tasks=["Long Task Name Test", "Ex 1", "Ex 2", "Ex 3"])

selecting_items = False
selected_items = []
wrong_items_popup_time = None
correct_items_popup_time = None

def draw_select_prompt():
    font = pygame.font.SysFont("Courier New", 24)
    text = font.render("Select 3 Items", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))

def draw_popup(message, color):
    font = pygame.font.SysFont("Courier New", 24)
    popup_text = font.render(message, True, WHITE)
    popup_background = pygame.Surface((popup_text.get_width() + 20, popup_text.get_height() + 10))
    popup_background.fill(color)
    popup_background.blit(popup_text, (10, 5))
    screen.blit(popup_background, (SCREEN_WIDTH // 2 - popup_background.get_width() // 2, 20))

def main():
    global selecting_items, selected_items, wrong_items_popup_time, correct_items_popup_time
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inventory.toggle_visibility()
                elif event.key == pygame.K_t:
                    tasks.toggle_visibility()
                elif event.key == pygame.K_a:
                    tasks.add_task(f"Task {len(tasks.tasks) + 1}")
                elif event.key == pygame.K_m:
                    inventory.add_item(f"Item {len(inventory.items) + 1}")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if stand_mixer_rect.collidepoint(mouse_x, mouse_y):
                    selecting_items = True
                    selected_items.clear()

                if selecting_items and inventory.visible:
                    width, height = inventory.calculate_dimensions()
                    inventory_x = SCREEN_WIDTH - width - 20
                    inventory_y = 20
                    if inventory_x <= mouse_x <= inventory_x + width and inventory_y <= mouse_y <= inventory_y + height:
                        index = (mouse_y - inventory_y - 40) // (inventory.font_size + inventory.padding)
                        if 0 <= index < len(inventory.items):
                            selected_item = inventory.items[index]
                            if selected_item not in selected_items:
                                selected_items.append(selected_item)

                            if len(selected_items) == 3:
                                if set(selected_items) == {"Ex 1", "Ex 2", "Ex 3"}:
                                    correct_items_popup_time = time.time()
                                    if correct_sound:
                                        correct_sound.play()
                                    for item in selected_items:
                                        inventory.remove_item(item)
                                    inventory.add_item("Ex 4")
                                else:
                                    wrong_items_popup_time = time.time()
                                    if incorrect_sound:
                                        incorrect_sound.play()
                                selecting_items = False

        screen.fill(WHITE)

        screen.blit(stand_mixer_image, stand_mixer_rect)

        inventory.draw(screen)

        tasks.render(screen)

        if selecting_items:
            draw_select_prompt()

        if wrong_items_popup_time and time.time() - wrong_items_popup_time < 1:
            draw_popup("Wrong Items", RED)
        elif wrong_items_popup_time and time.time() - wrong_items_popup_time >= 1:
            wrong_items_popup_time = None
        if correct_items_popup_time and time.time() - correct_items_popup_time < 1:
            draw_popup("Item Collected", GREEN)
        elif correct_items_popup_time and time.time() - correct_items_popup_time >= 1:
            correct_items_popup_time = None

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

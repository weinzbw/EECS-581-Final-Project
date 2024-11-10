# Sound Test
# Code Artifact 14
# Sam Harrison
# Created: 11/10/24
# Preconditions: takes inputs of test_image.png and test_sound.mp3
# Postconditions: plays sound when clicked
# Errors/Exceptions: FileNotFoundError if image or sound are missing
# Side Effects: requires audio usage
# Variants: none known
# Known Faults: none known

import pygame
import sys
from helper import Room, GameObject, load_sound


pygame.init()
screen = pygame.display.set_mode((500, 500))

test_image = pygame.image.load("test_image.png")
test_sound = load_sound("test_sound.mp3")

room = Room()
button = GameObject(38, 190, test_image, sound = test_sound)
room.add_object(button)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            room.handle_click(pos)

    screen.fill((255, 255, 255))  # Clear screen with white background
    room.draw(screen)  # Draw room and its objects
    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()

import pygame
import sys
import time

# this block initializes Pygame, as well as making the window (made with the help of ChatGPT)
pygame.init()
window_width, window_height = 640, 480
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Escape Room")

# CREATING CANVAS 
canvas = pygame.display.set_mode((500,500)) 
  
# TITLE OF CANVAS 
pygame.display.set_caption("Show Image") 
exit = False

while not exit: 
    canvas.fill((255,255,255)) 
  
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
  
    pygame.display.update() 
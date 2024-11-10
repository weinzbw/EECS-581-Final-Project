"""
Program Name: win_lose.py
Description: Helper file that controls win/loss conditions. 1 hour timer complete the game
Programmer(s): Naran Bat
Date Made: 11/05/2024
Date(s) Revised:11/10/2024: Added timer display to show remaining time on screen.
Preconditions: Must be initialized before calling any functions from this file
Postconditions: Win and loss conditions are properly displayed. Countdown timer is displayed on the game screen, updating each second.
Errors/Exceptions: None explicitly handled
Side Effects: Rendering win/lose screens and the countdown timer
Invariants: The countdown timer should consistently update and display time
Known Faults: Timer precision may be slightly affected by Pygame's frame rate
"""

import pygame
import sys
import time

class GameTimer:
    def __init__(self, duration):
        self.start_time = time.time()
        self.duration = duration  # in seconds

    def time_remaining(self):
        elapsed = time.time() - self.start_time
        return max(self.duration - elapsed, 0)

    def is_time_up(self):
        return self.time_remaining() <= 0

    def format_time(self):
        remaining = int(self.time_remaining())
        minutes = remaining // 60
        seconds = remaining % 60
        return f"{minutes:02}:{seconds:02}"

class GameState:
    def __init__(self):
        self.timer = GameTimer(60)  # 1-hour timer
        self.door_unlocked = False

    def unlock_door(self):
        self.door_unlocked = True

    def check_win_condition(self):
        return self.door_unlocked

    def check_fail_condition(self):
        return self.timer.is_time_up()

    def update(self):
        # Update win/fail condition checks and handle outcomes
        if self.check_win_condition():
            return "win"
        elif self.check_fail_condition():
            return "fail"
        return "ongoing"

# Functions to display win and fail screens
def display_win_screen(screen):
    screen.fill((0, 240, 0))  # Green background for win
    font = pygame.font.SysFont('Arial', 64)
    text = font.render("You Win!", True, (0, 0, 0))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)  # Show for 3 seconds

def display_fail_screen(screen):
    screen.fill((240, 0, 0))  # Red background for fail
    font = pygame.font.SysFont('Arial', 64)
    text = font.render("Time's Up! You Lose.", True, (0, 0, 0))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)  # Show for 3 seconds

# Function to display the countdown timer on the screen
def display_timer(screen, timer):
    font = pygame.font.SysFont('Arial', 32)
    time_text = timer.format_time()
    text_surface = font.render(time_text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))  # Display timer at the top-left corner

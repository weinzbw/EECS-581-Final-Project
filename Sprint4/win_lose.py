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
Known Faults: N/A
"""

import pygame
import sys
import time

pygame.init()

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
        self.timer = GameTimer(5*60)  # 5 minute timer
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

def display_win_screen(screen):
    screen.fill((0, 240, 0))  # Green background for win
    font = pygame.font.SysFont('Arial', 64)
    text = font.render("You Win!", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    # Pulsing animation
    for scale in range(50, 101, 2):  # Scale from 50% to 100% size
        scaled_font = pygame.font.SysFont('Arial', scale)
        scaled_text = scaled_font.render("You Win!", True, (0, 0, 0))
        scaled_rect = scaled_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.fill((0, 240, 0))  # Ensure the background stays consistent
        screen.blit(scaled_text, scaled_rect)
        pygame.display.update()
        pygame.time.delay(30)  # Adjust for animation speed

    # Flashing effect after pulsing
    for _ in range(5):
        screen.fill((0, 240, 0))  # Green background
        pygame.display.update()
        pygame.time.delay(150)
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(150)

    pygame.time.wait(3000)  # Show for 3 seconds
    display_credits(screen)


def display_fail_screen(screen):
    screen.fill((240, 0, 0))  # Red background for fail
    font = pygame.font.SysFont('Arial', 64)
    text = font.render("Time's Up! You Lose.", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    # Pulsing animation
    for scale in range(50, 101, 2):  # Scale from 50% to 100% size
        scaled_font = pygame.font.SysFont('Arial', scale)
        scaled_text = scaled_font.render("Time's Up! You Lose.", True, (0, 0, 0))
        scaled_rect = scaled_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.fill((240, 0, 0))  # Ensure the background stays consistent
        screen.blit(scaled_text, scaled_rect)
        pygame.display.update()
        pygame.time.delay(30)  # Adjust for animation speed

    # Flashing effect after pulsing
    for _ in range(5):
        screen.fill((240, 0, 0))  # Red background
        pygame.display.update()
        pygame.time.delay(150)
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(150)

    pygame.time.wait(3000)  # Show for 3 seconds
    display_credits(screen)


def display_credits(screen):
    screen.fill((0, 0, 0))  # Black background for credits
    font = pygame.font.SysFont('Arial', 36)
    credits = [
        "Made for EECS 581",
        "",
        "",
        "Team 37",
        "",
        "Ben Weinzirl",
        "",
        "Del Endecott",
        "",
        "Mick Torres",
        "",
        "Naran Bat",
        "",
        "Sam Harrison",
        "",
        "",
        "",
        "",
        "Thank you for playing!",
    ]

    # Starting position for the text to scroll up
    screen_height = screen.get_height()
    y_offset = screen_height

    # Scroll the credits
    while y_offset > -len(credits) * 50:  # Ensure all text scrolls past the screen
        screen.fill((0, 0, 0))  # Clear the screen each frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        for i, line in enumerate(credits):
            text = font.render(line, True, (255, 255, 255))  # White text
            text_rect = text.get_rect(center=(screen.get_width() // 2, y_offset + i * 50))
            screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(50)  # Adjust for scroll speed
        y_offset -= 2  # Move text upward gradually

    # Wait a moment at the end of the credits
    pygame.time.wait(2000)

# Function to display the countdown timer on the screen
def display_timer(screen, timer):
    font = pygame.font.SysFont('Arial', 32)
    time_text = timer.format_time()
    text_surface = font.render(time_text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))  # Display timer at the top-left corner
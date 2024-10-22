import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Button Example")

# Define colors
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Set up fonts
font = pygame.font.SysFont('Arial', 32)

# Button click state
button_clicked = False

# Create a function to draw a button
def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    global button_clicked
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Check if the mouse is over the button
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))

        if click[0] == 1 and not button_clicked:
            button_clicked = True  # Set flag to prevent repeated clicks
            if action is not None:
                action()

        if click[0] == 0:  # Detect mouse release to reset the flag
            button_clicked = False
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    # Render the text on the button
    button_text = font.render(text, True, BLACK)
    screen.blit(button_text, (x + (width // 2 - button_text.get_width() // 2), y + (height // 2 - button_text.get_height() // 2)))

# Define the action function to be triggered when the button is clicked
def button_action():
    print("Button clicked!")

def start():
    screen.fill(WHITE)
# Run the game loop
while True:
    screen.fill(WHITE)

    # Draw the button (text, x, y, width, height, inactive color, active color, action)
    draw_button("Start Game", 300, 150, 200, 50, GRAY, DARK_GRAY, button_action)
    draw_button("Load Game", 300, 250, 200, 50, GRAY, DARK_GRAY, button_action)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

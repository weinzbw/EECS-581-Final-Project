"""
Program Name: front_room.py
Description: Provide the front view of the room. Currently a template with placeholder image and object interaction.
Programmer(s): Naran Bat, Sam Harrison, Ben Weinzirl
Date Made: 10/26/2024
Date(s) Revised:
10/27/2024: Added placeholder image and object interaction
11/5/2024: Made a main function for connecting to other screens
11/10/2024: Added win_lose conditions
11/16/2024: Avoided using "global" for interaction_time
11/23/2024: Added the computer from Sam's main.py to this screen to avoid using temp room. More will need to be done for full integration. Updated for pause menu
11/24/2024: Added Sam's fix to chess, added navigation
11/27/2024: Removed task implementation
12/2/2024: Added Inventory Class Initalization. Removed left room from rotation
12/3/2024: Added Uno Reverse Card to printer
12/7/2024: Deleted "state" variable, added fan and cellar objects, added more savestate variables (carpet gets destroyed by ceiling fan)
12/8/2024: Added intermediate frame to carpet getting destroyed. Added interaction texts when hovering over items and removed transparent boxes
Preconditions: Requires a JPEG image located in the same directory as the program.
Postconditions: A graphical window displaying the room background with interactive objects. Users can hover and click on objects to see visual feedback
Errors/Exceptions: No intended errors/exceptions
Side Effects: Opens a graphical Pygame window that requires user input to close.
Invariants: The screen dimensions are constant at 800x600 pixels. Interactive object areas are fixed and defined as rectangles within the room.
Known Faults:
"""


import pygame
import sys
import win_lose
import time
import helper
import right
import back_room
from objects import Inventory

pygame.init()
pygame.mixer.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Front View")

# Load images and rects for arrows
left_image = pygame.image.load("Images/left_arrow_white.png")
right_image = pygame.image.load("Images/right_arrow_white.png")
left_image = pygame.transform.scale(left_image, (50, 50))
right_image = pygame.transform.scale(right_image, (50, 50))
leftRect = left_image.get_rect()
rightRect = right_image.get_rect()
leftRect.center = (50, 300)
rightRect.center = (750, 300)

# Define font
font = pygame.font.SysFont(None, 36)
interaction_text = ""

# Define objects
objects = {
    "computer": pygame.Rect(120, 260, 100, 100),
    "keyboard": pygame.Rect(100, 400, 100, 30),
    "printer": pygame.Rect(500, 280, 180, 110),
    "fan": pygame.Rect(315, 5, 200, 75),
    "cellar": pygame.Rect(100, 525, 575, 100),
    "right": rightRect,
    "left": leftRect
}

# Colors
HIGHLIGHT_COLOR = (255, 255, 0)
TRANSPARENT_COLOR = (0, 0, 255, 100)

# this loads the computer screen itself
computer_view_image = pygame.image.load("Images/computer_view.png")
scaled_computer_view_image = pygame.transform.scale(computer_view_image, (WIDTH, HEIGHT))

# this loads the progress bar in the middle of the screen of the computer
fakebar_image = pygame.image.load("Images/fakebar1.png")
fakebar_position = ((WIDTH - 200) // 2, (HEIGHT - 75) // 2)

# this loads the little bar that will be used later on the progress bar window
fakebar_progress_image = pygame.image.load("Images/fakebar2.png")

# this loads chess and its pieces
chess_board_image = pygame.image.load("Images/chess_board.png")
chess_board_rect = chess_board_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
black_king_image = pygame.image.load("Images/black_king.png")
white_king_image = pygame.image.load("Images/white_king.png")
white_pawn_image = pygame.image.load("Images/white_pawn.png")

# this is the chessboard tile size with the positioning of pieces
tile_size = 21
board_offset_x = chess_board_rect.left + 16
board_offset_y = chess_board_rect.top + 41

# uses defined board size to offset the pieces to be on the tiles
tile_positions = {
    "E8": (board_offset_x + 4 * tile_size, board_offset_y + 0 * tile_size),  # black king
    "A3": (board_offset_x + 0 * tile_size, board_offset_y + 5 * tile_size),  # white king
    "E4": (board_offset_x + 4 * tile_size, board_offset_y + 4 * tile_size)   # white pawn
}

# does more for centering the pieces
piece_offsets = {
    "black_king": ((tile_size - black_king_image.get_width()) // 2, (tile_size - black_king_image.get_height()) // 2),
    "white_king": ((tile_size - white_king_image.get_width()) // 2, (tile_size - white_king_image.get_height()) // 2),
    "white_pawn": ((tile_size - white_pawn_image.get_width()) // 2, (tile_size - white_pawn_image.get_height()) // 2)
}

# does more for centering the pieces
piece_positions = {
    "black_king": (tile_positions["E8"][0] + piece_offsets["black_king"][0], tile_positions["E8"][1] + piece_offsets["black_king"][1]),
    "white_king": (tile_positions["A3"][0] + piece_offsets["white_king"][0], tile_positions["A3"][1] + piece_offsets["white_king"][1]),
    "white_pawn": (tile_positions["E4"][0] + piece_offsets["white_pawn"][0], tile_positions["E4"][1] + piece_offsets["white_pawn"][1])
}



# Function to draw a transparent overlay on a rectangle
def draw_transparent_overlay(rect, color):
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA) 
    overlay.fill(color)
    screen.blit(overlay, rect.topleft)

def handle_hover(obj, savestate, inventory):
    if obj == "computer":
        if int(savestate[0]) == 0:
            return "Turn on the computer?"
        elif int(savestate[1]) == 0:
            return "Continue playing?"
        else:
            return "That's enough gaming for now"
    elif obj == "keyboard":
        return "Tip tap type"
    elif obj == "printer":
        if not "Uno Reverse Card" in inventory.items and savestate[3] == 0:
            return "It looks like something is in here"
        return "Out of ink"
    elif obj == "fan":
        return "It is chilly in here. I wish it was the opposite"
    elif obj == "cellar":
        if savestate[3] == 0:
            return "What a lovely rug. It really puts the room together"
        elif savestate[3] == 1:
            return "Was this here the whole time?"
        elif savestate[3] == 2:
            if not "Thing 2/2" in inventory.items and savestate[4] == 0:
                return "There's a thing in here!"
            else:
                return "I'm not going down there"
    elif obj == "right":
        return "Go to the Right Room"
    elif obj == "left":
        return "Go to the Back Room"

# Function whenver the player is on the computer screen
def computer(game_state, savestate, computer_unlocked, chess_completed):
    # block of variables for the progress bar; it starts at the pixel of the top-left corner of the progress bar
    progress_start_x = fakebar_position[0] + 44
    progress_start_y = fakebar_position[1] + 32
    progress_x_offset = 0
    right_arrow_count = 0

    # tracks pawns positioning
    pawn_tile_x, pawn_tile_y = 4, 4  

    running = True
    while running:
        screen.blit(scaled_computer_view_image, (0, 0))

        # Display the countdown timer
        win_lose.display_timer(screen, game_state.timer)

        # displays the loading bar until you unlock the computer; it needs to be removed when the task is complete
        if not computer_unlocked:
            screen.blit(fakebar_image, fakebar_position)
            for i in range(0, progress_x_offset, 4):
                segment_x = progress_start_x + i
                screen.blit(fakebar_progress_image, (segment_x, progress_start_y))
        # display the chess board until you beat chess; it needs to be removed when the task is complete
        elif not chess_completed:
            screen.blit(chess_board_image, chess_board_rect.topleft)
            screen.blit(black_king_image, piece_positions["black_king"])
            screen.blit(white_king_image, piece_positions["white_king"])
            screen.blit(white_pawn_image, piece_positions["white_pawn"])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not computer_unlocked:
                    # when available, it'll let you add a bar when pressing right arrow key
                    if progress_x_offset < 200 - 44:
                        progress_x_offset += 4
                        right_arrow_count += 1
                        if right_arrow_count >= 36:
                            computer_unlocked = True # changed from game states above
                            savestate[0]="1"
                elif event.key == pygame.K_ESCAPE:
                    return savestate
                # lets the chess board's pawn be controlled when the task is available; it makes sure it doesnt go out of bounds as well
                elif computer_unlocked and not chess_completed:
                    new_tile_x, new_tile_y = pawn_tile_x, pawn_tile_y
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and pawn_tile_y > 0:
                            new_tile_y -= 1
                        elif event.key == pygame.K_DOWN and pawn_tile_y < 7:
                            new_tile_y += 1
                        elif event.key == pygame.K_LEFT and pawn_tile_x > 0:
                            new_tile_x -= 1
                        elif event.key == pygame.K_RIGHT and pawn_tile_x < 7:
                            new_tile_x += 1
                        elif event.key == pygame.K_ESCAPE:
                            return savestate
                        
                    if (new_tile_x, new_tile_y) != (0, 5):  # white king's position in chessboard coordinates
                        pawn_tile_x, pawn_tile_y = new_tile_x, new_tile_y
            
                    # updates pawn's positioning
                    piece_positions["white_pawn"] = (
                    board_offset_x + pawn_tile_x * tile_size + piece_offsets["white_pawn"][0],
                    board_offset_y + pawn_tile_y * tile_size + piece_offsets["white_pawn"][1]
                    )

                # checks for the pawn reaching the black king; when it's done, it's complete
                if pawn_tile_x == 4 and pawn_tile_y == 0:
                    running = False  # closes computer view, so the player can see the drawer opening
                    chess_completed = True 
                    savestate[1] = "1"
        text_surface = font.render("USE ARROW KEYS", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        screen.blit(text_surface, text_rect)

        text_surface = font.render("ESC TO EXIT", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
    return savestate

# Main loop
def front(game_state, savestate, inventory: Inventory):
    # load the sounds
    computer_sound = pygame.mixer.Sound("sounds/computer.mp3")
    printer_sound = pygame.mixer.Sound("sounds/printer.mp3")

    # Determines which background to use based on savestate
    room_image = pygame.image.load("Images/RealFront.jpg") 
    room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))

    thing2 = pygame.image.load("Images/Thing2.png")
    thing2 = pygame.transform.scale(thing2, (50, 50))

    if int(savestate[3]) == 1: # If Uno Card Used
        room_image = pygame.image.load("Images/DestroyedCarpet.jpg") 
        room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))

    if int(savestate[3]) == 2: # IF Cellar door opened
        room_image = pygame.image.load("Images/OpenFront.jpg") 
        room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))

    interaction_time = 0

    pygame.display.set_caption("Front Room")

    clock = pygame.time.Clock()
    running = True
    while running:
        # Check win/fail conditions
        status = game_state.update()
        if status == "win":
            win_lose.display_win_screen(screen)
            running = False
        elif status == "fail":
            win_lose.display_fail_screen(screen)
            running = False

        # Clear the screen and display room image
        screen.blit(room_image, (0, 0))
        screen.blit(left_image, leftRect)
        screen.blit(right_image, rightRect)
        if not "Thing 2/2" in inventory.items and savestate[3] == 2:
            screen.blit(thing2, (380, 520))
        if inventory.visible:
            inventory.draw(screen)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw objects with hover effects
        for obj_name, obj_rect in objects.items():
            if obj_rect.collidepoint(mouse_pos):
                interaction_text = handle_hover(obj_name, savestate, inventory)
                interaction_time = time.time()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if player clicked on an object
                for obj_name, obj_rect in objects.items():
                    if obj_rect.collidepoint(mouse_pos):

                        if obj_name == "computer": # If computer clicked
                            computer_sound.play()
                            savestate = computer(game_state, savestate, int(savestate[0]), int(savestate[1])) # Run the computer function

                        if obj_name == "keyboard": # If keyboard clicked
                            if "Extremely Tiny Crowbar" in inventory.selected_items: # If player has Extremely Tiny Crowbar
                                inventory.selected_items = set()
                                savestate[1] = 2 # Player used the Crowbar
                                inventory.remove_item("Extremely Tiny Crowbar")
                                inventory.add_item("Keyboard Key") # Add Keyboard Key to inventory

                        if obj_name == "printer": # If printer clicked

                            if "Uno Reverse Card" not in inventory.items and not int(savestate[3]) > 0: # IF the player hasn't collected or used the Uno Reverse Card
                                printer_sound.play()
                                inventory.add_item("Uno Reverse Card")

                        if obj_name == "fan" and "Uno Reverse Card" in inventory.selected_items: # If fan clicked and the player has Uno Reverse Card
                            inventory.selected_items = set()
                            savestate[3] = 1 # Carpet is destroyed

                            # Show intermediate flame of carpet going to the fan
                            room_image = pygame.image.load("Images/CarpetFly.jpg")
                            room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))
                            screen.blit(room_image, (0, 0))
                            pygame.display.flip()

                            pygame.time.wait(1000) # Wait to show intermediate frame

                            # Show background of carpet destroyed
                            room_image = pygame.image.load("Images/DestroyedCarpet.jpg") 
                            room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))
    
                            inventory.remove_item("Uno Reverse Card") # Remove Uno Reverse Card from inventory

                        if obj_name == "cellar": # If the cellar is clicked

                            if int(savestate[3]) == 2 and not "Thing 2/2" in inventory.items: # If cellar door opened
                                inventory.add_item("Thing 2/2")

                            if int(savestate[3]) == 1: # If cellar door not opened
                                savestate[3] = 2 # Cellar door opened

                                # Update background to reflect change
                                room_image = pygame.image.load("Images/OpenFront.jpg") 
                                room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))

                        if obj_name == "left": # If left arrow clicked
                            back_room.back(game_state, savestate, inventory) # Go to the back room

                        if obj_name == "right": # If right arrow clicked
                            right.right(game_state, savestate, inventory) # Go to the right room

            elif event.type == pygame.KEYDOWN: # If a key is pressed
                if event.key == pygame.K_ESCAPE: # If the ESC key is pressed
                    helper.pause_menu(screen, font, "savedata.txt", game_state, savestate, inventory) # Show the pause menu
                if event.key == pygame.K_i: # If i is pressed
                    inventory.toggle_visibility() # Show or hide the inventory
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN: # If up or down arrows are pressed
                    inventory.handle_input(event) # Handle the input for inventory
                if int(savestate[4]) == 0:
                    if event.key == pygame.K_RETURN: # If Enter is pressed
                        inventory.handle_input(event) # Handle the input for inventory
                        if len(inventory.selected_items) > 1:
                            print(inventory.selected_items)
                            inventory.selected_items = set()
                            print(inventory.selected_items)

        # Check if interaction text should be cleared after 2 seconds
        if time.time() - interaction_time > 2:
            interaction_text = ""
        # Display interaction text
        text_surface = font.render(interaction_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(text_surface, text_rect)

        # Display the countdown timer
        win_lose.display_timer(screen, game_state.timer)

        # Update display and control frame rate
        pygame.display.flip()
        clock.tick(30)  # Cap the frame rate

    # Quit Pygame when loop ends
    helper.save_state(game_state, savestate, inventory)
    pygame.quit()
    sys.exit()

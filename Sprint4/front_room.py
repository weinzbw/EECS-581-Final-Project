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
import left

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Front View")

# Load room image
room_image = pygame.image.load("front_room.jpeg") 
room_image = pygame.transform.scale(room_image, (WIDTH, HEIGHT))
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
    "printer": pygame.Rect(500, 280, 180, 110),
    "right": rightRect,
    "left": leftRect
}

# Colors
HIGHLIGHT_COLOR = (255, 255, 0)
TRANSPARENT_COLOR = (0, 0, 255, 100)

# Initialize game state
game_state = win_lose.GameState() # 1-hour timer and locked door initially

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
    screen.blit(left_image, leftRect)
    screen.blit(right_image, rightRect)

def computer(savestate, computer_unlocked, chess_completed):
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
                            main.tasks.complete_task("Unlock the computer")
                            computer_unlocked = True # changed from game states above
                            savestate[0]="1"
                            main.tasks.add_task("Beat Chess")  # gives the player this task, as chess is now visible
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
                    main.tasks.complete_task("Beat Chess")
        pygame.display.flip()
    return savestate

# Main loop
def front(savestate, inventory, state):

    interaction_time = 0

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

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw objects with hover effects
        for obj_name, obj_rect in objects.items():
            if obj_rect.collidepoint(mouse_pos):
                # Highlight object when hovering
                draw_transparent_overlay(obj_rect, HIGHLIGHT_COLOR + (100,))
                interaction_text = f"You are hovering over the {obj_name}."
                interaction_time = time.time()
            else:
                # Transparent overlay when not hovering
                draw_transparent_overlay(obj_rect, TRANSPARENT_COLOR)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if player clicked on an object
                for obj_name, obj_rect in objects.items():
                    if obj_rect.collidepoint(mouse_pos):
                        interaction_text = f"You clicked on the {obj_name}."
                        interaction_time = time.time()
                        # If the monitor is clicked, unlock the door (win condition)
                        if obj_name == "computer":
                            savestate = computer(savestate, int(savestate[0]), int(savestate[1]))
                        if obj_name == "printer":
                            game_state.unlock_door() # Set win state
                        if obj_name == "left":
                            left.left(savestate, inventory, state)
                        if obj_name == "right":
                            right.right(savestate, inventory, state)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    helper.pause_menu(screen, font, "savedata.txt", savestate, inventory, state)

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
    helper.save_state(savestate, inventory, state)
    pygame.quit()
    sys.exit()

# Main
# Code Artifacts 8-11
# This is a (potentially temporary) main file. Its goal is to run the whole game loop of the beginning room. In this version, you can complete a few tasks. You can print an uno reverse card, unlock the computer, beat chess, and get the crowbar from the drawer.
# Name: Sam Harrison, Ben Weinzirl
# Creation Date: 10/26/24
# Revision Date(s): 11/5/24 - Temporarily added to front for testing, updated for savegame file
#                   11/7/24 - Added connection to front room, updated saving
#                   11/16/24 - Added Sam's sounds. got rid of the "global" usage, refactored loading a save
# Preconditions: The only inputs are the arrow keys and mouse clicks. These are used to interact with the world. Also, I opens the inventory, and T shows the task list.
# Postconditions: The only values returned are visual. That could be an item going in your inventory or something moving in game.
# Error & Exceptions: There are none so far.
# Side Effects: inventory, is_computer_view, computer_unlocked, chess_completed, pawn_tile_x, pawn_tile_y
# Invariants: chess movement boundaries, tasks, drawer state
# Faults:
import pygame
import sys
import time
from tasks import Tasks
from helper import handle_save, GameObject

# this block initializes Pygame, as well as making the window (made with the help of ChatGPT)
pygame.init()
window_width, window_height = 640, 480
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Escape Room")

# load the sounds
#computer_sound = load_sound("sounds/computer.mp3")
#drawer_sound = load_sound("sounds/drawer.mp3")
#printer_sound = load_sound("sounds/printer.mp3")

# this block loads the background image; it is scaled to match the increased window size
room_image = pygame.image.load("Images/temp_room.png")
scaled_room_image = pygame.transform.scale(room_image, (window_width, window_height))

# this block loads the computer image and sets its location; it is scaled to match the increased window size
computer_image = pygame.image.load("Images/computer_object.png")
computer_image = pygame.transform.scale(computer_image, (128, 72))
computer_position = (400, 300)
computer_object = GameObject(computer_position[0], computer_position[1], computer_image)

# this block loads the drawer images and sets their location; it is scaled to match the increased window size
drawer_closed_image = pygame.image.load("Images/drawer_closed.png")
drawer_opened_image = pygame.image.load("Images/drawer_opened.png")
drawer_position = (50, computer_position[1])
drawer_object = GameObject(drawer_position[0], drawer_position[1], drawer_closed_image)

# this block loads the printer image and sets its location; it is scaled to match the increased window size; I was lazy, so the printer is positioned between the two via their own variables (made with the help of ChatGPT)
printer_image = pygame.image.load("Images/printer.png")
printer_position = (drawer_position[0] + 150, computer_position[1])  # Position the printer between drawer and computer
printer_object = GameObject(printer_position[0], printer_position[1], printer_image)

# this loads the computer screen itself
computer_view_image = pygame.image.load("Images/computer_view.png")
scaled_computer_view_image = pygame.transform.scale(computer_view_image, (window_width, window_height))

# this loads the progress bar in the middle of the screen of the computer
fakebar_image = pygame.image.load("Images/fakebar1.png")
fakebar_position = ((window_width - 200) // 2, (window_height - 75) // 2)

# this loads the little bar that will be used later on the progress bar window
fakebar_progress_image = pygame.image.load("Images/fakebar2.png")

# this loads chess and its pieces
chess_board_image = pygame.image.load("Images/chess_board.png")
chess_board_rect = chess_board_image.get_rect(center=(window_width // 2, window_height // 2))
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



# starts list of tasks
tasks = Tasks(font_size=24, tasks=["Unlock the computer", "Collect the crowbar", "Print"])

# font loaded
font = pygame.font.SysFont("Courier New", 24)

# main game loop
def computer():

    # sets current game states
    savestate = handle_save("savedata.txt")
    print(savestate)
    computer_unlocked = int(savestate[0])
    chess_completed = int(savestate[1])
    state = []
    inventory = []
    i = 2
    while i < len(savestate):
        if savestate[i] not in inventory:
            inventory.append(str(savestate[i]))
            state.append(str(savestate[i]))
        i += 1

    in_computer_view = False
    inventory_visible = False 
    item_popup_time = None  

    # block of variables for the progress bar; it starts at the pixel of the top-left corner of the progress bar
    progress_start_x = fakebar_position[0] + 44
    progress_start_y = fakebar_position[1] + 32
    progress_x_offset = 0
    right_arrow_count = 0

    # tracks pawns positioning
    pawn_tile_x, pawn_tile_y = 4, 4  

    running = True
    while running:
        for event in pygame.event.get():
            # the game is no longer running when the game has been ended
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.KEYDOWN:
                # T shows task list
                if event.key == pygame.K_t:
                    tasks.toggle_visibility()
                # I shows inventory
                elif event.key == pygame.K_i:
                    inventory_visible = not inventory_visible
                # ESC exits computer view; it also resets the task progress for unlocking the computer
                elif event.key == pygame.K_ESCAPE:
                    in_computer_view = False
                    progress_x_offset = 0
                    right_arrow_count = 0
                # this is the task unlocking the computer
                elif event.key == pygame.K_RIGHT and in_computer_view and not computer_unlocked:
                    # when available, it'll let you add a bar when pressing right arrow key
                    if progress_x_offset < 200 - 44:
                        progress_x_offset += 4
                        right_arrow_count += 1
                        if right_arrow_count >= 36:
                            tasks.complete_task("Unlock the computer")
                            computer_unlocked = True # changed from game states above
                            savestate[0]="1"
                            tasks.add_task("Beat Chess")  # gives the player this task, as chess is now visible
                # lets the chess board's pawn be controlled when the task is available; it makes sure it doesnt go out of bounds as well
                elif computer_unlocked and not chess_completed:
                    if event.key == pygame.K_UP and pawn_tile_y > 0:
                        pawn_tile_y -= 1
                    elif event.key == pygame.K_DOWN and pawn_tile_y < 7:
                        pawn_tile_y += 1
                    elif event.key == pygame.K_LEFT and pawn_tile_x > 0:
                        pawn_tile_x -= 1
                    elif event.key == pygame.K_RIGHT and pawn_tile_x < 7:
                        pawn_tile_x += 1

                    # updates pawn's positioning
                    piece_positions["white_pawn"] = (
                        board_offset_x + pawn_tile_x * tile_size + piece_offsets["white_pawn"][0],
                        board_offset_y + pawn_tile_y * tile_size + piece_offsets["white_pawn"][1]
                    )

                    # checks for the pawn reaching the black king; when it's done, it's complete
                    if pawn_tile_x == 4 and pawn_tile_y == 0:
                        in_computer_view = False  # closes computer view, so the player can see the drawer opening
                        chess_completed = True 
                        savestate[1] = "1"
                        tasks.complete_task("Beat Chess") 

            # used when the drawer is open; when it is, checks if your mouse is over it and you click; then it gives you the items in the drawer, completing the task
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # play computer sound if clicked
                if computer_object.rect.collidepoint(mouse_x, mouse_y):
                    computer_object.handle_click()
                    in_computer_view = True
                 
                drawer_rect = drawer_opened_image.get_rect(topleft=drawer_position)
                if chess_completed and drawer_rect.collidepoint(mouse_x, mouse_y) and "This Thing" not in inventory:
                    drawer_object.handle_click() # play drawer sound if clicked and unlocked
                    inventory.append("This Thing")
                    inventory.append("Extremely Small Crowbar")
                    tasks.complete_task("Collect the crowbar") 
                    item_popup_time = time.time()  # set the popup display time

                # checks if the printer is clicked; if not, you can get the uno reverse card and complete this task
                printer_rect = printer_image.get_rect(topleft=printer_position)
                if printer_rect.collidepoint(mouse_x, mouse_y) and "Uno Reverse Card" not in inventory:
                    printer_object.handle_click()  # play printer sound if clicked
                    inventory.append("Uno Reverse Card")
                    tasks.complete_task("Print") 
                    item_popup_time = time.time() 

                # checks if the computer is clicked, this prevents you from potentially clicking on it when already in it
                if not in_computer_view:
                    computer_rect = computer_image.get_rect(topleft=computer_position)
                    if computer_rect.collidepoint(mouse_x, mouse_y):
                        in_computer_view = True

        # display the correct view
        if in_computer_view:
            window.blit(scaled_computer_view_image, (0, 0))

            # displays the loading bar until you unlock the computer; it needs to be removed when the task is complete
            if not computer_unlocked:
                window.blit(fakebar_image, fakebar_position)
                for i in range(0, progress_x_offset, 4):
                    segment_x = progress_start_x + i
                    window.blit(fakebar_progress_image, (segment_x, progress_start_y))
            # display the chess board until you beat chess; it needs to be removed when the task is complete
            elif not chess_completed:
                window.blit(chess_board_image, chess_board_rect.topleft)
                window.blit(black_king_image, piece_positions["black_king"])
                window.blit(white_king_image, piece_positions["white_king"])
                window.blit(white_pawn_image, piece_positions["white_pawn"])
        else:
            # displays the rest in its correct state
            window.blit(scaled_room_image, (0, 0))
            window.blit(computer_image, computer_position)
            window.blit(printer_image, printer_position)
        
            # opens the drawer (visually) when chess is complete
            if chess_completed:
                window.blit(drawer_opened_image, drawer_position)
            else:
                window.blit(drawer_closed_image, drawer_position)
            
            tasks.render(window)

        # display inventory (it's currently ugly and needs some fixing)(made with the help of ChatGPT)
        if inventory_visible:
            inventory_surface = pygame.Surface((200, 100))
            inventory_surface.fill((240, 240, 240))
            y_offset = 10
            for item in inventory:
                item_text = font.render(f"- {item}", True, (0, 0, 0))
                inventory_surface.blit(item_text, (10, y_offset))
                y_offset += 30
            window.blit(inventory_surface, (window_width - 220, 20))

        # displays a popup when an item is collected for 1 second
        if item_popup_time and time.time() - item_popup_time < 1:
            popup_text = font.render("Items Collected!", True, (255, 255, 255))
            popup_background = pygame.Surface((popup_text.get_width() + 20, popup_text.get_height() + 10))
            popup_background.fill((0, 128, 0))
            popup_background.blit(popup_text, (10, 5))
            window.blit(popup_background, (window_width // 2 - popup_background.get_width() // 2, 20))
        elif item_popup_time and time.time() - item_popup_time >= 1:
            item_popup_time = None
        
        pygame.display.flip() # updates the display

    with open("savedata.txt", "w") as save:
        for line in savestate:
            save.write(str(line) + "\n")
        for item in inventory:
            if item not in state:
                save.write(str(f"{item}\n"))
                state.append(item)

    pygame.quit()
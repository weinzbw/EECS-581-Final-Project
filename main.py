import pygame
import sys
import time
import os
from tasks import Tasks

# Initialize Pygame
pygame.init()
window_width, window_height = 640, 480
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Escape Room")

# Load images and scale them as needed
room_image = pygame.image.load("Images/temp_room.png")
scaled_room_image = pygame.transform.scale(room_image, (window_width, window_height))
computer_image = pygame.image.load("Images/computer_object.png")
computer_image = pygame.transform.scale(computer_image, (128, 72))
computer_position = (400, 300)
drawer_closed_image = pygame.image.load("Images/drawer_closed.png")
drawer_opened_image = pygame.image.load("Images/drawer_opened.png")
drawer_position = (50, computer_position[1])
printer_image = pygame.image.load("Images/printer.png")
printer_position = (drawer_position[0] + 150, computer_position[1])
computer_view_image = pygame.image.load("Images/computer_view.png")
scaled_computer_view_image = pygame.transform.scale(computer_view_image, (window_width, window_height))
fakebar_image = pygame.image.load("Images/fakebar1.png")
fakebar_position = ((window_width - 200) // 2, (window_height - 75) // 2)
fakebar_progress_image = pygame.image.load("Images/fakebar2.png")
chess_board_image = pygame.image.load("Images/chess_board.png")
chess_board_rect = chess_board_image.get_rect(center=(window_width // 2, window_height // 2))
black_king_image = pygame.image.load("Images/black_king.png")
white_king_image = pygame.image.load("Images/white_king.png")
white_pawn_image = pygame.image.load("Images/white_pawn.png")

# Chessboard settings
tile_size = 21
board_offset_x = chess_board_rect.left + 16
board_offset_y = chess_board_rect.top + 41
tile_positions = {
    "E8": (board_offset_x + 4 * tile_size, board_offset_y + 0 * tile_size),
    "A3": (board_offset_x + 0 * tile_size, board_offset_y + 5 * tile_size),
    "E4": (board_offset_x + 4 * tile_size, board_offset_y + 4 * tile_size)
}
piece_offsets = {
    "black_king": ((tile_size - black_king_image.get_width()) // 2, (tile_size - black_king_image.get_height()) // 2),
    "white_king": ((tile_size - white_king_image.get_width()) // 2, (tile_size - white_king_image.get_height()) // 2),
    "white_pawn": ((tile_size - white_pawn_image.get_width()) // 2, (tile_size - white_pawn_image.get_height()) // 2)
}
piece_positions = {
    "black_king": (tile_positions["E8"][0] + piece_offsets["black_king"][0], tile_positions["E8"][1] + piece_offsets["black_king"][1]),
    "white_king": (tile_positions["A3"][0] + piece_offsets["white_king"][0], tile_positions["A3"][1] + piece_offsets["white_king"][1]),
    "white_pawn": (tile_positions["E4"][0] + piece_offsets["white_pawn"][0], tile_positions["E4"][1] + piece_offsets["white_pawn"][1])
}

# Progress bar variables
progress_start_x = fakebar_position[0] + 44
progress_start_y = fakebar_position[1] + 32
progress_x_offset = 0
right_arrow_count = 0

# Initialize tasks
tasks = Tasks(font_size=24, tasks=["Unlock the computer", "Collect the crowbar", "Print"])

# Game state variables
in_computer_view = False
computer_unlocked = False
chess_completed = False
inventory = []
game_paused = False
start_time = time.time()
total_played_time = 0.0

# Load saved game state
if os.path.exists("savedata.txt"):
    with open("savedata.txt", "r") as save:
        savestate = save.read().splitlines()
        try:
            i = 3
            computer_unlocked = int(savestate[0]) == 1
            chess_completed = int(savestate[1]) == 1
            total_played_time = float(savestate[2])
            while i < len(savestate):
                inventory.append(savestate[i])
                i += 1
        except:
            savestate = ['0', '0', '0.0']
else:
    savestate = ['0', '0', '0.0']
    with open("savedata.txt", "w") as save:
        save.write("\n".join(savestate))

inventory_visible = False
item_popup_time = None
pawn_tile_x, pawn_tile_y = 4, 4
font = pygame.font.SysFont("Courier New", 24)
running = True

def format_time(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def render_pause_menu():
    # Semi-transparent overlay
    overlay = pygame.Surface((window_width, window_height))
    overlay.set_alpha(128)  # Semi-transparent
    overlay.fill((0, 0, 0))
    window.blit(overlay, (0, 0))

    # Render timer
    formatted_time = format_time(total_played_time)
    timer_text = font.render(f"Time Played: {formatted_time}", True, (255, 255, 255))
    window.blit(timer_text, (window_width // 2 - timer_text.get_width() // 2, window_height // 2 - 100))

    # Render buttons
    button_width = 200
    button_height = 50
    button_x = window_width // 2 - button_width // 2
    button_y = window_height // 2 - button_height // 2

    # Delete Save button
    delete_save_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(window, (255, 0, 0), delete_save_button_rect)
    delete_save_text = font.render("Delete Save", True, (255, 255, 255))
    window.blit(delete_save_text, (button_x + (button_width - delete_save_text.get_width()) // 2, button_y + (button_height - delete_save_text.get_height()) // 2))

    # Load Save button
    load_save_button_rect = pygame.Rect(button_x, button_y + 60, button_width, button_height)
    pygame.draw.rect(window, (0, 0, 255), load_save_button_rect)
    load_save_text = font.render("Load Save", True, (255, 255, 255))
    window.blit(load_save_text, (button_x + (button_width - load_save_text.get_width()) // 2, button_y + 60 + (button_height - load_save_text.get_height()) // 2))

    # Save and Exit button
    save_exit_button_rect = pygame.Rect(button_x, button_y + 120, button_width, button_height)
    pygame.draw.rect(window, (0, 255, 0), save_exit_button_rect)
    save_exit_text = font.render("Save and Exit", True, (255, 255, 255))
    window.blit(save_exit_text, (button_x + (button_width - save_exit_text.get_width()) // 2, button_y + 120 + (button_height - save_exit_text.get_height()) // 2))

    return delete_save_button_rect, load_save_button_rect, save_exit_button_rect

def delete_save():
    global savestate, inventory, computer_unlocked, chess_completed, total_played_time, pawn_tile_x, pawn_tile_y, progress_x_offset, right_arrow_count, in_computer_view, game_paused, start_time, tasks
    savestate = ['0', '0', '0.0']
    computer_unlocked = False
    chess_completed = False
    total_played_time = 0.0
    inventory.clear()
    pawn_tile_x, pawn_tile_y = 4, 4
    progress_x_offset = 0
    right_arrow_count = 0
    in_computer_view = False
    tasks.reset()
    tasks = Tasks(font_size=24, tasks=["Unlock the computer", "Collect the crowbar", "Print"])
    # Save the reset savestate to file
    with open("savedata.txt", "w") as save:
        save.write("\n".join(savestate))
    # Unpause the game
    global game_paused
    game_paused = False
    start_time = time.time()

def load_save():
    global savestate, inventory, computer_unlocked, chess_completed, total_played_time, pawn_tile_x, pawn_tile_y, progress_x_offset, right_arrow_count, in_computer_view, game_paused, start_time, tasks
    if os.path.exists("savedata.txt"):
        with open("savedata.txt", "r") as save:
            savestate = save.read().splitlines()
            try:
                i = 3
                computer_unlocked = int(savestate[0]) == 1
                chess_completed = int(savestate[1]) == 1
                total_played_time = float(savestate[2])
                inventory = []
                while i < len(savestate):
                    inventory.append(savestate[i])
                    i += 1
            except:
                savestate = ['0', '0', '0.0']
                computer_unlocked = False
                chess_completed = False
                total_played_time = 0.0
                inventory = []
    else:
        savestate = ['0', '0', '0.0']
        computer_unlocked = False
        chess_completed = False
        total_played_time = 0.0
        inventory = []
    pawn_tile_x, pawn_tile_y = 4, 4
    progress_x_offset = 0
    right_arrow_count = 0
    in_computer_view = False
    tasks.reset()
    tasks = Tasks(font_size=24, tasks=["Unlock the computer", "Collect the crowbar", "Print"])
    if computer_unlocked:
        tasks.complete_task("Unlock the computer")
        tasks.add_task("Beat Chess")
    if chess_completed:
        tasks.complete_task("Beat Chess")
        tasks.complete_task("Collect the crowbar")
    if "Extremely Small Crowbar" in inventory:
        tasks.complete_task("Collect the crowbar")
    # Unpause the game
    game_paused = False
    start_time = time.time()

def save_and_exit():
    global running, total_played_time, savestate, start_time
    session_played_time = time.time() - start_time
    total_played_time += session_played_time
    start_time = time.time()
    savestate[0] = '1' if computer_unlocked else '0'
    savestate[1] = '1' if chess_completed else '0'
    savestate[2] = str(total_played_time)
    with open("savedata.txt", "w") as save:
        save.write("\n".join(savestate) + "\n")
        for item in inventory:
            save.write(f"{item}\n")
    running = False

def computer():
    global in_computer_view
    global inventory_visible
    global item_popup_time
    global inventory
    global chess_completed
    global computer_unlocked
    global progress_x_offset
    global right_arrow_count
    global pawn_tile_x
    global pawn_tile_y
    global game_paused
    global total_played_time
    global start_time
    global running
    global savestate
    global tasks

    while running:
        if game_paused:
            # Handle events for pause menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_and_exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                        start_time = time.time()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    # Render pause menu to get button rects
                    delete_save_button_rect, load_save_button_rect, save_exit_button_rect = render_pause_menu()
                    if delete_save_button_rect.collidepoint(mouse_x, mouse_y):
                        delete_save()
                    elif load_save_button_rect.collidepoint(mouse_x, mouse_y):
                        load_save()
                    elif save_exit_button_rect.collidepoint(mouse_x, mouse_y):
                        save_and_exit()
            # Render pause menu
            delete_save_button_rect, load_save_button_rect, save_exit_button_rect = render_pause_menu()
            pygame.display.flip()
            continue  # Skip the rest of the loop when paused
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_and_exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        tasks.toggle_visibility()
                    elif event.key == pygame.K_i:
                        inventory_visible = not inventory_visible
                    elif event.key == pygame.K_ESCAPE:
                        if in_computer_view:
                            in_computer_view = False
                            progress_x_offset = 0
                            right_arrow_count = 0
                        else:
                            # Pause the game
                            session_played_time = time.time() - start_time
                            total_played_time += session_played_time
                            game_paused = True
                    elif event.key == pygame.K_RIGHT and in_computer_view and not computer_unlocked:
                        if progress_x_offset < 200 - 44:
                            progress_x_offset += 4
                            right_arrow_count += 1
                            if right_arrow_count >= 36:
                                tasks.complete_task("Unlock the computer")
                                computer_unlocked = True
                                savestate[0] = "1"
                                tasks.add_task("Beat Chess")
                    elif computer_unlocked and not chess_completed:
                        if event.key == pygame.K_UP and pawn_tile_y > 0:
                            pawn_tile_y -= 1
                        elif event.key == pygame.K_DOWN and pawn_tile_y < 7:
                            pawn_tile_y += 1
                        elif event.key == pygame.K_LEFT and pawn_tile_x > 0:
                            pawn_tile_x -= 1
                        elif event.key == pygame.K_RIGHT and pawn_tile_x < 7:
                            pawn_tile_x += 1
                        piece_positions["white_pawn"] = (
                            board_offset_x + pawn_tile_x * tile_size + piece_offsets["white_pawn"][0],
                            board_offset_y + pawn_tile_y * tile_size + piece_offsets["white_pawn"][1]
                        )
                        if pawn_tile_x == 4 and pawn_tile_y == 0:
                            in_computer_view = False
                            chess_completed = True
                            savestate[1] = "1"
                            tasks.complete_task("Beat Chess")
                            tasks.add_task("Collect the crowbar")
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    drawer_rect = drawer_opened_image.get_rect(topleft=drawer_position)
                    if chess_completed and drawer_rect.collidepoint(mouse_x, mouse_y) and "Extremely Small Crowbar" not in inventory:
                        inventory.append("This Thing")
                        inventory.append("Extremely Small Crowbar")
                        tasks.complete_task("Collect the crowbar")
                        item_popup_time = time.time()
                    printer_rect = printer_image.get_rect(topleft=printer_position)
                    if printer_rect.collidepoint(mouse_x, mouse_y) and "Uno Reverse Card" not in inventory:
                        inventory.append("Uno Reverse Card")
                        tasks.complete_task("Print")
                        item_popup_time = time.time()
                    if not in_computer_view:
                        computer_rect = computer_image.get_rect(topleft=computer_position)
                        if computer_rect.collidepoint(mouse_x, mouse_y):
                            in_computer_view = True

            # Display the correct view
            if in_computer_view:
                window.blit(scaled_computer_view_image, (0, 0))
                if not computer_unlocked:
                    window.blit(fakebar_image, fakebar_position)
                    for i in range(0, progress_x_offset, 4):
                        segment_x = progress_start_x + i
                        window.blit(fakebar_progress_image, (segment_x, progress_start_y))
                elif not chess_completed:
                    window.blit(chess_board_image, chess_board_rect.topleft)
                    window.blit(black_king_image, piece_positions["black_king"])
                    window.blit(white_king_image, piece_positions["white_king"])
                    window.blit(white_pawn_image, piece_positions["white_pawn"])
            else:
                window.blit(scaled_room_image, (0, 0))
                window.blit(computer_image, computer_position)
                window.blit(printer_image, printer_position)
                if chess_completed:
                    window.blit(drawer_opened_image, drawer_position)
                else:
                    window.blit(drawer_closed_image, drawer_position)
                tasks.render(window)

            # Display inventory
            if inventory_visible:
                inventory_surface = pygame.Surface((200, 100))
                inventory_surface.fill((240, 240, 240))
                y_offset = 10
                for item in inventory:
                    item_text = font.render(f"- {item}", True, (0, 0, 0))
                    inventory_surface.blit(item_text, (10, y_offset))
                    y_offset += 30
                window.blit(inventory_surface, (window_width - 220, 20))

            # Display item popup
            if item_popup_time and time.time() - item_popup_time < 1:
                popup_text = font.render("Items Collected!", True, (255, 255, 255))
                popup_background = pygame.Surface((popup_text.get_width() + 20, popup_text.get_height() + 10))
                popup_background.fill((0, 128, 0))
                popup_background.blit(popup_text, (10, 5))
                window.blit(popup_background, (window_width // 2 - popup_background.get_width() // 2, 20))
            elif item_popup_time and time.time() - item_popup_time >= 1:
                item_popup_time = None

            pygame.display.flip()

    # Update total played time before exiting
    session_played_time = time.time() - start_time
    total_played_time += session_played_time
    savestate[0] = '1' if computer_unlocked else '0'
    savestate[1] = '1' if chess_completed else '0'
    savestate[2] = str(total_played_time)
    with open("savedata.txt", "w") as save:
        save.write("\n".join(savestate) + "\n")
        for item in inventory:
            save.write(f"{item}\n")
    pygame.quit()

computer()

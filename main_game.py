# main_game.py
import pygame
import sys
import time
import pygame.mixer
import copy
import math
import random

pygame.init()
pygame.mixer.init()

# Screen & audio (paths kept the same)
screen = pygame.display.set_mode((1080, 800))
pygame.mixer.music.load(r"music\game_music2.mp3")   # initial game music
click_sound = pygame.mixer.Sound(r"music\user_move.wav")
button_click_sound = pygame.mixer.Sound(r"music\user_move.wav")  # Using same sound for buttons

# ---------- Configuration ----------
FPS = 60

# MCTS parameters
MCTS_ITERATIONS = 500  # iterations per MCTS move (increased for better performance)
MCTS_SIMULATION_DEPTH = 60  # cap for playout length

# ---------- Utility / Game logic ----------
def deep_copy(board):
    return copy.deepcopy(board)

# ---------- Main Game ----------
def main_game():
    pygame.mixer.music.play(-1)
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    pygame.display.set_caption("Reversi Game")

    HUMAN = 1
    COMPUTER = -1

    clock = pygame.time.Clock()

    # --- Menu / Grid / Mode selection variables
    grid_size = 8  # default; changed by selection
    selecting = True
    game_mode = None  # "human_vs_human", "human_vs_ai", "ai_vs_ai"
    game_ready = False  # Flag to indicate when to start the game
    
    # AI algorithm and player selection
    human_color = HUMAN  # For human_vs_ai: which side human plays (HUMAN=1=white, COMPUTER=-1=black)
    ai_algorithm = "minimax"  # For human_vs_ai: which algorithm AI uses
    white_algorithm = "minimax"  # For ai_vs_ai: algorithm for white/player1
    black_algorithm = "mcts"  # For ai_vs_ai: algorithm for black/player2

    # Helper to draw text
    def draw_text(center_x, center_y, text, size=28, color=(0, 0, 0)):
        font = pygame.font.SysFont('freesansbold.ttf', size)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(center_x, center_y))
        screen.blit(surf, rect)

    # Developer text (from original)
    def print_developer_name():
        font1 = pygame.font.Font('freesansbold.ttf', 16)
        text1 = font1.render('Developed By', True, (0, 200, 83))
        textRect1 = text1.get_rect()
        textRect1.center = (980, 730)

        font2 = pygame.font.Font('freesansbold.ttf', 20)
        text2 = font2.render('Ryad & Faruk', True, (0, 200, 83))
        textRect2 = text2.get_rect()
        textRect2.center = (980, 760)
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)

    # --- Menu Loop: choose mode + grid size ---
    while not game_ready:
        # Main menu selection
        while selecting:
            screen.fill((255, 255, 255))
            # Background image (keep)
            try:
                back_ground = pygame.image.load(r"Image/First_Page.png")
                screen.blit(back_ground, (0, 0))
            except:
                # fallback if image missing
                pass

            # Mode buttons rectangles
            hvh_rect = pygame.Rect(320, 260, 440, 60)
            hvai_rect = pygame.Rect(320, 340, 440, 60)
            aivai_rect = pygame.Rect(320, 420, 440, 60)

            # Draw mode buttons with hover effect
            mouse_pos = pygame.mouse.get_pos()
            
            # Human vs Human button
            if hvh_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (180, 230, 180), hvh_rect, border_radius=8)
            else:
                pygame.draw.rect(screen, (200, 200, 200), hvh_rect, border_radius=8)
            
            # Human vs AI button  
            if hvai_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (180, 230, 180), hvai_rect, border_radius=8)
            else:
                pygame.draw.rect(screen, (200, 200, 200), hvai_rect, border_radius=8)
            
            # AI vs AI button
            if aivai_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (180, 230, 180), aivai_rect, border_radius=8)
            else:
                pygame.draw.rect(screen, (200, 200, 200), aivai_rect, border_radius=8)

            draw_text(540, 290, "Human  vs  Human", 32)
            draw_text(540, 370, "Human  vs  AI", 32)
            draw_text(540, 450, "AI  vs  AI", 32)

            # Grid selection
            draw_text(540, 530, "Choose Grid Size: 4   6   8 (Click icons below)", 22)
            
            # Grid selection buttons with visual feedback
            grid4_rect = pygame.Rect(420, 560, 70, 40)
            grid6_rect = pygame.Rect(500, 560, 70, 40)
            grid8_rect = pygame.Rect(580, 560, 70, 40)
            
            # Draw grid buttons with selection feedback
            grid4_color = (100, 255, 100) if grid_size == 4 else (180, 230, 180) if grid4_rect.collidepoint(mouse_pos) else (230, 230, 230)
            grid6_color = (100, 255, 100) if grid_size == 6 else (180, 230, 180) if grid6_rect.collidepoint(mouse_pos) else (230, 230, 230)
            grid8_color = (100, 255, 100) if grid_size == 8 else (180, 230, 180) if grid8_rect.collidepoint(mouse_pos) else (230, 230, 230)
            
            pygame.draw.rect(screen, grid4_color, grid4_rect, border_radius=5)
            pygame.draw.rect(screen, grid6_color, grid6_rect, border_radius=5)
            pygame.draw.rect(screen, grid8_color, grid8_rect, border_radius=5)
            
            # Add border to selected grid size
            if grid_size == 4:
                pygame.draw.rect(screen, (0, 150, 0), grid4_rect, 3, border_radius=5)
            if grid_size == 6:
                pygame.draw.rect(screen, (0, 150, 0), grid6_rect, 3, border_radius=5)
            if grid_size == 8:
                pygame.draw.rect(screen, (0, 150, 0), grid8_rect, 3, border_radius=5)
                
            draw_text(grid4_rect.centerx, grid4_rect.centery, "4", 26, (0, 0, 0))
            draw_text(grid6_rect.centerx, grid6_rect.centery, "6", 26, (0, 0, 0))
            draw_text(grid8_rect.centerx, grid8_rect.centery, "8", 26, (0, 0, 0))

            print_developer_name()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Play click sound for any button press
                    button_click_sound.play()
                    
                    if hvh_rect.collidepoint(event.pos):
                        game_mode = "human_vs_human"
                        pygame.mixer.music.stop() 
                        selecting = False
                    elif hvai_rect.collidepoint(event.pos):
                        game_mode = "human_vs_ai"
                        # Don't stop selecting yet - need to choose color and AI
                        selecting = False
                    elif aivai_rect.collidepoint(event.pos):
                        game_mode = "ai_vs_ai"
                        # Don't stop selecting yet - need to choose algorithms
                        selecting = False
                    elif grid4_rect.collidepoint(event.pos):
                        grid_size = 4
                        # Visual feedback - briefly change color
                        pygame.draw.rect(screen, (150, 255, 150), grid4_rect, border_radius=5)
                        pygame.draw.rect(screen, (0, 150, 0), grid4_rect, 3, border_radius=5)
                        draw_text(grid4_rect.centerx, grid4_rect.centery, "4", 26, (0, 0, 0))
                        pygame.display.flip()
                        time.sleep(0.1)
                    elif grid6_rect.collidepoint(event.pos):
                        grid_size = 6
                        # Visual feedback - briefly change color
                        pygame.draw.rect(screen, (150, 255, 150), grid6_rect, border_radius=5)
                        pygame.draw.rect(screen, (0, 150, 0), grid6_rect, 3, border_radius=5)
                        draw_text(grid6_rect.centerx, grid6_rect.centery, "6", 26, (0, 0, 0))
                        pygame.display.flip()
                        time.sleep(0.1)
                    elif grid8_rect.collidepoint(event.pos):
                        grid_size = 8
                        # Visual feedback - briefly change color
                        pygame.draw.rect(screen, (150, 255, 150), grid8_rect, border_radius=5)
                        pygame.draw.rect(screen, (0, 150, 0), grid8_rect, 3, border_radius=5)
                        draw_text(grid8_rect.centerx, grid8_rect.centery, "8", 26, (0, 0, 0))
                        pygame.display.flip()
                        time.sleep(0.1)

            clock.tick(FPS)

        # --- Second Menu: Algorithm and Color Selection (for human_vs_ai and ai_vs_ai) ---
        if game_mode in ["human_vs_ai", "ai_vs_ai"]:
            selecting_options = True
            
            while selecting_options:
                screen.fill((255, 255, 255))
                try:
                    back_ground = pygame.image.load(r"Image/First_Page.png")
                    screen.blit(back_ground, (0, 0))
                except:
                    pass
                
                mouse_pos = pygame.mouse.get_pos()
                
                if game_mode == "human_vs_ai":
                    # Human vs AI: Choose color and AI algorithm
                    draw_text(540, 150, "Human vs AI Setup", 36, (0, 100, 200))
                    
                    # Color selection
                    draw_text(540, 220, "Choose Your Color:", 28)
                    white_btn = pygame.Rect(380, 250, 140, 50)
                    black_btn = pygame.Rect(560, 250, 140, 50)
                    
                    # Color buttons
                    if human_color == HUMAN:
                        pygame.draw.rect(screen, (100, 255, 100), white_btn, border_radius=8)
                        pygame.draw.rect(screen, (0, 150, 0), white_btn, 3, border_radius=8)
                    else:
                        col = (180, 230, 180) if white_btn.collidepoint(mouse_pos) else (220, 220, 220)
                        pygame.draw.rect(screen, col, white_btn, border_radius=8)
                    
                    if human_color == COMPUTER:
                        pygame.draw.rect(screen, (100, 255, 100), black_btn, border_radius=8)
                        pygame.draw.rect(screen, (0, 150, 0), black_btn, 3, border_radius=8)
                    else:
                        col = (180, 230, 180) if black_btn.collidepoint(mouse_pos) else (220, 220, 220)
                        pygame.draw.rect(screen, col, black_btn, border_radius=8)
                    
                    draw_text(white_btn.centerx, white_btn.centery, "White", 24)
                    draw_text(black_btn.centerx, black_btn.centery, "Black", 24)
                    
                    # AI Algorithm selection
                    draw_text(540, 340, "Choose AI Algorithm:", 28)
                    greedy_btn = pygame.Rect(280, 380, 160, 50)
                    minimax_btn = pygame.Rect(460, 380, 160, 50)
                    mcts_btn = pygame.Rect(640, 380, 160, 50)
                    
                    # AI algorithm buttons
                    for btn, name in [(greedy_btn, "greedy"), (minimax_btn, "minimax"), (mcts_btn, "mcts")]:
                        if ai_algorithm == name:
                            pygame.draw.rect(screen, (100, 200, 255), btn, border_radius=8)
                            pygame.draw.rect(screen, (0, 100, 200), btn, 3, border_radius=8)
                        else:
                            col = (150, 210, 255) if btn.collidepoint(mouse_pos) else (200, 220, 240)
                            pygame.draw.rect(screen, col, btn, border_radius=8)
                    
                    draw_text(greedy_btn.centerx, greedy_btn.centery, "Greedy", 22)
                    draw_text(minimax_btn.centerx, minimax_btn.centery, "Minimax", 22)
                    draw_text(mcts_btn.centerx, mcts_btn.centery, "MCTS", 22)
                    
                    # Difficulty labels
                    #draw_text(greedy_btn.centerx, greedy_btn.bottom + 15, "(Easy)", 16, (100, 100, 100))
                    #draw_text(minimax_btn.centerx, minimax_btn.bottom + 15, "(Medium)", 16, (100, 100, 100))
                    #draw_text(mcts_btn.centerx, mcts_btn.bottom + 15, "(Hard)", 16, (100, 100, 100))
                    
                    # Start button
                    start_btn = pygame.Rect(440, 500, 200, 60)
                    col = (100, 255, 100) if start_btn.collidepoint(mouse_pos) else (150, 255, 150)
                    pygame.draw.rect(screen, col, start_btn, border_radius=10)
                    pygame.draw.rect(screen, (0, 150, 0), start_btn, 3, border_radius=10)
                    draw_text(start_btn.centerx, start_btn.centery, "START GAME", 28, (0, 100, 0))
                    
                    # Back button
                    back_btn = pygame.Rect(240, 500, 150, 60)
                    col = (255, 150, 150) if back_btn.collidepoint(mouse_pos) else (255, 200, 200)
                    pygame.draw.rect(screen, col, back_btn, border_radius=10)
                    pygame.draw.rect(screen, (200, 0, 0), back_btn, 3, border_radius=10)
                    draw_text(back_btn.centerx, back_btn.centery, "BACK", 28, (150, 0, 0))
                    
                elif game_mode == "ai_vs_ai":
                    # AI vs AI: Choose algorithms for both sides
                    draw_text(540, 150, "AI vs AI Setup", 36, (0, 100, 200))
                    
                    # White side algorithm
                    draw_text(540, 220, "White Side Algorithm:", 28)
                    w_greedy_btn = pygame.Rect(280, 250, 160, 50)
                    w_minimax_btn = pygame.Rect(460, 250, 160, 50)
                    w_mcts_btn = pygame.Rect(640, 250, 160, 50)
                    
                    for btn, name in [(w_greedy_btn, "greedy"), (w_minimax_btn, "minimax"), (w_mcts_btn, "mcts")]:
                        if white_algorithm == name:
                            pygame.draw.rect(screen, (255, 220, 100), btn, border_radius=8)
                            pygame.draw.rect(screen, (200, 150, 0), btn, 3, border_radius=8)
                        else:
                            col = (255, 240, 180) if btn.collidepoint(mouse_pos) else (240, 230, 210)
                            pygame.draw.rect(screen, col, btn, border_radius=8)
                    
                    draw_text(w_greedy_btn.centerx, w_greedy_btn.centery, "Greedy", 22)
                    draw_text(w_minimax_btn.centerx, w_minimax_btn.centery, "Minimax", 22)
                    draw_text(w_mcts_btn.centerx, w_mcts_btn.centery, "MCTS", 22)
                    
                    # Black side algorithm
                    draw_text(540, 340, "Black Side Algorithm:", 28)
                    b_greedy_btn = pygame.Rect(280, 370, 160, 50)
                    b_minimax_btn = pygame.Rect(460, 370, 160, 50)
                    b_mcts_btn = pygame.Rect(640, 370, 160, 50)
                    
                    for btn, name in [(b_greedy_btn, "greedy"), (b_minimax_btn, "minimax"), (b_mcts_btn, "mcts")]:
                        if black_algorithm == name:
                            pygame.draw.rect(screen, (180, 180, 180), btn, border_radius=8)
                            pygame.draw.rect(screen, (80, 80, 80), btn, 3, border_radius=8)
                        else:
                            col = (200, 200, 200) if btn.collidepoint(mouse_pos) else (230, 230, 230)
                            pygame.draw.rect(screen, col, btn, border_radius=8)
                    
                    draw_text(b_greedy_btn.centerx, b_greedy_btn.centery, "Greedy", 22)
                    draw_text(b_minimax_btn.centerx, b_minimax_btn.centery, "Minimax", 22)
                    draw_text(b_mcts_btn.centerx, b_mcts_btn.centery, "MCTS", 22)
                    
                    # Start button
                    start_btn = pygame.Rect(440, 480, 200, 60)
                    col = (100, 255, 100) if start_btn.collidepoint(mouse_pos) else (150, 255, 150)
                    pygame.draw.rect(screen, col, start_btn, border_radius=10)
                    pygame.draw.rect(screen, (0, 150, 0), start_btn, 3, border_radius=10)
                    draw_text(start_btn.centerx, start_btn.centery, "START GAME", 28, (0, 100, 0))
                    
                    # Back button
                    back_btn = pygame.Rect(240, 480, 150, 60)
                    col = (255, 150, 150) if back_btn.collidepoint(mouse_pos) else (255, 200, 200)
                    pygame.draw.rect(screen, col, back_btn, border_radius=10)
                    pygame.draw.rect(screen, (200, 0, 0), back_btn, 3, border_radius=10)
                    draw_text(back_btn.centerx, back_btn.centery, "BACK", 28, (150, 0, 0))
                
                print_developer_name()
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        button_click_sound.play()
                        
                        if game_mode == "human_vs_ai":
                            if white_btn.collidepoint(event.pos):
                                human_color = HUMAN
                            elif black_btn.collidepoint(event.pos):
                                human_color = COMPUTER
                            elif greedy_btn.collidepoint(event.pos):
                                ai_algorithm = "greedy"
                            elif minimax_btn.collidepoint(event.pos):
                                ai_algorithm = "minimax"
                            elif mcts_btn.collidepoint(event.pos):
                                ai_algorithm = "mcts"
                            elif start_btn.collidepoint(event.pos):
                                selecting_options = False
                                pygame.mixer.music.stop()
                                game_ready = True  # Ready to start game
                            elif back_btn.collidepoint(event.pos):
                                # Go back to main menu
                                selecting_options = False
                                selecting = True
                                game_mode = None
                        
                        elif game_mode == "ai_vs_ai":
                            if w_greedy_btn.collidepoint(event.pos):
                                white_algorithm = "greedy"
                            elif w_minimax_btn.collidepoint(event.pos):
                                white_algorithm = "minimax"
                            elif w_mcts_btn.collidepoint(event.pos):
                                white_algorithm = "mcts"
                            elif b_greedy_btn.collidepoint(event.pos):
                                black_algorithm = "greedy"
                            elif b_minimax_btn.collidepoint(event.pos):
                                black_algorithm = "minimax"
                            elif b_mcts_btn.collidepoint(event.pos):
                                black_algorithm = "mcts"
                            elif start_btn.collidepoint(event.pos):
                                selecting_options = False
                                pygame.mixer.music.stop()
                                game_ready = True  # Ready to start game
                            elif back_btn.collidepoint(event.pos):
                                # Go back to main menu
                                selecting_options = False
                                selecting = True
                                game_mode = None
                
                clock.tick(FPS)
        else:
            # Human vs Human - no algorithm selection needed
            pygame.mixer.music.stop()
            game_ready = True
    
    # --- Setup board and images ---
    square_size = 80
    board = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    center = grid_size // 2
    board[center - 1][center - 1], board[center][center] = 1, 1
    board[center - 1][center], board[center][center - 1] = -1, -1

    # Player images
    try:
        human_pic = pygame.image.load(r"Image/human.png")
        computer_pic = pygame.image.load(r"Image/robot.png")
    except:
        human_pic = pygame.Surface((40, 40))
        human_pic.fill((100, 100, 255))
        computer_pic = pygame.Surface((40, 40))
        computer_pic.fill((255, 100, 100))

    human_x = 60
    human_y = 30
    computer_x = 150
    computer_y = 30

    def player_draw():
        # Display icons based on game mode
        if game_mode == "human_vs_human":
            # Show two human icons
            screen.blit(human_pic, (human_x, human_y))
            screen.blit(human_pic, (computer_x, computer_y))
        elif game_mode == "human_vs_ai":
            # Show human and robot based on chosen color
            # human_x is for white/left side (HUMAN = 1)
            # computer_x is for black/right side (COMPUTER = -1)
            if human_color == HUMAN:
                # Human chose white, AI is black
                screen.blit(human_pic, (human_x, human_y))
                screen.blit(computer_pic, (computer_x, computer_y))
            else:
                # Human chose black, AI is white
                screen.blit(computer_pic, (human_x, human_y))
                screen.blit(human_pic, (computer_x, computer_y))
        elif game_mode == "ai_vs_ai":
            # Show two robot icons
            screen.blit(computer_pic, (human_x, human_y))
            screen.blit(computer_pic, (computer_x, computer_y))

    def get_score():
        score_human = 0
        score_computer = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if board[i][j] == HUMAN:
                    score_human += 1
                elif board[i][j] == COMPUTER:
                    score_computer += 1
        return (score_human, score_computer)

    def print_score():
        my_font = pygame.font.SysFont('Comic Sans MS', 20)
        score_h, score_c = get_score()
        text_surface = my_font.render('Score: {}      :      {}'.format(score_h, score_c), False, (0, 0, 0))
        screen.blit(text_surface, (10, 90))

    turn = HUMAN  # 1 = Human, -1 = AI/other

    cell = 80
    shift_right = (1080 - (grid_size * 80)) // 2
    shift_down = 100

    # Load tile/disc images once to avoid reloading each draw
    def load_image_or_empty(path, fallback_size=(80, 80)):
        try:
            return pygame.image.load(path)
        except:
            surf = pygame.Surface(fallback_size)
            surf.fill((200, 200, 200))
            return surf

    empty_image = load_image_or_empty(r"Image/empty.png")
    white_image = load_image_or_empty(r"Image/4.png")
    black_image = load_image_or_empty(r"Image/1.png")
    show_move_image = load_image_or_empty(r"Image/sMove.png", (40, 40))

    def draw_board(screen, valid_h):
        for i in range(grid_size):
            for j in range(grid_size):
                screen.blit(empty_image, (i * cell + shift_right, j * cell + shift_down))
                if board[i][j] == 1:
                    screen.blit(white_image, (i * cell + shift_right, j * cell + shift_down))
                elif board[i][j] == -1:
                    screen.blit(black_image, (i * cell + shift_right, j * cell + shift_down))
        for x, y in valid_h:
            # show possible moves
            screen.blit(show_move_image, (x * cell + shift_right + (cell - show_move_image.get_width()) // 2,
                                          y * cell + shift_down + (cell - show_move_image.get_height()) // 2))

    # Returns list of all valid move coordinates
    def get_valid_moves(board_state, player):
        val_m = []
        for i in range(grid_size):
            for j in range(grid_size):
                if board_state[i][j] == 0:
                    if is_valid_move(board_state, i, j, player):
                        val_m.append((i, j))
        return val_m

    # Returns True if valid move found in any direction, False otherwise
    def is_valid_move(board_state, x, y, player):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                opp = False
                while 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if board_state[nx][ny] == -player:
                        opp = True
                    elif board_state[nx][ny] == player and opp:
                        return True
                    else:
                        break
                    nx, ny = nx + dx, ny + dy
        return False

    def flip_pieces(board_state, x, y, player):
        flipped_board = deep_copy(board_state)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                flip = False
                while 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if flipped_board[nx][ny] == -player:
                        flip = True
                    elif flipped_board[nx][ny] == player and flip:
                        # Flip back along the line
                        while (nx, ny) != (x + dx, y + dy):
                            nx, ny = nx - dx, ny - dy
                            flipped_board[nx][ny] = player
                        break
                    else:
                        break
                    nx, ny = nx + dx, ny + dy
        return flipped_board

    # This modifies the actual board and returns flipped positions
    def flip_piecehuman(x, y, player):
        flipped_indices = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                flip = False
                while 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if board[nx][ny] == -player:
                        flip = True
                    elif board[nx][ny] == player and flip:
                        while (nx, ny) != (x + dx, y + dy):
                            nx, ny = nx - dx, ny - dy
                            flipped_indices.append((nx, ny))
                            board[nx][ny] = player
                        break
                    else:
                        break
                    nx, ny = nx + dx, ny + dy
        return flipped_indices

    def is_game_over(board_state):
        if len(get_valid_moves(board_state, HUMAN)) == 0 and len(get_valid_moves(board_state, COMPUTER)) == 0:
            return True
        for row in board_state:
            if 0 in row:
                return False
        return True

    # Animation for flipping pieces (keeps original style)
    def flip_animation(tmp, t):
        # load frames depending on t
        try:
            if t == HUMAN:
                img1 = pygame.image.load(r"Image/1.png")
                img2 = pygame.image.load(r"Image/2.png")
                img3 = pygame.image.load(r"Image/3.png")
                img4 = pygame.image.load(r"Image/4.png")
            else:
                img1 = pygame.image.load(r"Image/4.png")
                img2 = pygame.image.load(r"Image/3.png")
                img3 = pygame.image.load(r"Image/2.png")
                img4 = pygame.image.load(r"Image/1.png")
        except:
            img1 = img2 = img3 = img4 = white_image

        for img, delay in [(img1, 0.08), (img2, 0.12), (img3, 0.12), (img4, 0.08)]:
            for (x, y) in tmp:
                screen.blit(img, (x * cell + shift_right, y * cell + shift_down))
            pygame.display.update()
            time.sleep(delay)

    # Simple score calc used by minimax
    def calc_score(board_state, player):
        score = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if board_state[i][j] == player:
                    score += 1
                elif board_state[i][j] == -player:
                    score -= 1
        return score

    # ---------- Minimax with Heuristic Evaluation ----------
    def minimax(board_state, depth, player, alpha, beta, max_depth):
        if depth == 0 or is_game_over(board_state) or depth == max_depth:
            # Enhanced evaluation: coin count + positional heuristic
            coin_score = calc_score(board_state, player)
            position_score = heuristic_evaluation(board_state, player)
            # Weight the heuristic (0.3 factor for balance)
            return coin_score + position_score * 0.3

        if player == -1:
            b_s = float('inf')
            valid_moves = get_valid_moves(board_state, player)
            if not valid_moves:
                # pass
                return minimax(board_state, depth - 1, -player, alpha, beta, max_depth)
            for move in valid_moves:
                temp_board = deep_copy(board_state)
                flipped_board = flip_pieces(temp_board, move[0], move[1], player)
                flipped_board[move[0]][move[1]] = player
                sr = minimax(flipped_board, depth - 1, -player, alpha, beta, max_depth)
                if sr < b_s:
                    b_s = sr
                if b_s <= alpha:
                    return b_s
                if b_s < beta:
                    beta = b_s
            return b_s
        else:
            b_s = float('-inf')
            valid_moves = get_valid_moves(board_state, player)
            if not valid_moves:
                return minimax(board_state, depth - 1, -player, alpha, beta, max_depth)
            for move in valid_moves:
                temp_board = deep_copy(board_state)
                flipped_board = flip_pieces(temp_board, move[0], move[1], player)
                flipped_board[move[0]][move[1]] = player
                sr = minimax(flipped_board, depth - 1, -player, alpha, beta, max_depth)
                if sr > b_s:
                    b_s = sr
                if b_s >= beta:
                    return b_s
                if b_s > alpha:
                    alpha = b_s
            return b_s

    # ---------- MCTS Implementation ----------
    class MCTSNode:
        def __init__(self, board_state, player, parent=None, move=None, original_player=None):
            self.board = deep_copy(board_state)
            self.player = player  # player who will move at this node
            self.parent = parent
            self.move = move  # move that led to this node (x,y)
            self.children = []
            self.visits = 0
            self.wins = 0.0  # from perspective of original_player (the AI making the decision)

        def is_fully_expanded(self):
            possible = get_valid_moves(self.board, self.player)
            return len(self.children) >= len(possible)

        def uct_score(self, c=1.41):
            if self.visits == 0:
                return float('inf')
            
            if self.parent is None:
                # Root node
                return self.wins / self.visits if self.visits > 0 else 0
            
            # Pure UCT formula: exploitation + exploration (no heuristic bias)
            exploitation = self.wins / self.visits
            exploration = c * math.sqrt(math.log(self.parent.visits) / self.visits)
            return exploitation + exploration

    # Returns the new child node or None if no new moves available
    def mcts_expand(node, original_player=None):
        moves = get_valid_moves(node.board, node.player)
        tried = [child.move for child in node.children]
        for move in moves:
            if move not in tried:
                # create new child for this move
                new_board = flip_pieces(deep_copy(node.board), move[0], move[1], node.player)
                new_board[move[0]][move[1]] = node.player
                child = MCTSNode(new_board, -node.player, parent=node, move=move, original_player=original_player)
                node.children.append(child)
                return child
        return None

    # Returns result (HUMAN/COMPUTER/0) based on:
    # > Final score if game completed
    # > Heuristic evaluation if depth limit reached
    def random_playout(board_state, player, depth_limit=MCTS_SIMULATION_DEPTH):
        """
        Pure random playout with heuristic evaluation at depth limit
        - Plays random moves up to depth_limit
        - If depth limit reached: evaluate position heuristically
        - If game ends naturally: use actual winner
        """
        b = deep_copy(board_state)
        p = player
        count = 0
        
        while not is_game_over(b) and count < depth_limit:
            moves = get_valid_moves(b, p)
            if not moves:
                p = -p
                count += 1
                continue
            
            # Pure random selection
            mv = random.choice(moves)
            
            b = flip_pieces(b, mv[0], mv[1], p)
            b[mv[0]][mv[1]] = p
            p = -p
            count += 1
        
        # Determine winner
        if is_game_over(b):
            # Game ended naturally - use actual score
            final_score = get_score_static(b)
            if final_score[0] > final_score[1]:
                return HUMAN
            elif final_score[1] > final_score[0]:
                return COMPUTER
            return 0
        else:
            # Depth limit reached - use heuristic evaluation
            # Evaluate from both perspectives and determine predicted winner
            eval_white = calc_score(b, HUMAN) + heuristic_evaluation(b, HUMAN) * 0.3
            eval_black = calc_score(b, COMPUTER) + heuristic_evaluation(b, COMPUTER) * 0.3
            
            if eval_white > eval_black:
                return HUMAN
            elif eval_black > eval_white:
                return COMPUTER
            return 0

    # Updates statistics up the tree after simulation
    def backpropagate(node, result, original_player):
        """
        Backpropagate wins from the perspective of original_player (the AI making the decision)
        Every node stores wins from original_player's perspective
        """
        while node is not None:
            node.visits += 1
            
            # Always update from original_player's perspective
            if result == original_player:
                node.wins += 1.0  # AI won - reward!
            elif result == -original_player:
                node.wins += 0.0  # AI lost - punishment (no reward)
            else:
                node.wins += 0.5  # Tie - partial reward
            
            node = node.parent

    def get_score_static(board_state):
        s_h = 0
        s_c = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if board_state[i][j] == HUMAN:
                    s_h += 1
                elif board_state[i][j] == COMPUTER:
                    s_c += 1
        return (s_h, s_c)

    # Returns best move based on most visited child
    def mcts_move(root_board, player, iterations=MCTS_ITERATIONS):
        root = MCTSNode(root_board, player, original_player=player)
        for _ in range(iterations):
            # 1. Selection
            node = root
            while node.children:
                node = max(node.children, key=lambda n: n.uct_score())

            # 2. Expansion
            if not is_game_over(node.board):
                child = mcts_expand(node, original_player=player)
                if child:
                    node = child

            # 3. Simulation
            # simulate from node.board and node.player
            result = random_playout(node.board, node.player)

            # 4. Backpropagation
            backpropagate(node, result, original_player=player)

        # pick child with max visits or max wins
        if not root.children:
            return None
        best = max(root.children, key=lambda c: c.visits)
        return best.move

    # ---------- Heuristic weights for alternate AI (optional usage in playouts) ----------
    # (Not strictly necessary for MCTS, but useful if we implement heuristic playouts)
    def position_value(i, j):
        # simple weight map scaled to grid_size
        # corners strongly positive, adjacent to corners negative, edges positive
        # create a generic map based on normalized distances
        corner_bonus = 100
        edge_bonus = 10
        center_bonus = 1
        if (i == 0 or i == grid_size - 1) and (j == 0 or j == grid_size - 1):
            return corner_bonus
        if (i == 0 or i == grid_size - 1) or (j == 0 or j == grid_size - 1):
            return edge_bonus
        return center_bonus

    def heuristic_evaluation(board_state, player):
        total = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if board_state[i][j] == player:
                    total += position_value(i, j)
                elif board_state[i][j] == -player:
                    total -= position_value(i, j)
        return total

    # ---------- Greedy AI Algorithm ----------
    def greedy_move(board_state, player):
        """
        Greedy AI: Chooses move with best immediate heuristic value
        (coin count + positional advantage)
        """
        valid_moves = get_valid_moves(board_state, player)
        if not valid_moves:
            return None
        
        best_move = None
        best_score = float('-inf')
        
        for move in valid_moves:
            # Simulate the move
            temp_board = flip_pieces(deep_copy(board_state), move[0], move[1], player)
            temp_board[move[0]][move[1]] = player
            
            # Evaluate based on coin count + position value
            score = calc_score(temp_board, player) + heuristic_evaluation(temp_board, player) * 0.1
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
        nonlocal turn
        move = mcts_move(board, COMPUTER, iterations=iterations)
        if move is None:
            # pass
            turn = -turn
            return
        tmp = flip_piecehuman(move[0], move[1], COMPUTER)
        screen.blit(black_image, (move[0] * cell + shift_right, move[1] * cell + shift_down))
        pygame.display.flip()
        flip_animation(tmp, COMPUTER)
        board[move[0]][move[1]] = COMPUTER
        turn = -turn
        click_sound.play()  # ADDED: Sound for AI move
        time.sleep(0.12)

    # ---------- Universal AI Move Handler ----------
    def handle_ai_move(player, algorithm):
        """
        Universal AI move handler
        player: HUMAN (1) or COMPUTER (-1)
        algorithm: "greedy", "minimax", or "mcts"
        """
        nonlocal turn
        
        # Check if player has valid moves first
        valid_moves = get_valid_moves(board, player)
        if not valid_moves:
            # No valid moves - must pass turn
            show_pass_message(player, algorithm)
            turn = -turn
            return
        
        # Get the move based on algorithm
        if algorithm == "greedy":
            move = greedy_move(board, player)
        elif algorithm == "minimax":
            # Use minimax
            b_s = float('-inf')
            move = None
            for m in valid_moves:
                temp_board = deep_copy(board)
                flipped_board = flip_pieces(temp_board, m[0], m[1], player)
                flipped_board[m[0]][m[1]] = player
                score = minimax(flipped_board, 3, -player, float('-inf'), float('inf'), 4)
                if score >= b_s:
                    b_s = score
                    move = m
        elif algorithm == "mcts":
            move = mcts_move(board, player, iterations=MCTS_ITERATIONS)
        else:
            move = None
        
        # Execute the move if valid
        if move is None:
            # Algorithm failed to find move (shouldn't happen if valid_moves exists)
            show_pass_message(player, algorithm)
            turn = -turn
            return
        
        tmp = flip_piecehuman(move[0], move[1], player)
        img = white_image if player == HUMAN else black_image
        screen.blit(img, (move[0] * cell + shift_right, move[1] * cell + shift_down))
        pygame.display.flip()
        flip_animation(tmp, player)
        board[move[0]][move[1]] = player
        turn = -turn
        click_sound.play()
        time.sleep(0.15)
    
    # Show pass turn message
    def show_pass_message(player, algorithm=None):
        """Display a message when a player must pass their turn"""
        # Determine player name
        if game_mode == "human_vs_human":
            player_name = "Human 1 (White)" if player == HUMAN else "Human 2 (Black)"
        elif game_mode == "human_vs_ai":
            if player == human_color:
                player_name = "Human"
            else:
                algo_name = ai_algorithm.upper() if ai_algorithm == "mcts" else ai_algorithm.capitalize()
                player_name = f"AI ({algo_name})"
        elif game_mode == "ai_vs_ai":
            if player == HUMAN:
                algo_name = white_algorithm.upper() if white_algorithm == "mcts" else white_algorithm.capitalize()
                player_name = f"White AI ({algo_name})"
            else:
                algo_name = black_algorithm.upper() if black_algorithm == "mcts" else black_algorithm.capitalize()
                player_name = f"Black AI ({algo_name})"
        else:
            player_name = "Player"
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((1080, 800))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw message box
        box_width = 500
        box_height = 200
        box_x = (1080 - box_width) // 2
        box_y = (800 - box_height) // 2
        
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(screen, (255, 150, 0), (box_x, box_y, box_width, box_height), 5, border_radius=15)
        
        # Draw text
        font_title = pygame.font.SysFont('freesansbold.ttf', 32, bold=True)
        font_msg = pygame.font.SysFont('freesansbold.ttf', 24)
        
        title_text = font_title.render("NO VALID MOVES", True, (255, 100, 0))
        title_rect = title_text.get_rect(center=(box_x + box_width // 2, box_y + 50))
        
        msg_text = font_msg.render(f"{player_name}", True, (0, 0, 0))
        msg_rect = msg_text.get_rect(center=(box_x + box_width // 2, box_y + 100))
        
        msg_text2 = font_msg.render("must pass the turn", True, (0, 0, 0))
        msg_rect2 = msg_text2.get_rect(center=(box_x + box_width // 2, box_y + 135))
        
        screen.blit(title_text, title_rect)
        screen.blit(msg_text, msg_rect)
        screen.blit(msg_text2, msg_rect2)
        
        pygame.display.flip()
        time.sleep(1.5)  # Show message for 1.5 seconds

    # ---------- Main Game Loop ----------
    game_over = False
    # Different delays for different modes
    if game_mode == "ai_vs_ai":
        ai_auto_delay = 1.2  # Increased delay for AI vs AI to make it more visible
    else:
        ai_auto_delay = 0.3  # Keep original delay for other modes

    last_ai_move_time = time.time()
    
    # Button to switch to AI vs AI mode
    switch_to_ai_button_rect = pygame.Rect(900, 150, 150, 50)
    
    def draw_switch_button():
        # Only show button in human_vs_human or human_vs_ai modes
        if game_mode in ["human_vs_human", "human_vs_ai"]:
            mouse_pos = pygame.mouse.get_pos()
            if switch_to_ai_button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (100, 200, 255), switch_to_ai_button_rect, border_radius=8)
            else:
                pygame.draw.rect(screen, (150, 220, 255), switch_to_ai_button_rect, border_radius=8)
            pygame.draw.rect(screen, (0, 100, 200), switch_to_ai_button_rect, 2, border_radius=8)
            
            font = pygame.font.SysFont('freesansbold.ttf', 18)
            text1 = font.render('Watch AI', True, (0, 0, 0))
            text2 = font.render('Battle!', True, (0, 0, 0))
            text_rect1 = text1.get_rect(center=(switch_to_ai_button_rect.centerx, switch_to_ai_button_rect.centery - 10))
            text_rect2 = text2.get_rect(center=(switch_to_ai_button_rect.centerx, switch_to_ai_button_rect.centery + 10))
            screen.blit(text1, text_rect1)
            screen.blit(text2, text_rect2)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Human moves only accepted when appropriate
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if switch to AI button was clicked
                if switch_to_ai_button_rect.collidepoint(event.pos) and game_mode in ["human_vs_human", "human_vs_ai"]:
                    button_click_sound.play()
                    
                    # Show algorithm selection dialog
                    selecting_switch_ai = True
                    temp_white_algo = "minimax"
                    temp_black_algo = "mcts"
                    
                    while selecting_switch_ai:
                        screen.fill((255, 255, 255))
                        draw_text(540, 150, "Choose AI Algorithms", 36, (0, 100, 200))
                        
                        # White side algorithm
                        draw_text(540, 220, "White Side Algorithm:", 28)
                        w_greedy_btn = pygame.Rect(280, 250, 160, 50)
                        w_minimax_btn = pygame.Rect(460, 250, 160, 50)
                        w_mcts_btn = pygame.Rect(640, 250, 160, 50)
                        
                        m_pos = pygame.mouse.get_pos()
                        for btn, name in [(w_greedy_btn, "greedy"), (w_minimax_btn, "minimax"), (w_mcts_btn, "mcts")]:
                            if temp_white_algo == name:
                                pygame.draw.rect(screen, (255, 220, 100), btn, border_radius=8)
                                pygame.draw.rect(screen, (200, 150, 0), btn, 3, border_radius=8)
                            else:
                                col = (255, 240, 180) if btn.collidepoint(m_pos) else (240, 230, 210)
                                pygame.draw.rect(screen, col, btn, border_radius=8)
                        
                        draw_text(w_greedy_btn.centerx, w_greedy_btn.centery, "Greedy", 22)
                        draw_text(w_minimax_btn.centerx, w_minimax_btn.centery, "Minimax", 22)
                        draw_text(w_mcts_btn.centerx, w_mcts_btn.centery, "MCTS", 22)
                        
                        # Black side algorithm
                        draw_text(540, 340, "Black Side Algorithm:", 28)
                        b_greedy_btn = pygame.Rect(280, 370, 160, 50)
                        b_minimax_btn = pygame.Rect(460, 370, 160, 50)
                        b_mcts_btn = pygame.Rect(640, 370, 160, 50)
                        
                        for btn, name in [(b_greedy_btn, "greedy"), (b_minimax_btn, "minimax"), (b_mcts_btn, "mcts")]:
                            if temp_black_algo == name:
                                pygame.draw.rect(screen, (180, 180, 180), btn, border_radius=8)
                                pygame.draw.rect(screen, (80, 80, 80), btn, 3, border_radius=8)
                            else:
                                col = (200, 200, 200) if btn.collidepoint(m_pos) else (230, 230, 230)
                                pygame.draw.rect(screen, col, btn, border_radius=8)
                        
                        draw_text(b_greedy_btn.centerx, b_greedy_btn.centery, "Greedy", 22)
                        draw_text(b_minimax_btn.centerx, b_minimax_btn.centery, "Minimax", 22)
                        draw_text(b_mcts_btn.centerx, b_mcts_btn.centery, "MCTS", 22)
                        
                        # Start button
                        start_btn = pygame.Rect(490, 480, 150, 60)
                        col = (100, 255, 100) if start_btn.collidepoint(m_pos) else (150, 255, 150)
                        pygame.draw.rect(screen, col, start_btn, border_radius=10)
                        pygame.draw.rect(screen, (0, 150, 0), start_btn, 3, border_radius=10)
                        draw_text(start_btn.centerx, start_btn.centery, "START", 28, (0, 100, 0))
                        
                        # Cancel button
                        cancel_btn = pygame.Rect(320, 480, 150, 60)
                        col = (255, 150, 150) if cancel_btn.collidepoint(m_pos) else (255, 200, 200)
                        pygame.draw.rect(screen, col, cancel_btn, border_radius=10)
                        pygame.draw.rect(screen, (200, 0, 0), cancel_btn, 3, border_radius=10)
                        draw_text(cancel_btn.centerx, cancel_btn.centery, "CANCEL", 28, (150, 0, 0))
                        
                        pygame.display.flip()
                        
                        for evt in pygame.event.get():
                            if evt.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif evt.type == pygame.MOUSEBUTTONDOWN:
                                button_click_sound.play()
                                if w_greedy_btn.collidepoint(evt.pos):
                                    temp_white_algo = "greedy"
                                elif w_minimax_btn.collidepoint(evt.pos):
                                    temp_white_algo = "minimax"
                                elif w_mcts_btn.collidepoint(evt.pos):
                                    temp_white_algo = "mcts"
                                elif b_greedy_btn.collidepoint(evt.pos):
                                    temp_black_algo = "greedy"
                                elif b_minimax_btn.collidepoint(evt.pos):
                                    temp_black_algo = "minimax"
                                elif b_mcts_btn.collidepoint(evt.pos):
                                    temp_black_algo = "mcts"
                                elif start_btn.collidepoint(evt.pos):
                                    selecting_switch_ai = False
                                elif cancel_btn.collidepoint(evt.pos):
                                    # Cancel the switch - stay in current mode
                                    selecting_switch_ai = False
                                    temp_white_algo = None  # Mark as cancelled
                        
                        clock.tick(FPS)
                    
                    # Apply the selections only if not cancelled
                    if temp_white_algo is not None:
                        white_algorithm = temp_white_algo
                        black_algorithm = temp_black_algo
                        game_mode = "ai_vs_ai"
                        ai_auto_delay = 1.2
                        last_ai_move_time = time.time()
                    continue  # Skip other mouse handling for this click
                
                if game_mode == "human_vs_human":
                    # both players are human; allow either to click but must be valid move
                    x, y = event.pos
                    x -= shift_right
                    y -= shift_down
                    i, j = int(x // square_size), int(y // square_size)
                    if 0 <= i < grid_size and 0 <= j < grid_size:
                        if (i, j) in get_valid_moves(board, turn):
                            tmp = flip_piecehuman(i, j, turn)
                            img = white_image if turn == HUMAN else black_image
                            screen.blit(img, (i * cell + shift_right, j * cell + shift_down))
                            time.sleep(0.1)
                            pygame.display.flip()
                            flip_animation(tmp, turn)
                            board[i][j] = turn
                            turn = -turn
                            click_sound.play()
                            time.sleep(0.05)
                elif game_mode == "human_vs_ai":
                    # Handle click based on human's chosen color
                    if turn == human_color:
                        x, y = event.pos
                        x -= shift_right
                        y -= shift_down
                        i, j = int(x // square_size), int(y // square_size)
                        if 0 <= i < grid_size and 0 <= j < grid_size:
                            if (i, j) in get_valid_moves(board, human_color):
                                tmp = flip_piecehuman(i, j, human_color)
                                img = white_image if human_color == HUMAN else black_image
                                screen.blit(img, (i * cell + shift_right, j * cell + shift_down))
                                pygame.display.flip()
                                flip_animation(tmp, human_color)
                                board[i][j] = human_color
                                turn = -turn
                                click_sound.play()
                                time.sleep(0.15)

        # Automatic AI actions based on mode
        now = time.time()
        if game_mode == "human_vs_ai":
            # AI plays when it's not human's turn
            ai_player = -human_color
            if turn == ai_player and not is_game_over(board):
                if now - last_ai_move_time > ai_auto_delay:
                    handle_ai_move(ai_player, ai_algorithm)
                    last_ai_move_time = now

        elif game_mode == "ai_vs_ai":
            # Both players are AI with selected algorithms
            if now - last_ai_move_time > ai_auto_delay and not is_game_over(board):
                if turn == HUMAN:
                    # White side uses white_algorithm
                    handle_ai_move(HUMAN, white_algorithm)
                    last_ai_move_time = now
                else:
                    # Black side uses black_algorithm
                    handle_ai_move(COMPUTER, black_algorithm)
                    last_ai_move_time = now

        # Check end conditions and passing logic
        valid_moves_h = get_valid_moves(board, HUMAN)
        valid_moves_c = get_valid_moves(board, COMPUTER)
        if is_game_over(board):
            game_over = True
        else:
            # If current player has no moves, show pass message and switch turn
            if turn == HUMAN and not valid_moves_h:
                if not valid_moves_c:
                    game_over = True
                else:
                    # Show pass message for human player in human_vs_human mode
                    if game_mode == "human_vs_human":
                        show_pass_message(HUMAN)
                    turn = COMPUTER
            elif turn == COMPUTER and not valid_moves_c:
                if not valid_moves_h:
                    game_over = True
                else:
                    # Show pass message for human player 2 in human_vs_human mode
                    if game_mode == "human_vs_human":
                        show_pass_message(COMPUTER)
                    turn = HUMAN

        # Draw loop updates
        screen.fill((255, 255, 255))
        player_draw()
        if not game_over:
            current_valid = get_valid_moves(board, turn) if (game_mode != "ai_vs_ai" or turn == HUMAN and game_mode == "ai_vs_ai") else []
            # For human_vs_human show valid moves for current human only if a human can act
            if game_mode == "human_vs_human":
                current_valid = get_valid_moves(board, turn)
            elif game_mode == "human_vs_ai":
                # show valid moves only when human's turn
                current_valid = get_valid_moves(board, human_color) if turn == human_color else []
            elif game_mode == "ai_vs_ai":
                # hide move hints during AI-vs-AI for clarity (or show none)
                current_valid = []
            draw_board(screen, current_valid)
            print_score()
            draw_switch_button()  # Draw the switch button
            print_developer_name()
            pygame.display.flip()

        clock.tick(FPS)

    # ---------- Game Over Screen ----------
    if game_over:
        score_human, score_computer = get_score()
        try:
            winner_image = pygame.image.load(r"Image/winner1.png")
            defeat_image = pygame.image.load(r"Image/defeat.png")
            tie_image = pygame.image.load(r"Image/match_tie.png")
            replay_img = pygame.image.load(r"Image/replay.png")
            switch_img = pygame.image.load(r"Image/switch.png")
        except:
            winner_image = defeat_image = tie_image = pygame.Surface((200, 120))
            winner_image.fill((0, 255, 0))
            defeat_image.fill((255, 0, 0))
            tie_image.fill((200, 200, 200))
            replay_img = pygame.Surface((64, 64)); replay_img.fill((100, 200, 100))
            switch_img = pygame.Surface((64, 64)); switch_img.fill((200, 100, 100))

        screen.fill((255, 255, 255))
        player_draw()
        print_score()
        
        # Determine winner message based on game mode
        if game_mode == "human_vs_human":
            if score_human > score_computer:
                image = winner_image
                winner = "Human 1"
                winner_detail = "Human 1 Wins!"
                border_color = (0, 255, 0)
            elif score_computer > score_human:
                image = winner_image
                winner = "Human 2"
                winner_detail = "Human 2 Wins!"
                border_color = (0, 100, 255)
            else:
                image = tie_image
                winner = "Tie"
                winner_detail = "It's a Tie!"
                border_color = (150, 150, 150)
        elif game_mode == "human_vs_ai":
            # Determine who won based on human's color
            human_score = score_human if human_color == HUMAN else score_computer
            ai_score = score_computer if human_color == HUMAN else score_human
            
            if human_score > ai_score:
                image = winner_image
                winner = "Human"
                winner_detail = "Human Wins!"
                border_color = (0, 255, 0)
            elif ai_score > human_score:
                image = defeat_image
                winner = "AI"
                ai_name = ai_algorithm.upper() if ai_algorithm == "mcts" else ai_algorithm.capitalize()
                winner_detail = f"AI ({ai_name}) Wins!"
                border_color = (255, 0, 0)
            else:
                image = tie_image
                winner = "Tie"
                winner_detail = "It's a Tie!"
                border_color = (150, 150, 150)
        elif game_mode == "ai_vs_ai":
            white_ai_name = white_algorithm.upper() if white_algorithm == "mcts" else white_algorithm.capitalize()
            black_ai_name = black_algorithm.upper() if black_algorithm == "mcts" else black_algorithm.capitalize()
            
            if score_human > score_computer:
                image = winner_image
                winner = "White AI"
                winner_detail = f"White ({white_ai_name}) Wins!"
                border_color = (0, 200, 255)
            elif score_computer > score_human:
                image = winner_image
                winner = "Black AI"
                winner_detail = f"Black ({black_ai_name}) Wins!"
                border_color = (255, 100, 0)
            else:
                image = tie_image
                winner = "Tie"
                winner_detail = "It's a Tie!"
                border_color = (150, 150, 150)

        # Card drawing
        card_width = 405
        card_height = 450
        card_x = (1080 - card_width) // 2
        card_y = (800 - card_height) // 2
        image_x = card_x + (card_width - image.get_width()) // 2
        image_y = card_y + (card_height - image.get_height()) // 2

        # Draw border and white card
        pygame.draw.rect(screen, border_color, (card_x, card_y, card_width, card_height), 3)
        pygame.draw.rect(screen, (255, 255, 255), (card_x, card_y, card_width, card_height))
        screen.blit(image, (image_x, image_y))
        
        # Draw winner text on card
        winner_font = pygame.font.SysFont('freesansbold.ttf', 32, bold=True)
        winner_text = winner_font.render(winner_detail, True, (0, 0, 0))
        winner_text_rect = winner_text.get_rect(center=(card_x + card_width // 2, image_y + image.get_height() + 30))
        screen.blit(winner_text, winner_text_rect)
        
        # Draw final score on card
        score_font = pygame.font.SysFont('freesansbold.ttf', 24)
        score_text = score_font.render(f'Final Score: {score_human} - {score_computer}', True, (50, 50, 50))
        score_text_rect = score_text.get_rect(center=(card_x + card_width // 2, winner_text_rect.bottom + 25))
        screen.blit(score_text, score_text_rect)

        # Buttons
        screen.blit(replay_img, (850, 50))
        screen.blit(switch_img, (970, 50))
        pygame.display.update()

        waiting_replay = True
        while waiting_replay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (x >= 970 and y >= 50) and (x <= 1034 and y <= 114):
                        pygame.quit()
                        sys.exit()
                    elif (x >= 850 and y >= 50) and (x <= 914 and y <= 114):
                        waiting_replay = False
                        # restart main_game by returning and letting outer loop call it
                        pygame.mixer.music.stop()
                        return

    pygame.mixer.music.stop()
    return

# Run game in loop to allow replay behavior
if __name__ == "__main__":
    while True:
        main_game()
        # After returning from a game (user clicked replay), restart loop to start a new game
        # this keeps paths and behavior consistent
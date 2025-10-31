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

# ---------- Configuration ----------
FPS = 60

# MCTS parameters
MCTS_ITERATIONS = 300  # iterations per MCTS move (adjustable)
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

        pygame.draw.rect(screen, (200, 200, 200), hvh_rect, border_radius=8)
        pygame.draw.rect(screen, (200, 200, 200), hvai_rect, border_radius=8)
        pygame.draw.rect(screen, (200, 200, 200), aivai_rect, border_radius=8)

        draw_text(540, 290, "Human  vs  Human", 32)
        draw_text(540, 370, "Human  vs  AI (Minimax)", 32)
        draw_text(540, 450, "AI  vs  AI (Minimax vs MCTS)", 32)

        # Grid selection
        draw_text(540, 530, "Choose Grid Size: 4   6   8 (Click icons below)", 22)
        # Fake icons drawn as rects for click areas
        grid4_rect = pygame.Rect(420, 560, 70, 40)
        grid6_rect = pygame.Rect(500, 560, 70, 40)
        grid8_rect = pygame.Rect(580, 560, 70, 40)
        pygame.draw.rect(screen, (230, 230, 230), grid4_rect)
        pygame.draw.rect(screen, (230, 230, 230), grid6_rect)
        pygame.draw.rect(screen, (230, 230, 230), grid8_rect)
        draw_text(grid4_rect.centerx, grid4_rect.centery, "4", 26)
        draw_text(grid6_rect.centerx, grid6_rect.centery, "6", 26)
        draw_text(grid8_rect.centerx, grid8_rect.centery, "8", 26)

        print_developer_name()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hvh_rect.collidepoint(event.pos):
                    game_mode = "human_vs_human"
                    selecting = False
                elif hvai_rect.collidepoint(event.pos):
                    game_mode = "human_vs_ai"
                    selecting = False
                elif aivai_rect.collidepoint(event.pos):
                    game_mode = "ai_vs_ai"
                    selecting = False
                elif grid4_rect.collidepoint(event.pos):
                    grid_size = 4
                elif grid6_rect.collidepoint(event.pos):
                    grid_size = 6
                elif grid8_rect.collidepoint(event.pos):
                    grid_size = 8

        clock.tick(FPS)

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
        screen.blit(human_pic, (human_x, human_y))
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

    # Valid moves & flipping logic (kept consistent with original)
    def get_valid_moves(board_state, player):
        val_m = []
        for i in range(grid_size):
            for j in range(grid_size):
                if board_state[i][j] == 0:
                    if is_valid_move(board_state, i, j, player):
                        val_m.append((i, j))
        return val_m

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

    # ---------- Minimax (kept largely as original) ----------
    def minimax(board_state, depth, player, alpha, beta, max_depth):
        if depth == 0 or is_game_over(board_state) or depth == max_depth:
            return calc_score(board_state, -1)

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
        def __init__(self, board_state, player, parent=None, move=None):
            self.board = deep_copy(board_state)
            self.player = player  # player who will move at this node
            self.parent = parent
            self.move = move  # move that led to this node (x,y)
            self.children = []
            self.visits = 0
            self.wins = 0.0  # from perspective of the player that just moved?

        def is_fully_expanded(self):
            possible = get_valid_moves(self.board, self.player)
            return len(self.children) >= len(possible)

        def uct_score(self, c=1.41):
            if self.visits == 0:
                return float('inf')
            # wins are stored from POV of the player who just moved (parent.player)
            return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits) if self.parent else float('inf')

    def mcts_select(node):
        # select child with highest UCT
        while node.children:
            # pick child with highest UCT
            node = max(node.children, key=lambda n: n.uct_score())
        return node

    def mcts_expand(node):
        moves = get_valid_moves(node.board, node.player)
        tried = [child.move for child in node.children]
        for move in moves:
            if move not in tried:
                # create new child for this move
                new_board = flip_pieces(deep_copy(node.board), move[0], move[1], node.player)
                new_board[move[0]][move[1]] = node.player
                child = MCTSNode(new_board, -node.player, parent=node, move=move)
                node.children.append(child)
                return child
        return None

    def random_playout(board_state, player, depth_limit=MCTS_SIMULATION_DEPTH):
        b = deep_copy(board_state)
        p = player
        count = 0
        while not is_game_over(b) and count < depth_limit:
            moves = get_valid_moves(b, p)
            if not moves:
                p = -p
                # if both have no moves loop will exit due to is_game_over
                count += 1
                continue
            mv = random.choice(moves)
            b = flip_pieces(b, mv[0], mv[1], p)
            b[mv[0]][mv[1]] = p
            p = -p
            count += 1
        # final score from COMPUTER perspective (-1) --> we want >0 good for COMPUTER
        final_score = get_score_static(b)
        # return winner: 1 -> HUMAN, -1 -> COMPUTER, 0 -> tie
        if final_score[0] > final_score[1]:
            return HUMAN
        elif final_score[1] > final_score[0]:
            return COMPUTER
        return 0

    def backpropagate(node, result):
        # result is winner (HUMAN/COMPUTER/0)
        while node is not None:
            node.visits += 1
            # if the result is a win for the player who just moved into this node's parent,
            # increment wins. We'll store wins as +1 for a COMPUTER win, -1 for HUMAN win.
            if result == COMPUTER:
                node.wins += 1
            elif result == HUMAN:
                node.wins += 0  # count wins as 0 for human if we only reward COMPUTER?
                # For balanced statistics, we could do node.wins += (1 if result == node.player else 0)
                # But for simple selection we reward COMPUTER wins.
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

    def mcts_move(root_board, player, iterations=MCTS_ITERATIONS):
        root = MCTSNode(root_board, player)
        for _ in range(iterations):
            # 1. Selection
            node = root
            while node.children:
                node = max(node.children, key=lambda n: n.uct_score())

            # 2. Expansion
            if not is_game_over(node.board):
                child = mcts_expand(node)
                if child:
                    node = child

            # 3. Simulation
            # simulate from node.board and node.player
            result = random_playout(node.board, node.player)

            # 4. Backpropagation
            backpropagate(node, result)

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

    # ---------- Handlers for moves ----------
    def handle_human_click(mouse_pos):
        nonlocal turn
        x, y = mouse_pos
        x -= shift_right
        y -= shift_down
        i, j = int(x // square_size), int(y // square_size)
        if 0 <= i < grid_size and 0 <= j < grid_size:
            if (i, j) in get_valid_moves(board, HUMAN):
                tmp = flip_piecehuman(i, j, HUMAN)
                screen.blit(white_image, (i * cell + shift_right, j * cell + shift_down))
                pygame.display.flip()
                flip_animation(tmp, HUMAN)
                board[i][j] = HUMAN
                turn = -turn
                click_sound.play()
                time.sleep(0.15)

    def handle_ai_minimax_move(depth=4):
        nonlocal turn
        Ai_moves = get_valid_moves(board, COMPUTER)
        if not Ai_moves:
            turn = -turn
            return
        b_s = float('-inf')
        best_move = None
        for move in Ai_moves:
            temp_board = deep_copy(board)
            flipped_board = flip_pieces(temp_board, move[0], move[1], COMPUTER)
            flipped_board[move[0]][move[1]] = COMPUTER
            score = minimax(flipped_board, depth - 1, -COMPUTER, float('-inf'), float('inf'), depth)
            if score >= b_s:
                b_s = score
                best_move = move
        if best_move is not None:
            tmp = flip_piecehuman(best_move[0], best_move[1], COMPUTER)
            screen.blit(black_image, (best_move[0] * cell + shift_right, best_move[1] * cell + shift_down))
            pygame.display.flip()
            flip_animation(tmp, COMPUTER)
            time.sleep(0.15)
            board[best_move[0]][best_move[1]] = COMPUTER
            turn = -turn

    def handle_ai_mcts_move(iterations=MCTS_ITERATIONS):
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
        time.sleep(0.12)
        board[move[0]][move[1]] = COMPUTER
        turn = -turn

    # ---------- Main Game Loop ----------
    game_over = False
    ai_auto_delay = 0.3  # seconds between automated AI moves for visibility

    last_ai_move_time = time.time()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Human moves only accepted when appropriate
            if event.type == pygame.MOUSEBUTTONDOWN:
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
                    if turn == HUMAN:
                        handle_human_click(event.pos)

        # Automatic AI actions based on mode
        now = time.time()
        if game_mode == "human_vs_ai":
            if turn == COMPUTER and not is_game_over(board):
                # little delay so player can see changes
                if now - last_ai_move_time > ai_auto_delay:
                    handle_ai_minimax_move(depth=4)
                    last_ai_move_time = now

        elif game_mode == "ai_vs_ai":
            # Both players automated: Minimax (player -1) vs MCTS (player -1 as well in our previous setup)
            # We'll set: AI1 = Minimax (plays as HUMAN side for variety), AI2 = MCTS (plays as COMPUTER)
            # To make them alternate properly, we will let HUMAN be one AI (minimax) and COMPUTER be MCTS.
            if now - last_ai_move_time > ai_auto_delay and not is_game_over(board):
                # pick mover based on turn
                if turn == HUMAN:
                    # Minimax playing as HUMAN side (so we use minimax but compute with player=HUMAN)
                    Ai_moves = get_valid_moves(board, HUMAN)
                    if Ai_moves:
                        # Use minimax but flipping perspective: we want HUMAN to maximize its presence
                        b_s = float('-inf')
                        best_move = None
                        for move in Ai_moves:
                            temp_board = deep_copy(board)
                            flipped_board = flip_pieces(temp_board, move[0], move[1], HUMAN)
                            flipped_board[move[0]][move[1]] = HUMAN
                            # minimax expects player param to next mover; adapt by calling with next player COMPUTER
                            score = minimax(flipped_board, 3, COMPUTER, float('-inf'), float('inf'), 3)
                            if score >= b_s:
                                b_s = score
                                best_move = move
                        if best_move:
                            tmp = flip_piecehuman(best_move[0], best_move[1], HUMAN)
                            screen.blit(white_image, (best_move[0] * cell + shift_right, best_move[1] * cell + shift_down))
                            pygame.display.flip()
                            flip_animation(tmp, HUMAN)
                            board[best_move[0]][best_move[1]] = HUMAN
                            turn = -turn
                            last_ai_move_time = now
                    else:
                        # no moves -> pass
                        turn = -turn
                        last_ai_move_time = now
                else:
                    # COMPUTER => MCTS
                    Ai_moves = get_valid_moves(board, COMPUTER)
                    if Ai_moves:
                        move = mcts_move(board, COMPUTER, iterations=MCTS_ITERATIONS)
                        if move:
                            tmp = flip_piecehuman(move[0], move[1], COMPUTER)
                            screen.blit(black_image, (move[0] * cell + shift_right, move[1] * cell + shift_down))
                            pygame.display.flip()
                            flip_animation(tmp, COMPUTER)
                            board[move[0]][move[1]] = COMPUTER
                            turn = -turn
                            last_ai_move_time = now
                    else:
                        turn = -turn
                        last_ai_move_time = now

        # Check end conditions and passing logic
        valid_moves_h = get_valid_moves(board, HUMAN)
        valid_moves_c = get_valid_moves(board, COMPUTER)
        if is_game_over(board):
            game_over = True
        else:
            # If current player has no moves, pass turn
            if turn == HUMAN and not valid_moves_h:
                if not valid_moves_c:
                    game_over = True
                else:
                    turn = COMPUTER
            elif turn == COMPUTER and not valid_moves_c:
                if not valid_moves_h:
                    game_over = True
                else:
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
                current_valid = get_valid_moves(board, HUMAN) if turn == HUMAN else []
            elif game_mode == "ai_vs_ai":
                # hide move hints during AI-vs-AI for clarity (or show none)
                current_valid = []
            draw_board(screen, current_valid)
            print_score()
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
        if score_human > score_computer:
            image = winner_image
            winner = "Human"
        elif score_computer > score_human:
            image = defeat_image
            winner = "Computer"
        else:
            image = tie_image
            winner = "Tie"

        # Card drawing
        card_width = 405
        card_height = 450
        card_x = (1080 - card_width) // 2
        card_y = (800 - card_height) // 2
        image_x = card_x + (card_width - image.get_width()) // 2
        image_y = card_y + (card_height - image.get_height()) // 2

        # Draw border and white card
        if winner == "Human":
            pygame.draw.rect(screen, (0, 255, 0), (card_x, card_y, card_width, card_height), 3)
        elif winner == "Computer":
            pygame.draw.rect(screen, (255, 0, 0), (card_x, card_y, card_width, card_height), 3)
        pygame.draw.rect(screen, (255, 255, 255), (card_x, card_y, card_width, card_height))
        screen.blit(image, (image_x, image_y))

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

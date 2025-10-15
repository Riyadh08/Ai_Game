import pygame
import sys
import time
import pygame.mixer
import copy

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1080, 800))
pygame.mixer.music.load(r"music\game_music2.mp3")   #initial game music
click_sound = pygame.mixer.Sound(r"music\user_move.wav")

play_again=True
def main_game():
        
        pygame.mixer.music.play(-1)
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)

        
        pygame.display.set_caption("Reversi Game")
        human = 1
        computer = -1
        clock = pygame.time.Clock()

        
        grid_size = 4  #Dynamically taken later
        check_grid=True

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

        while check_grid:
            
           
            back_ground=pygame.image.load(r"Image/First_Page.png")
            screen.blit(back_ground,(0,0))
           
            pygame.display.update()
         
            card_button_rect = pygame.Rect(448, 215, 180, 100)
            message_box_visible = False
            guide_button_rect = pygame.Rect(448, 395,180,150)
            guide_box_visible = False

            pygame.display.update()
           
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Check if the card button is clicked
                        if card_button_rect.collidepoint(event.pos):
                           
                            message_box_visible = not message_box_visible

                        elif guide_button_rect.collidepoint(event.pos):
                            
                            guide_box_visible = not message_box_visible
                            
                #print(message_box_visible)    
                running1= True
                if guide_box_visible:
                   
                    print(check_grid, running)
                    play_pop = pygame.image.load(r"Image/rules2.png")
                    screen.blit(play_pop,(130,400))
                    pygame.display.flip()
                    print(running1)

                    while  running1:
                          
                          for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                    sys.exit()

                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    # Check if the card button is clicked
                                    x,y = event.pos
                                    print(x,y)
                                    if guide_button_rect.collidepoint(event.pos):
                                        running1=False
                                        running = False
                                        break

                                   
                #grid selection on the choose grid card
                if message_box_visible:
                   
                    print(check_grid, running)
                    play_pop = pygame.image.load(r"Image/grid2.png")
                    screen.blit(play_pop,(645,185))
                    pygame.display.flip()

                    while check_grid and running:
                          
                          for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                    sys.exit()

                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    
                                    x,y = event.pos
                                    print(x,y)
                                    if card_button_rect.collidepoint(event.pos):
                                        running=False
                                        break

                                    elif (x>=695 and x<=740) and (y>= 298 and y<= 336):
                                        check_grid=False
                                        running = False
                                        grid_size = 4
                                        pygame.mixer.music.stop()
                                        break

                                    elif x>=765 and x<=808 and y>=298 and y<= 336:
                                        check_grid=False
                                        running = False
                                        grid_size = 6
                                        pygame.mixer.music.stop() 
                                        break

                                    elif x>=830 and x<=875 and y>=298 and y<= 336:
                                        check_grid=False
                                        running = False
                                        grid_size = 8
                                        pygame.mixer.music.stop()
                                        break
                     
            clock.tick(60)
           
        print('hihihihi')
        # Size of the square
        square_size = 80

        # Set up the game board
        board = [[0 for i in range(grid_size)] for j in range(grid_size)]
        center = grid_size // 2
        board[center-1][center-1], board[center][center] = 1, 1
        board[center-1][center], board[center][center-1] = -1, -1

        # Player Images
        human_pic = pygame.image.load(r"Image/human.png")
        computer_pic = pygame.image.load(r"Image/robot.png")
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
                    if board[i][j] == human:
                        score_human += 1
                    elif board[i][j] == computer:
                        score_computer += 1
            return (score_human, score_computer)


        def print_score():
            my_font = pygame.font.SysFont('Comic Sans MS', 20)
            score_h, score_c = get_score()
            text_surface = my_font.render('Score: {}      :      {}'.format(score_h, score_c), False, (0, 0, 0))
            screen.blit(text_surface, (10, 90))


        
        turn = 1  # 1= Human, -1= AI
        game_over = False


        cell = 80

        shift_right=(1080-(grid_size*80))//2
        #print(shift_right)
        shift_down=100

        # Drawing the game board
        def draw_board(screen, valid_h):
            # Load the images
            empty_image = pygame.image.load(r"Image/empty.png")
            white_image = pygame.image.load(r"Image/4.png")
            black_image = pygame.image.load(r"Image/1.png")
            show_move   = pygame.image.load(r"Image/sMove.png")

            for i in range(grid_size):
                for j in range(grid_size):
                    if (i + j) % 2 == 0:
                        # Draw the empty square
                        screen.blit(empty_image, (i * cell + shift_right, j * cell + shift_down))
                    else:

                        screen.blit(empty_image, (i * cell + shift_right, j * cell + shift_down))
                    
                    if board[i][j] == 1:
                        # Draw the white disc
                        screen.blit(white_image, (i * cell+ shift_right, j * cell+ shift_down))
                    elif board[i][j] == -1:
                        # Draw the black disc
                        screen.blit(black_image, (i * cell+ shift_right, j * cell + shift_down))



            for x, y in valid_h:
                screen.blit(show_move, (x * cell + shift_right, y * cell + shift_down))


        # Make a move for the player
     #   def move_perform(x, y):
      ##      global turn
       #     if board[x][y] == 0:
        #        valid_moves = get_valid_moves(board,turn)
         #       if (x, y) in valid_moves:
         #           flip_pieces(x, y, turn)
          #          board[x][y] = turn
          #          turn = -turn


        # This return all the valid moves for the playr
        def get_valid_moves(board,player):
            val_m = []
            for i in range(grid_size):
                for j in range(grid_size):
                    if board[i][j] == 0:
                        if is_valid_move(board,i, j, player):
                            val_m.append((i, j))
            return val_m


        # Chosen Move is valid or not for player
        def is_valid_move(board,x, y, player):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    opp = False
                    while 0 <= nx < grid_size and 0 <= ny < grid_size:
                        if board[nx][ny] == -player:
                            opp = True
                        elif board[nx][ny] == player and opp:
                            return True
                        else:
                            break
                        nx, ny = nx + dx, ny + dy
            return False

        #for flipping the opponent's discs
        def flip_pieces(board, x, y, player):
            flipped_board = copy.deepcopy(board)
            
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
                            while (nx, ny) != (x + dx, y + dy):
                                nx, ny = nx - dx, ny - dy
                                flipped_board[nx][ny] = player
                            break
                        else:
                            break
                        nx, ny = nx + dx, ny + dy

            return flipped_board


      
        # Flip the pieces for a player
        def flip_piecehuman(x, y, player):
            flipped_indices = []  # List to store opponent's trapped piece indices
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
                                flipped_indices.append((nx, ny))  # Add opponent's trapped piece index
                                board[nx][ny]=player
                            break
                        else:
                            break
                        nx, ny = nx + dx, ny + dy

            return flipped_indices




        def is_game_over(board):
            # check if human and ai has moves
            if len(get_valid_moves(board,1)) == 0 and len(get_valid_moves(board,-1)) == 0:
                return True

            # Board is full or not
            for row in board:
                if 0 in row:
                    return False

            return True


        
        
        #Shows flip animation
        def flip_animation(tmp,t):
            
            if t==human:
                img1=pygame.image.load(r"Image/1.png")
                img2=pygame.image.load(r"Image/2.png")
                img3=pygame.image.load(r"Image/3.png")
                img4=pygame.image.load(r"Image/4.png")
            else:
                img1=pygame.image.load(r"Image/4.png")
                img2=pygame.image.load(r"Image/3.png")
                img3=pygame.image.load(r"Image/2.png")
                img4=pygame.image.load(r"Image/1.png")

            l=0
            while(l<len(tmp)):
                x,y=tmp[l]
                
                screen.blit(img1, (x * cell + shift_right, y * cell + shift_down))
                l=l+1
                
            pygame.display.update()
            time.sleep(0.1)

            l=0
            while(l<len(tmp)):
                x,y=tmp[l]
                screen.blit(img2, (x * cell + shift_right, y * cell + shift_down))
                l=l+1
            pygame.display.update()
            time.sleep(0.2)

            l=0
            while(l<len(tmp)):
                x,y=tmp[l]
                screen.blit(img3, (x * cell + shift_right, y * cell + shift_down))
                l=l+1
            pygame.display.update()
            time.sleep(0.2)

            l=0
            while(l<len(tmp)):
                x,y=tmp[l]
                screen.blit(img4, (x * cell + shift_right, y * cell + shift_down))
                l=l+1
            pygame.display.update()
            time.sleep(0.1)

        # Check if the board is full
       # def is_board_full(board):
         #   for row in board:
         #       if 0 in row:
         #           return False
        #    return True


       
        #score  calculation
        def calc_score(board, player):
            score = 0
            for i in range(grid_size):
                for j in range(grid_size):
                    if board[i][j] == player:
                        score += 1
                    elif board[i][j] == -player:
                        score -= 1
            return score

        #minimax implementation
        def minimax(board, depth, player, alpha, beta, max_depth, x, y):
            if depth == 0 or is_game_over(board) or depth == max_depth:
                sr = calc_score(board, -1)  
                #print(score, alpha, beta, player)
                return sr

            if player == -1:
                b_s = float('inf')
                valid_moves = get_valid_moves(board, player)  
               # print("Computer: ", valid_moves)
                for move in valid_moves:
                    temp_board = copy.deepcopy(board)
                    flipped_board = flip_pieces(temp_board, move[0], move[1], player)  # Get the flipped board
                    flipped_board[move[0]][move[1]] = player  # Update the flipped board
                    turn = -player
                    sr = minimax(flipped_board, depth - 1, turn, alpha, beta, max_depth, move[0], move[1])  # Use flipped board

                    if sr < b_s:
                        b_s = sr
                    if b_s <= alpha:
                        return b_s
                    if b_s < beta:
                        beta = b_s
                return b_s

            else:
                b_s = float('-inf')
                valid_moves = get_valid_moves(board, player)  
               # print("Human: ", valid_moves)
                for move in valid_moves:
                    temp_board = copy.deepcopy(board)
                    flipped_board = flip_pieces(temp_board, move[0], move[1], player)  
                    flipped_board[move[0]][move[1]] = player  
                    turn = -player
                    sr = minimax(flipped_board, depth - 1, turn, alpha, beta, max_depth, move[0], move[1])  
                    if sr > b_s:
                        b_s = sr
                    if b_s >= beta:
                        return b_s
                    if b_s > alpha:
                        alpha = b_s
                return b_s


        
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and turn == human:
                    x, y = event.pos
                   # print(x,y)
                    x-=shift_right
                    y-=shift_down
                    i, j = int(x // square_size), int(y // square_size)
                    #print(i,j)
                    #print("Human : ",get_valid_moves(human))
                    if (i, j) in get_valid_moves(board,human):
                        tmp=flip_piecehuman(i, j, human)
                        img=pygame.image.load(r"Image/4.png")
                        screen.blit(img, (i * cell+ shift_right, j * cell+ shift_down))
                        time.sleep(0.4)
                        pygame.display.flip()
                        flip_animation(tmp,human)

                        board[i][j] = human
                        turn = -turn
                       
                        screen.fill((255, 255, 255))
                        player_draw()
                        draw_board(screen, [])
                        print_score()
                        print_developer_name()
                        pygame.display.update()
                        click_sound.play()
                        time.sleep(0.5)


            if turn == computer and not is_game_over(board):
                Ai_moves = get_valid_moves(board, computer)
                if not Ai_moves:
                    turn = -turn
                    print("No valid AI moves")
                else:
                    depth = 4
                    b_s = float('-inf')
                    best_move = None
                    #print("Computerr :", Ai_moves)
                    for move in Ai_moves:  # iterate all valid AI moves
                        temp_board = copy.deepcopy(board)
                        flipped_board = flip_pieces(temp_board, move[0], move[1], computer)  # Flipped the board
                        flipped_board[move[0]][move[1]] = computer 
                        print(flipped_board)
                        #print(get_valid_moves(flipped_board,human))
                        score = minimax(flipped_board, depth - 1, -computer, float('-inf'), float('inf'), depth, move[0], move[1])  # Use temp_board
                       # sys.exit()
                        if score >= b_s:
                            b_s = score
                            best_move = move

                    if best_move is not None:
                        tmp = flip_piecehuman(best_move[0], best_move[1], computer)
                        img = pygame.image.load(r"Image/1.png")
                        screen.blit(img, (best_move[0] * cell + shift_right, best_move[1] * cell + shift_down))
                        time.sleep(0.4)
                        pygame.display.flip()
                        flip_animation(tmp, computer)
                        time.sleep(0.5)
                        board[best_move[0]][best_move[1]] = computer
                        turn = -turn



            # Check for game over condition
            valid_moves_human = get_valid_moves(board,human)
            if is_game_over(board):
                game_over = True
            elif not valid_moves_human:
                if not Ai_moves:
                    game_over = True
                else:
                    turn = -turn
                    print("No valid Human moves")

            # Update the display
            screen.fill((255, 255, 255))
            player_draw()
            draw_board(screen, valid_moves_human)
            print_score()
            print_developer_name()
            pygame.display.flip()
            clock.tick(60)


       
        if game_over:
           
            score_human, score_computer = get_score()
            winner_image = pygame.image.load(r"Image/winner1.png")
            defeat_image = pygame.image.load(r"Image/defeat.png")
            tie_image = pygame.image.load(r"Image/match_tie.png")
            screen.fill((255, 255, 255))
            player_draw()
            print_score()
            if score_human > score_computer:
                winner = "Human"
                image=winner_image
            elif score_computer > score_human:
                winner = "Computer"
                image =defeat_image
            else:
                winner = "Tie"
                image=tie_image
            
            
           
            card_width = 405
            card_height = 450
            card_x = (1080 - card_width) // 2
            card_y = (800 - card_height) // 2
            image_x = card_x + (card_width - image.get_width()) // 2
            image_y = card_y + (card_height - image.get_height()) // 2
            
            if winner == "Human":
               
               pygame.draw.rect(screen, (0,255,0), (card_x, card_y, card_width, card_height), 3)
            elif winner == "Computer":
               
               pygame.draw.rect(screen, (255,0,0), (card_x, card_y, card_width, card_height), 3)

            
            pygame.draw.rect(screen, (255, 255, 255), (card_x, card_y, card_width, card_height))

            

            screen.blit(image, (image_x, image_y))

            play_again = pygame.image.load(r"Image/replay.png")   #play again button
            game_quit = pygame.image.load(r"Image/switch.png")    #quite game button
            
            screen.blit(play_again,(850,50))
            screen.blit(game_quit,(970,50))
            
            pygame.display.update()
            play_again=False
            while not play_again:
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN :
                        x, y = event.pos
                        print(x,y)
                        if((x>=970 and y>=50) and (x<=1034 and y<=114)):
                            sys.exit()
                        elif((x>=850 and y>=50)and (x<=914 and y<=114)):
                            play_again=True
                            print(play_again)
                            break
            
            

while play_again:
    
    main_game()
    play_again=True
    
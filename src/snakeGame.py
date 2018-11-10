import pygame as pg
from random import randint

def gameUpdate():
    """
    Update the screen to show game score, highscore, food and snake position.
    """
    score_txt = font.render('Score: ' + str(score), True, white)
    hscore_txt = font.render('High Score: ' + str(high_score), True, white)
    pg.draw.rect(game_disp, red, food_pos)
    game_disp.blit(score_txt, (0,0))
    game_disp.blit(hscore_txt, (canv_w - 150, 0))
    snakePrint()
    screen.blit(game_disp, (0,0))
    pg.display.update()

def snakeGen():
    """
    Generate the next position of each snake cell based on the direction the \
snake is moving. Also check if the snake has run into itself.
    """
    collision = False
    for i, snake in enumerate(snake_pos):
        w = snake[0]
        h = snake[1]
        move_w = 0
        move_h = 0
        if(snake_dir[i] == 1):
            if(w >= canv_w - pt_dim):
                snake[0] = 0
            else:
                move_w = pt_dim
        elif(snake_dir[i] == -1):
            if(w < pt_dim):
                snake[0] = canv_w - pt_dim
            else:
                move_w = -pt_dim
        elif(snake_dir[i] == 2):
            if(h < pt_dim):
                snake[1] = canv_h - pt_dim
            else:
                move_h = -pt_dim
        elif(snake_dir[i] == -2):
            if(h >= canv_h - pt_dim):
                snake[1] = 0
            else:
                move_h = pt_dim
        snake.move_ip(move_w, move_h)
    
    # check if head of snake collides with the snake's body
    if (snake_pos[0].collidelist(snake_pos[1:]) != -1):
        collision = True
        
    return collision         
        

def foodGen():
    """
    Generate the next random food position, making sure it doesn't fall on a \
location with a snake cell on.
    """
    pos_w = int(randint(0, canv_w - pt_dim)/pt_dim) * pt_dim
    pos_h = int(randint(0, canv_h - pt_dim)/pt_dim) * pt_dim
    
    food = pg.rect.Rect((pos_w, pos_h), cell)
    
    food_on_snake = 1
    
    # check to see that the food does not fall on top of the snake
    while food_on_snake:
        for snake in snake_pos:
            # if food falls on snake, generate new food position
            if(food.colliderect(snake)):
                food_on_snake = 1
                pos_w = int(randint(0, canv_w - pt_dim)/pt_dim) * pt_dim
                pos_h = int(randint(0, canv_h - pt_dim)/pt_dim) * pt_dim
                food = pg.rect.Rect((pos_w, pos_h), cell)
                break
            else:
                food_on_snake = 0
    return food

def snakePrint():
    """
    Draw a rectangle for each snake cell.
    """
    for snake in snake_pos:        
        pg.draw.rect(game_disp, white, snake)
        
def instructionsPrint():
    instr_txt = end_font.render('Instructions:', True, white)
    end_text_rect[1] += 2 * text_pos
    screen.blit(instr_txt, end_text_rect)
    arrow_txt = end_font.render('Use arrow keys to move', True, white)
    end_text_rect[1] += text_pos
    screen.blit(arrow_txt, end_text_rect)
    f_txt = end_font.render('Press f to move faster', True, white)
    end_text_rect[1] += text_pos
    screen.blit(f_txt, end_text_rect)
    end_text_rect[1] += text_pos
    s_txt = end_font.render('Press s to move slower', True, white)
    screen.blit(s_txt, end_text_rect)
    end_text_rect[1] += 2 * text_pos
    enjoy_txt = end_font.render('Enjoy!', True, white)
    screen.blit(enjoy_txt, end_text_rect)
    
#############################################################################
time_wait_ms = 110
canv_w = 1280
canv_h = 720
score = 0
high_score = 0
direction = 1
snake_len = 3
pt_dim = 40
cell = (pt_dim, pt_dim)
white = pg.color.Color('White')
black = pg.color.Color('Black')
red = pg.color.Color('Red')
collision = False
game_over = False
win = False
win_thresh = 10
clear_events = False
text_pos = 50
print_game_over = False
#############################################################################

pg.init()
screen = pg.display.set_mode((canv_w, canv_h))
game_disp = pg.Surface((canv_w, canv_h))
font = pg.font.SysFont('Times New Roman', 20, True)
end_font = pg.font.SysFont('Times New Roman', 38, True)
pg.display.set_caption('Snake Game')
win_text = end_font.render('Congratulations, you won!', True, black)
win_text_rect = win_text.get_rect(center=(canv_w/2, canv_h/2))
end_text = end_font.render('Game Over!', True, white)
end_text_rect = end_text.get_rect(center=(canv_w/2 - 2 * text_pos, 
                                          canv_h/4 - text_pos))

# snake direction list: 
# 1: moving right horizontally
# -1: moving left horizontally
# 2: moving up vertically
# -2: moving down vertically
# 0: don't move
# the head of the snake is the left end of this list
snake_dir = [direction] * snake_len

# (x,y) position of each snake cell: head of snake is on the left
snake_pos = []
w0 = (canv_w/2, canv_h/2)
w1 = (w0[0] - pt_dim, w0[1])
w2 = (w1[0] - pt_dim, w0[1])
snake_pos.append(pg.rect.Rect(w0, cell))
snake_pos.append(pg.rect.Rect(w1, cell))
snake_pos.append(pg.rect.Rect(w2, cell))

food_pos = foodGen()

# print the instructions on screen for 2s
game_disp.fill(black)
instructionsPrint()
pg.display.update()

# wait 3s
for _ in range(3000):
    pg.event.pump()
    pg.time.wait(1)
     
run = True

while not game_over:
    # if user closes the window, the game is over
    for event in pg.event.get():
        if (event.type == pg.QUIT):
            game_over = True
            break
        # if user presses any key when game is over, restart game
        if (event.type == pg.KEYDOWN):
            run = True
            direction = 1
            snake_len = 3
            collision = False
            win = False
            game_disp.fill(black)
            snake_dir = [direction] * snake_len
            snake_pos = []
            snake_pos.append(pg.rect.Rect(w0, cell))
            snake_pos.append(pg.rect.Rect(w1, cell))
            snake_pos.append(pg.rect.Rect(w2, cell))       
            food_pos = foodGen()
            time_wait_ms = 110
            if(score > high_score):
                high_score = score
            score = 0
            end_text_rect = end_text.get_rect(center=(canv_w/2, 
                                                      canv_h/4 - text_pos))
            print_game_over = False
        
    while run:
        # if user closes the window, the game is over
        for event in pg.event.get():
            if (event.type == pg.QUIT):
                run = False
                game_over = True
                break
        
        # get user input for snake direction: <, >, ^, v
        pressed = pg.key.get_pressed()
        if pressed[pg.K_LEFT]:
            if(snake_dir[0] != 1):
                direction = -1
            
        elif pressed[pg.K_RIGHT]:
            if(snake_dir[0] != -1):
                direction = 1
            
        elif pressed[pg.K_UP]:
            if(snake_dir[0] != -2):
                direction = 2
            
        elif pressed[pg.K_DOWN]:
            if(snake_dir[0] != 2):
                direction = -2
        
        # make snake move faster by pressing the f key
        elif pressed[pg.K_f]:
            if(time_wait_ms > 30):
                time_wait_ms -= 10
        
        # make snake move slower by pressing the s key
        elif pressed[pg.K_s]:
            if(time_wait_ms < 500):
                time_wait_ms += 10
        
        # add the new direction to the front of the list, popping the last
        # this updates directions for each snake cell
        snake_dir = [direction] + snake_dir
        del snake_dir[-1]
        
        game_disp.fill(black)
        # keep track of snake's tail; to be used when snake gets longer
        tail_prev = snake_pos[-1].copy()
        
        # generate next snake position; check if snake has crashed into itself
        collision = snakeGen()
        
        # when snake touches food, make snake longer and increment score
        if(snake_pos[0] == food_pos):
            score += 1
            # the added cell will not move for the first time increment
            snake_dir.append(0)
            snake_pos.append(tail_prev)
            food_pos = foodGen()
        
        if(collision):
            run = False
            print_game_over = True
            clear_events = True
        
        # check winning condition: length of snake is max - win_thresh
        if(len(snake_pos) >= (canv_w/pt_dim) * (canv_h/pt_dim) - win_thresh):
            win = True
            run = False
            print_game_over = True
            clear_events = True
        
        if not collision:
            gameUpdate()
            pg.time.wait(time_wait_ms)
    
    if (win and print_game_over):
        screen.blit(win_text, win_text_rect)
        print_game_over = False
        pg.display.update()
        pg.time.wait(500)
    elif print_game_over:
        print_game_over = False
        end_text = end_font.render('Game Over!', True, white)
        end_text_rect = end_text.get_rect(center=(canv_w/2, canv_h/4))
        screen.blit(end_text, end_text_rect)
        if not game_over:
            key_tx = end_font.render('Press any key to continue', True, white)
            end_text_rect[1] += text_pos
            screen.blit(key_tx, end_text_rect)
            instructionsPrint()    
        pg.display.update()
        pg.time.wait(500)
        
    # after game is over, clear keyboard events
    if(clear_events):
        pg.event.clear()
        pg.time.wait(500)
        clear_events = False

pg.quit()
quit()
import pygame as pg
from random import randint

def gameUpdate():
    """
    Update the screen to show the game score, highscore, food and snake position.
    """
    score_txt = font.render('Score: ' + str(score), True, white)
    hscore_txt = font.render('High Score: ' + str(high_score), True, white)
    pg.draw.rect(game_disp, red, [food_pos[1], food_pos[0], pt_dim, pt_dim])
    game_disp.blit(score_txt, (0,0))
    game_disp.blit(hscore_txt, (canv_w - 150, 0))
    screen.blit(game_disp, (0,0))
    pg.display.update()

def snakeGen():
    """
Generate the next position of each snake cell based on the direction the \
snake is moving. Call the snakePrint(pos) function to update the position. \
Also check if the snake has run into itself.
    """
    collision = False    
    for i, pos in enumerate(snake_pos):
        if(snake_dir[i] == 1):
            if(pos[1] >= canv_w - pt_dim):
                pos[1] = 0
            else:
                pos[1] = pos[1] + pt_dim
        elif(snake_dir[i] == -1):
            if(pos[1] < pt_dim):
                pos[1] = canv_w - pt_dim
            else:
                pos[1] = pos[1] - pt_dim
        elif(snake_dir[i] == 2):
            if(pos[0] < pt_dim):
                pos[0] = canv_h - pt_dim
            else:
                pos[0] = pos[0] - pt_dim
        elif(snake_dir[i] == -2):
            if(pos[0] >= canv_h - pt_dim):
                pos[0] = 0
            else:
                pos[0] = pos[0] + pt_dim
            
        snakePrint([pos[0], pos[1]])
        
    for i in range(len(snake_pos) - 1):
        for j in range(i + 1, len(snake_pos)):
            if(snake_pos[i] == snake_pos[j]):
                collision = True
                return collision
    return collision         
        

def foodGen():
    """
Generate the next random food position, making sure it doesn't fall on a \
location with a snake cell on.
    """
    pos_w = int(randint(0, canv_w - pt_dim)/pt_dim) * pt_dim
    pos_h = int(randint(0, canv_h - pt_dim)/pt_dim) * pt_dim
    
    food_on_snake = 1
    
    # check to see that the food does not fall on top of the snake
    while food_on_snake:
        for i in range(len(snake_pos)):
            if([pos_h, pos_w] == snake_pos[i]):
                food_on_snake = 1
                # if food falls on snake, generate new food position
                pos_w = int(randint(0, canv_w - pt_dim)/pt_dim) * pt_dim
                pos_h = int(randint(0, canv_h - pt_dim)/pt_dim) * pt_dim
                break
            else:
                food_on_snake = 0
    return [pos_h, pos_w]

def snakePrint(pos):
    """
Draw a rectangle at the location of the provided 'pos' variable.
    """
    pg.draw.rect(game_disp, white, [pos[1], pos[0], pt_dim, pt_dim])  
    
#############################################################################
time_wait_ms = 110
canv_w = 1280
canv_h = 720
step = 10
origin = 0
score = 0
high_score = 0
direction = 1
snake_len = 3
grow_tail_dir = 0
grow_tail_pos = [0, 0]
tail_prev = [0, 0]
pt_dim = 40
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
collision = False
game_over = False
win = False
win_thresh = 10
clear_events = False
text_pos = 50
#############################################################################

pg.init()
screen = pg.display.set_mode((canv_w, canv_h))
game_disp = pg.Surface((canv_w, canv_h))
game_disp.fill(black)
font = pg.font.SysFont('Times New Roman', 20, True)
game_over_text = pg.font.SysFont('Times New Roman', 38, True)
winning_text = pg.font.SysFont('Times New Roman', 38, True)
instructions_text = pg.font.SysFont('Times New Roman', 38, True)
pg.display.set_caption('Snake Python')

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
snake_pos.append([canv_h/2, canv_w/2])
snake_pos.append([canv_h/2, canv_w/2 - pt_dim])
snake_pos.append([canv_h/2, canv_w/2 - 2 * pt_dim])

food_pos = foodGen()
        
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
            grow_tail_dir = 0
            grow_tail_pos = [0, 0]
            tail_prev = [0, 0]
            collision = False
            win = False
            game_disp.fill(black)
            snake_dir = [direction] * snake_len
            snake_pos = []
            snake_pos.append([canv_h/2, canv_w/2])
            snake_pos.append([canv_h/2, canv_w/2 - pt_dim])
            snake_pos.append([canv_h/2, canv_w/2 - 2 * pt_dim])            
            food_pos = foodGen()
            if(score > high_score):
                high_score = score
            score = 0
        
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
            
        if pressed[pg.K_RIGHT]:
            if(snake_dir[0] != -1):
                direction = 1
            
        if pressed[pg.K_UP]:
            if(snake_dir[0] != -2):
                direction = 2
            
        if pressed[pg.K_DOWN]:
            if(snake_dir[0] != 2):
                direction = -2
        
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
            snakePrint(snake_pos[-1])
            food_pos = foodGen()
        
        if(collision):
            run = False
            clear_events = True
        
        # check winning condition: length of snake is max - win_thresh
        if(len(snake_pos) >= (canv_w/pt_dim) * (canv_h/pt_dim) - win_thresh):
            win = True
            run = False
            clear_events = True
            
        gameUpdate()
        pg.time.wait(time_wait_ms)
    
    if(win):
        text = winning_text.render('Congratulations, You Won!', True, white)
    else:
        text = game_over_text.render('Game Over!', True, white)
        if not game_over:            
            text2 = game_over_text.render('Press any key to continue', \
                                              True, white)
            text2_rect = text2.get_rect(center=(canv_w/2, canv_h/2 + text_pos))
            screen.blit(text2, text2_rect)
    
    text_rect = text.get_rect(center=(canv_w/2, canv_h/2))
    screen.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(500)
    
    # after game is over, clear keyboard events
    if(clear_events):
        pg.event.clear()
        pg.time.wait(500)
        clear_events = False

pg.quit()
quit()
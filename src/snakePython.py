import pygame as pg
from random import randint

def gameUpdate():
    textsurface = font.render('Score: ' + str(score), True, white)
    pg.draw.rect(game_disp, red, [food_pos[1], food_pos[0], pt_dim, pt_dim])
    game_disp.blit(textsurface, (0,0))
    screen.blit(game_disp, (0,0))
    pg.display.update()

def snakeGen():
    collision = 0    
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
                collision = 1
                return collision
    return collision         
        

def foodGen():
    pos_w = int(randint(0, canv_w - 2 * pt_dim)/pt_dim) * pt_dim
    pos_h = int(randint(0, canv_h - 2 * pt_dim)/pt_dim) * pt_dim
    
    food_on_snake = 1
    
    # check to see that the food does not fall on top of the snake
    while food_on_snake:
        for i in range(len(snake_pos)):
            if([pos_h, pos_w] == snake_pos[i]):
                food_on_snake = 1
                pos_w = int(randint(0, canv_w - 2 * pt_dim)/pt_dim) * pt_dim
                pos_h = int(randint(0, canv_h - 2 * pt_dim)/pt_dim) * pt_dim
                break
            else:
                food_on_snake = 0
    return [pos_h, pos_w]

def snakePrint(pos):
    pg.draw.rect(game_disp, white, [pos[1], pos[0], pt_dim, pt_dim])  
    
#############################################################################
time_wait_ms = 120
canv_w = 1280
canv_h = 720
step = 10
origin = 0
score = 0
direction = 1
snake_len = 3
grow_tail_dir = 0
grow_tail_pos = [0, 0]
tail_prev = [0, 0]
pt_dim = 40
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
collision = 0
game_over = 0
win = 0
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

# (x,y) position of each snake cell that is on: head of snake is on the left
snake_pos = []
snake_pos.append([canv_h/2, canv_w/2])
snake_pos.append([canv_h/2, canv_w/2 - pt_dim])
snake_pos.append([canv_h/2, canv_w/2 - 2 * pt_dim])

food_pos = foodGen()
        
run = True

while run:
    for event in pg.event.get():
        if (event.type == pg.QUIT):
            run = False
            game_over = 1
            break
        
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
    
    snake_dir = [direction] + snake_dir
    del snake_dir[-1]
    
    game_disp.fill(black)
    tail_prev = snake_pos[-1].copy()
    collision = snakeGen()
        
    if(snake_pos[0] == food_pos):
        score += 1
        grow = 1
        snake_dir.append(0)
        snake_pos.append(tail_prev)
        snakePrint(snake_pos[-1])
        food_pos = foodGen()
    
    if(collision):
        run = False
    
    if(len(snake_pos) >= (canv_w/pt_dim) * (canv_h/pt_dim) - 10):
        win = 1
        run = False
        
    gameUpdate()
    pg.time.wait(time_wait_ms)

if(win):
    text = winning_text.render('Congratulations, You Won!', True, white)
else:
    text = game_over_text.render('Game Over!', True, white)

text_rect = text.get_rect(center=(canv_w/2, canv_h/2))
screen.blit(text, text_rect)
pg.display.update()

while not game_over:
    for event in pg.event.get():
        if (event.type == pg.QUIT):
            game_over = 1
            break

pg.quit()
quit()
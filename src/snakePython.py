import pygame
from random import randint

def gameUpdate(game_disp, score, font, pt_dim, food_pos):
    white = (255, 255, 255)
    red = (255, 0, 0)
    textsurface = font.render('Score: ' + str(score), True, white)
    pygame.draw.rect(game_disp, red, [food_pos[1], food_pos[0], pt_dim, pt_dim])
    game_disp.blit(textsurface, (0,0))
    screen.blit(game_disp, (0,0))
    pygame.display.update()

def snakeGen(game_disp, pt_dim, snake_dir, snake_pos, w_max, h_max):
    white = (255, 255, 255)
    
    for i, pos in enumerate(snake_pos):
        if(snake_dir[i] == 1):
            if(pos[1] >= w_max - pt_dim):
                pos[1] = 0
            else:
                pos[1] = pos[1] + pt_dim
        elif(snake_dir[i] == -1):
            if(pos[1] < pt_dim):
                pos[1] = w_max - pt_dim
            else:
                pos[1] = pos[1] - pt_dim
        elif(snake_dir[i] == 2):
            if(pos[0] < pt_dim):
                pos[0] = h_max - pt_dim
            else:
                pos[0] = pos[0] - pt_dim
        elif(snake_dir[i] == -2):
            if(pos[0] >= h_max - pt_dim):
                pos[0] = 0
            else:
                pos[0] = pos[0] + pt_dim
            
        snakePrint(game_disp, white, [pos[0], pos[1]], pt_dim)

def foodGen(game_disp, snake_pos, pt_dim, w_max, h_max):
    pos_w = int(randint(0, w_max - 2 * pt_dim)/pt_dim) * pt_dim
    pos_h = int(randint(0, h_max - 2 * pt_dim)/pt_dim) * pt_dim
    
    food_on_snake = 1
    
    # check to see that the food does not fall on top of the snake
    while food_on_snake:
        for i in range(len(snake_pos)):
            if([pos_h, pos_w] == snake_pos[i]):
                food_on_snake = 1
                pos_w = int(randint(0, w_max - 2 * pt_dim)/pt_dim) * pt_dim
                pos_h = int(randint(0, h_max - 2 * pt_dim)/pt_dim) * pt_dim
                break
            else:
                food_on_snake = 0
    return [pos_h, pos_w]

def snakePrint(game_disp, white, pos, pt_dim):
    for i in snake_pos:
        pygame.draw.rect(game_disp, white, [pos[1], pos[0], pt_dim, pt_dim])  
    
time_wait_ms = 100
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
pt_dim = 20
white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((canv_w, canv_h))
game_disp = pygame.Surface((canv_w, canv_h))
game_disp.fill(black)
font = pygame.font.SysFont('Times New Roman', 14, True)
pygame.display.set_caption('Snake Python')

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

food_pos = foodGen(game_disp, snake_pos, pt_dim, canv_w, canv_h)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        if(snake_dir[0] != 1):
            direction = -1
        
    if pressed[pygame.K_RIGHT]:
        if(snake_dir[0] != -1):
            direction = 1
        
    if pressed[pygame.K_UP]:
        if(snake_dir[0] != -2):
            direction = 2
        
    if pressed[pygame.K_DOWN]:
        if(snake_dir[0] != 2):
            direction = -2
    
    snake_dir = [direction] + snake_dir
    del snake_dir[-1]
    
    game_disp.fill(black)
    tail_prev = snake_pos[-1].copy()
    snakeGen(game_disp, pt_dim, snake_dir, snake_pos, canv_w, canv_h)
        
    if(snake_pos[0] == food_pos):
        score += 1
        grow = 1
        snake_dir.append(0)
        snake_pos.append(tail_prev)
        snakePrint(game_disp, white, snake_pos[-1], pt_dim)
        food_pos = foodGen(game_disp, snake_pos, pt_dim, canv_w, canv_h)
    gameUpdate(game_disp, score, font, pt_dim, food_pos)
    pygame.time.wait(time_wait_ms)

pygame.quit()
quit()
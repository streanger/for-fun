import sys
import os
# import time
import random
import pygame
from pygame.locals import *


"""
info:
    -pygame             (+)
    -tkinter            (-)
    -cv2                (-)
    -curses -> console  (-)
    
todo:
    -draw grid, to show possible move                       (-)                  
    -block reverse move                                     (+)
    -add wall or not on the edges                           (-)
    -make snake possible to grow                            (+)                     
    -add random meat, to eat                                (+)
    -add collisions with tail                               (+)
    -add meat eat                                           (+)
    -remove turning back bug, which causing collision       (-)
    -put meat only in free places, not onto the snake tail  (+)
    -make snake thinner than one grid size                  (-)
    -

23.09.2022:
    -constant frame rate:
        https://stackoverflow.com/questions/67285976/pygame-pygame-time-clock-or-time-sleep

20.11.2022:
    -point aka object:
        https://stackoverflow.com/questions/29290359/existence-of-mutable-named-tuple-in-python
        https://stackoverflow.com/questions/36688966/let-a-class-behave-like-its-a-list-in-python
"""


class Speed():
    """
    object with two mutable fields, to behave like list
    https://stackoverflow.com/questions/36688966/let-a-class-behave-like-its-a-list-in-python
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __getitem__(self, item):
        return (self.x, self.y)[item]
        
        
def map_speed(event, speed):
    """map snake speed depend on user event"""
    if event.type == 2:
        print(event.scancode)
        # 2 - KeyDown
        if event.scancode == 80:
            # print('down')
            if speed.x:
                speed.x, speed.y = (0, 1*speed_coeff)
            
        elif event.scancode == 72:
            # print('up')
            if speed.x:
                speed.x, speed.y = (0, -1*speed_coeff)
            
        elif event.scancode == 77:
            # print('right')
            if speed.y:
                speed.x, speed.y = (1*speed_coeff, 0)
                
        elif event.scancode == 75:
            # print('left')
            if speed.y:
                speed.x, speed.y = (-1*speed_coeff, 0)
                
    elif event.type == 768:
        print(event.scancode)
        # 2 - KeyDown
        if event.scancode == 81:
            # print('down')
            if speed.x:
                speed.x, speed.y = (0, 1*speed_coeff)
            
        elif event.scancode == 82:
            # print('up')
            if speed.x:
                speed.x, speed.y = (0, -1*speed_coeff)
            
        elif event.scancode == 79:
            # print('right')
            if speed.y:
                speed.x, speed.y = (1*speed_coeff, 0)
            
        elif event.scancode == 80:
            # print('left')
            if speed.y:
                speed.x, speed.y = (-1*speed_coeff, 0)
    return speed
    
    
if __name__ == "__main__":
    # ********* init pygame *********
    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    clock = pygame.time.Clock()
    
    # ********* screen setup *********
    size = width, height = 640, 480
    speed_coeff = 20
    speed = Speed(speed_coeff*1, speed_coeff*0)
    black = 0, 0, 0
    color = (50, 50, 150)
    screen = pygame.display.set_mode(size)
    
    # ********* meat setup *********
    meat_size = 20
    meat_color = (230, 50, 120)    
    meat_position_x = random.randrange(0, (width-meat_size), 20)
    meat_position_y = random.randrange(0, (height-meat_size), 20)
    meat_rect = pygame.Rect(meat_position_x, meat_position_y, meat_size, meat_size)
    
    # ********* snake setup *********
    snake = pygame.Rect(0, 0, 20, 20)
    snake_square_size_x = 20
    snake_square_size_y = 20
    
    snake = snake.move([width+1, 0])
    snake = snake.move([-(width+1), 0])
    snake = snake.move([0, height+1])
    snake = snake.move([0, -(height+1)])
    snake = snake.move([320, 240])
    
    # ********* tail setup *********
    last_positions = []
    current_length = 2
    
    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # print(event.type, event.dict, event)
            # print(event.type)
            speed = map_speed(event, speed)
            
        snake = snake.move(*speed)
        
        if snake.right < 1:
            snake = snake.move([width, 0])
            
        if snake.left > (width-1):
            snake = snake.move([-width, 0])
            
        if snake.bottom < 1:
            snake = snake.move([0, height])
            
        if snake.top > (height-1):
            snake = snake.move([0, -height])
            
        screen.fill(color)
        
        # ********* draw meat *********
        if pygame.Rect.colliderect(snake, meat_rect):
            current_length += 1
            # put meat only in free places, not onto the snake tail
            all_positions = set([(x, y) for x in range(0, (width-meat_size), 20) for y in range(0, (height-meat_size), 20)])
            snake_head_position = (snake.left, snake.top)
            snake_tail_positions = list(zip(*[item for key, item in enumerate(list(zip(*last_positions))) if not key%2]))
            prohibited_positions = set(snake_tail_positions + [snake_head_position])     # snake tail + head
            possible_positions = list(all_positions.difference(prohibited_positions))
            meat_position_x, meat_position_y = random.choice(possible_positions)
            meat_rect = pygame.Rect(meat_position_x, meat_position_y, meat_size, meat_size)
            
        pygame.draw.rect(screen, meat_color, meat_rect)
        
        # ********* draw snake *********
        pygame.draw.rect(screen, (150, 200, 10), snake)
        
        # ********* draw tail *********
        tail_collisions = []
        for key, item in enumerate(last_positions[-current_length:]):
            if not key%2:
                tail_color = (20, 100, 20)
            else:
                tail_color = (30, 150, 30)
                
            tail_left, tail_right, tail_top, tail_bottom = item
            tail_width = tail_right - tail_left
            tail_height = tail_bottom - tail_top
            tail_rect = pygame.Rect(tail_left, tail_top, tail_width, tail_height)
            pygame.draw.rect(screen, tail_color, tail_rect)
            tail_collisions.append(pygame.Rect.colliderect(snake, tail_rect))
            
        # ********* detect collisions *********
        if sum(tail_collisions):
            print('\n--------------------------')
            print('SNAKE EAT YOURSELF :(')
            print('GAME OVER!')
            print('YOUR SCORE IS: {}'.format(current_length*10))
            print('----------------------------\n')
            
            # draw some text on the board
            textsurface = myfont.render('GAME OVER!', True, (200, 20, 20))
            screen.blit(textsurface, (200, 20))
            
            textsurface = myfont.render('YOUR SCORE IS: {}'.format(current_length*10), False, (200, 20, 20))
            screen.blit(textsurface, (160, 80))
            pygame.display.flip()
            break
            
        # ********* update screen *********
        pygame.display.flip()
        last_positions.append((snake.left, snake.right, snake.top, snake.bottom))
        last_positions = last_positions[-current_length:]
        
    # ********* cleanup *********
    input('press enter to exit ')
    # pygame.image.save(screen, "screenshot.png")
    pygame.display.flip()
    pygame.quit()
    
import sys
import os
import time
import random
import pygame
from pygame.locals import *


def script_path():
    '''change current path to script one'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
if __name__ == "__main__":
    script_path()
    
    
    # ****************** init pygame ******************
    pygame.init()
    
    
    # ****************** screen setup ******************
    size = width, height = 640, 480
    speed_coeff = 20
    speed = [speed_coeff*1, speed_coeff*0]
    black = 0, 0, 0
    color = (50, 50, 150)
    screen = pygame.display.set_mode(size)
    
    
    # ****************** meat setup ******************
    meat_size = 20
    meat_color = (230, 50, 120)    
    meat_position_x = random.randrange(0, (width-meat_size), 20)
    meat_position_y = random.randrange(0, (height-meat_size), 20)
    create_new_meat = True
    
    
    # ****************** snake setup ******************
    snake = pygame.Rect(0, 0, 20, 20)
    snake_square_size_x = 20
    snake_square_size_y = 20
    
    snake = snake.move([width+1, 0])
    snake = snake.move([-(width+1), 0])
    snake = snake.move([0, height+1])
    snake = snake.move([0, -(height+1)])
    snake = snake.move([320, 240])
    
    
    # ****************** tail setup ******************
    last_positions = []
    current_length = 1
    current_length = 30
    
    
    while 1:
        # print('speed_x: {:003}, speed_y: {:003}'.format(*speed), end='\r', flush=True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # print(event.type, event.dict, event)
            
            if event.type == 2:
                # 2 - KeyDown
                if event.scancode == 80:
                    # print('down')
                    if speed[0]:
                        speed = [0, 1*speed_coeff]
                    
                elif event.scancode == 72:
                    # print('up')
                    if speed[0]:
                        speed = [0, -1*speed_coeff]
                    
                elif event.scancode == 77:
                    # print('right')
                    if speed[1]:
                        speed = [1*speed_coeff, 0]
                    
                elif event.scancode == 75:
                    # print('left')
                    if speed[1]:
                        speed = [-1*speed_coeff, 0]
                        
                        
        snake = snake.move(speed)
        
        if snake.right < 1:
            snake = snake.move([width, 0])
            
        if snake.left > (width-1):
            snake = snake.move([-width, 0])
            
        if snake.bottom < 1:
            snake = snake.move([0, height])
            
        if snake.top > (height-1):
            snake = snake.move([0, -height])
            
            
        screen.fill(color)
        
        
        # ****************** draw meat ******************
        if create_new_meat:
            meat_position_x = random.randrange(0, (width-meat_size), 20)
            meat_position_y = random.randrange(0, (height-meat_size), 20)
            meat_rect = pygame.Rect(meat_position_x, meat_position_y, meat_size, meat_size)
            print('meat position: ({}, {})'.format(meat_position_x, meat_position_y))
            create_new_meat = False
            # if snake eat current meat, change flag, to True
        pygame.draw.rect(screen, meat_color, meat_rect)
        
        
        # ****************** draw snake ******************
        pygame.draw.rect(screen, (150, 200, 10), snake)
        
        
        # ****************** draw tail ******************
        for key, item in enumerate(last_positions[-current_length:]):
            # print('{:003}: {}'.format(key, item))
            
            if not key%2:
                tail_color = (20, 100, 20)
            else:
                tail_color = (30, 150, 30)
                
            # if not key%3:
                # tail_color = (20, 100, 20)
            # elif key%3 == 2:
                # tail_color = (25, 125, 25)
            # else:
                # tail_color = (30, 150, 30)
                
            tail_left, tail_right, tail_top, tail_bottom = item
            tail_width = tail_right - tail_left
            tail_height = tail_bottom - tail_top
            tail_rect = pygame.Rect(tail_left, tail_top, tail_width, tail_height)
            pygame.draw.rect(screen, tail_color, tail_rect)
            
            
        # ****************** update screen ******************
        pygame.display.flip()
        time.sleep(0.1)
        # color = ((ballrect.x)%256, (ballrect.y)%256, ((ballrect.x+ballrect.y)//2)%256)
        color = (50, 50, 150)
        last_positions.append((snake.left, snake.right, snake.top, snake.bottom))
        last_positions = last_positions[-current_length:]
        # pygame.image.save(screen, "screenshot.jpg")
        
        
'''
info:
    -pygame
    -tkinter
    -cv2
    -curses -> console
    
todo:
    -create rect, which grows with new rects when catching other rects
    -draw grid, to show possible move
    -block reverse move
    -add wall or not on the edges
    -make snake possible to grow
    -add random meat, to eat
    -add collisions with tail
    -add meat eat
    -
    
'''

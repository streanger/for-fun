import sys
import os
import time
import pyautogui
import cv2
import numpy as np


def script_path():
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)
    return currentPath
    
    
def reverse_way(way):
    reverse = {
        'up': 'down',
        'down': 'up',
        'right': 'left',
        'left': 'right',
        '': ''
    }
    return reverse[way]
    
    
def update_pos(pos, way):
    direction, value = way
    dictio = {
        'up': (0, -1),
        'down': (0, +1),
        'left': (-1, 0),       
        'right': (+1, 0)
        }
    posX, posY = pos
    return (posX + value*dictio[direction][0], posY + value*dictio[direction][1])
    
    
def way_out(data, last, shape, current):
    out = sorted(data, key=lambda x: x[1])
    zeroCondition = out[0][1]
    if not zeroCondition:
        direction = out[0][0]
        if direction == 'up':
            value = - current[1]
        elif direction == 'down':
            value = shape[0] - current[1] -1
        elif direction == 'right':
            value = shape[1] - current[0] - 1
        elif direction == 'left':
            value = - current[0]
        else:
            value = 0
        return (direction, value)
        
        
def choose_way(data, last):
    out = sorted(data, key=lambda x: x[1], reverse=True)
    for key, value in out:
        if key == reverse_way(last):
            continue
        return (key, value)
        
        
def check_rays(img, pos):
    # startPos = (47, 216)
    posX, posY = pos
    up = down = right = left = 0
    
    rayUp = (img[:posY, posX])[::-1]
    indexesUp = np.where(rayUp == 255)
    if indexesUp[0].any():
        up = indexesUp[0][0]
        
    rayDown = img[posY:, posX]
    indexesDown = np.where(rayDown == 255)
    if indexesDown[0].any():
        down = indexesDown[0][0]
    
    # horizontal rays
    rayLeft = (img[posY, :posX])[::-1]
    indexesLeft = np.where(rayLeft == 255)
    if indexesLeft[0].any():
        left = indexesLeft[0][0]
    
    rayRight = img[posY, posX:]
    indexesRight = np.where(rayRight == 255)
    if indexesRight[0].any():
        right = indexesRight[0][0]
    
    # print('up: {}\ndown: {}\nright: {}\nleft: {}'.format(up, down, right, left))
    out = [
        ('up', up),
        ('down', down),
        ('right', right),
        ('left', left)
        ]
    return out
    
    
def make_path(img, pos, last=''):
    '''
        img - image with maze(tunnel)
        pos - initial position (X, Y)
        last - last way (up/down/left/right)
    '''
    decreaseValue = 16                                   # it may be calculated from tubbel thickness?
    shape = img.shape                                   # (Y, X)
    boundaries = (0, shape[0]-1, shape[1]-1)
    # print('initial pos[X, Y]: {}'.format(pos))
    POSITIONS = [pos]
    
    for x in range(26):
        out = check_rays(img, pos)
        new = choose_way(out, last)
        new = (new[0], new[1] - decreaseValue)
        
        if not new[1]:
            new = way_out(out, last, shape, pos)        # we come to an end
            
        pos = update_pos(pos, new)
        POSITIONS.append(pos)
        last = new[0]
        # print('new pos: {}, direction(last): {}'.format(pos, last))
        # print('new pos: {}'.format(pos))
        
        if pos[0] in boundaries or (pos[1] in boundaries):
            # print('you are out :)\nx: {}'.format(x))
            break
    return POSITIONS
    
    
def draw_path(img, positions):
    '''draw lines on img in live mode'''
    out = img.copy()
    for key, pos in enumerate(positions):
        if key:
            out = cv2.line(out, positions[key-1], pos, (105, 255, 105), 3)
        cv2.imshow('out', out)
        time.sleep(0.025)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    input('press enter to exit... ')
    cv2.destroyAllWindows()
    return out
    
    
def mouse_movement(positions):
    '''make mouse movement with initial position'''
    return True
    
    
if __name__ == "__main__":
    script_path()
    
    
    # *********** calculate positions ***********
    img = cv2.imread('clear.png', 0)
    POSITIONS = make_path(img, (47, 216), '')
    
    
    # *********** draw path on image ***********
    img = cv2.imread('clear.png', 1)        # color mode
    out = draw_path(img, POSITIONS)
    cv2.imwrite('solution.png', out)
    
    
    # *********** make mouse movements ***********
    mouse_movement(positions)
    
    
    
'''
before:
    -we got 4 ways, and can't go back
    -can't do last 2 ways
    -5px before white
    -choose one of two longest way and never look back
    
todo:
    -draw path on the image
    -move mouse live
    
'''


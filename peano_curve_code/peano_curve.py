import sys
import os
import time
import math
import string
import numpy as np
import cv2


def script_path():
    '''change current path to script one'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def show_image(title, image):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def create_blank_image(height, width):
    img = np.zeros((height, width, 3), np.uint8)
    return img
    
    
def peano_curve(start, iterations, step):
    '''
    parameters:
        -start          -frist item: P, Q, R, S
        -iterations     -number of iterations
        -step           -step value
        
    info:
        PQRS
        
        P - down, down, right, up, up, right, down, down
        Q - down, down, left, up, up, left, down, down
        R - up, up, right, down, down, right, up, up
        S - up, up, left, down, down, left, up, up
        
        P is reverse with S
        Q is reverse with R
        
        P => P, Q, P, R, S, R, P, Q, P
        Q => Q, P, Q, S, R, S, Q, P, Q
        R => R, S, R, P, Q, P, R, S, R
        S => S, R, S, Q, P, Q, S, R, S
        
    directions:
        P
        | +-+
        | | |
        +-+ v


        S
        ^ +-+
        | | |
        +-+ |


        Q
        +-+ |
        | | |
        v +-+

        R
        +-+ ^
        | | |
        | +-+
        
    '''
    
    if iterations <= 0:
        # translate to matrix values of positions
        values_dictio = {
            'up': (0, -1*step),
            'down': (0, +1*step),
            'left': (-1*step, 0),
            'right': (+1*step, 0),
            }
            
        directions_dictio = {
            'P': ['down', 'down', 'right', 'up', 'up', 'right', 'down', 'down'],
            'Q': ['down', 'down', 'left', 'up', 'up', 'left', 'down', 'down'],
            'R': ['up', 'up', 'right', 'down', 'down', 'right', 'up', 'up'],
            'S': ['up', 'up', 'left', 'down', 'down', 'left', 'up', 'up'],
            }
            
        transition_dictio = {
            'PQ': 'down',
            'QP': 'down',
            'PR': 'right',
            'RP': 'right',
            'RS': 'up',
            'SR': 'up',
            'QS': 'left',
            'SQ': 'left',
            }
            
        out = []
        for key, item in enumerate(start):
            if key:
                # add transition between items
                before = start[key-1]
                transition = values_dictio[transition_dictio[before+item]]
                out.append(transition)
                
            dot_values = [values_dictio[direction] for direction in directions_dictio[item]]
            out.extend(dot_values)
        return out
        
    recursion_dictio = {
        'P': 'PQPRSRPQP',
        'Q': 'QPQSRSQPQ',
        'R': 'RSRPQPRSR',
        'S': 'SRSQPQSRS',
        }
        
    data = list(start)
    start = ''.join([recursion_dictio[item] for item in data])
    
    return peano_curve(start, iterations-1, step)
    
    
def draw_peano_curve_clear(start, iterations, step):
    '''draw peano curve on blank image
        -without coloring effects
    '''
    
    if not start in 'PQRS':
        print('wrong start value: {}, should be: P, Q, R or S'.format(start))
        return False
        
    # get peano positions
    positions = peano_curve(start, iterations, step)
    
    
    # create image, with proper shape
    width = height = (3**(iterations+1)-1)*step + 1
    img = create_blank_image(height, width)
    
    
    # get initial position
    # P is reverse with S, Q is reverse with R
    if start == 'P':
        pos_x, pos_y = (0, 0)
    elif start == 'S':
        pos_x, pos_y = (width - 1, height - 1)
    elif start == 'Q':
        pos_x, pos_y = (width - 1, 0)
    elif start == 'R':
        pos_x, pos_y = (0, height - 1)
        
        
    # draw image
    for key, (move_x, move_y) in enumerate(positions):
        last_pos = (pos_x, pos_y)
        pos_x += move_x
        pos_y += move_y
        pos = (pos_x, pos_y)
        img = cv2.line(img, last_pos, pos, (50, 255, 50), 1)      # draw line
        
        # cv2.imshow('img', img)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
            # break
        # time.sleep(0.01)
    # cv2.destroyAllWindows()   
    return img
    
    
def draw_peano_curve(start, iterations, step, color_effects, live_mode=False):
    '''draw peano curve on blank image'''
    
    if not start in 'PQRS':
        print('wrong start value: {}, should be: P, Q, R or S'.format(start))
        return False
        
    # get peano positions
    positions = peano_curve(start, iterations, step)
    
    
    # create image, with proper shape
    width = height = (3**(iterations+1)-1)*step + 1
    img = create_blank_image(height, width)
    
    
    # get initial position
    # P is reverse with S, Q is reverse with R
    if start == 'P':
        pos_x, pos_y = (0, 0)
    elif start == 'S':
        pos_x, pos_y = (width - 1, height - 1)
    elif start == 'Q':
        pos_x, pos_y = (width - 1, 0)
    elif start == 'R':
        pos_x, pos_y = (0, height - 1)
        
        
    # make live colors
    if color_effects == 0:
        B = 50
        G = 255
        R = 50
        
    elif color_effects == 1:
        B = 200
        G = 100
        R = 100
    else:
        B = 255
        G = 255
        R = 255
        
    color = (B, G, R)
    
    # draw image
    for key, (move_x, move_y) in enumerate(positions):
        last_pos = (pos_x, pos_y)
        pos_x += move_x
        pos_y += move_y
        pos = (pos_x, pos_y)
        
        if color_effects == 2:
            B = (key * pos_x) % 256
            G = (key * pos_y) % 256
            R = (key * (pos_x + pos_y)) % 256
            
        elif color_effects == 3:
            B = round((pos_y+1)**math.sin(pos_x)) % 256
            G = round((pos_x+1)**math.sin(pos_y)) % 256
            R = round((pos_x+pos_y+1)**math.sin(pos_x+pos_y)) % 256
            
        elif color_effects == 4:
            B = round(math.sin(pos_x)*key) % 256
            G = round(math.sin(pos_y)*key) % 256
            R = round(math.sin(pos_x+pos_y)*key) % 256
            
        elif color_effects == 5:
            B = (pos_x + pos_y)**1 % 256
            G = (pos_x + pos_y + key)**2 % 256
            R = (pos_x - pos_y + key)**2 % 256
            
        color = (B, G, R)
        img = cv2.line(img, last_pos, pos, color, 1)      # draw line
        
        if live_mode:
            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.01)
            
    if live_mode:
        cv2.destroyAllWindows()
        
    return img
    
    
def extract_vales(img):
    values = []
    # positions = peano_curve('P', 5, 1)
    # pos_x, pos_y = (0, 0)
    
    positions = peano_curve('R', 6, 1)
    pos_x, pos_y = (0, 511)
    
    values.append(img[pos_x, pos_y])
    
    for move_x, move_y in positions:
        pos_x += move_x
        pos_y += move_y
        try:
            values.append(img[pos_x, pos_y])
        except IndexError:
            continue
    return values
    
    
if __name__ == "__main__":
    script_path()
    
    # ********* draw peano curve on blank image *********
    start, iterations, step, color_effects = 'P', 2, 20, 0
    out = draw_peano_curve(start, iterations, step, color_effects, live_mode=True)
    # out = draw_peano_curve_clear(start, iterations, step)
    filename = '{}_{}_{}_{}.png'.format(start, iterations, step, color_effects)
    cv2.imwrite(filename, out)
    
    
    
    # ********* draw over existing image with peano curve *********
    
    
    
    
    
    # ********* extract values from image, by peano curve trace *********
    
    
    
    
    # ********* ctf not solved task *********
    # file = 'peano_curve.png'
    # img = cv2.imread(file, 0)
    # values = extract_vales(img)
    # values_str = ''.join(['1' if item == 255 else '0' for item in values])
    # print(''.join([chr(int(values_str[n:n+8], 2)) for n in range(0, len(values_str), 8)]))          # P
    # print('\n' + '-------------------------------' + '\n')
    # print(''.join([chr(int(values_str[n:n+8], 2)) for n in range(0, len(values_str[::-1]), 8)]))    # S
    
    
'''
todo:
    -draw over existing image with peano curve
    -extract values from image, by peano curve trace (clean)
    -make the same, for hiber curve
    
'''

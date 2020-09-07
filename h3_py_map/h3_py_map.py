import sys
import os
import math
import colorsys
import numpy as np
import cv2
from vision_stuff import shrink_image, show_image, blank_image

import time
import pyautogui
import re
import pywinauto
from pywinauto.application import Application
import subprocess
import warnings
from pywinauto.keyboard import send_keys
import ctypes

# set pause
# pyautogui.PAUSE = 0.0001
pyautogui.PAUSE = 0.001


def script_path():
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)
    return currentPath
    
    
def convert_rotation(deg, radius):
    # R layer
    R_a = math.cos((deg/360)*2*math.pi)*radius
    R_b = math.sin((deg/360)*2*math.pi)*radius
    # G layer
    G_a = math.cos(((deg+120)/360)*2*math.pi)*radius
    G_b = math.sin(((deg+120)/360)*2*math.pi)*radius
    # B layer
    B_a = math.cos(((deg+240)/360)*2*math.pi)*radius
    B_b = math.sin(((deg+240)/360)*2*math.pi)*radius
    dictio = {"R_a":R_a,
              "R_b":R_b,
              "G_a":G_a,
              "G_b":G_b,
              "B_a":B_a,
              "B_b":B_b}
    dictio = dict(zip(dictio.keys(), [round(item) for item in list(dictio.values())]))
    return dictio
    
    
def rgb_to_xy(r, g, b):
    '''red - 0deg, green - 120deg, blue - 240deg'''
    r_vector = np.array([r, 0])
    g_vector = np.array([math.cos((120/360)*2*math.pi)*g, math.sin((120/360)*2*math.pi)*g])
    b_vector = np.array([math.cos((240/360)*2*math.pi)*b, math.sin((240/360)*2*math.pi)*b])
    
    out = r_vector + g_vector + b_vector
    out = tuple(int(round(item)) for item in out)
    return out
    
    
def rgb_to_xyz(r, g, b):
    '''red - 0deg, green - 120deg, blue - 240deg'''
    r_vector = np.array([r, 0, r])
    g_vector = np.array([math.cos((120/360)*2*math.pi)*g, math.sin((120/360)*2*math.pi)*g, g])
    b_vector = np.array([math.cos((240/360)*2*math.pi)*b, math.sin((240/360)*2*math.pi)*b, b])
    
    out = r_vector + g_vector + b_vector
    out = tuple(int(round(item)) for item in out)
    return out
    
    
def h3_colors():
    '''do the same mapping for true terrain color (this one is from minimap)'''
    data = {
        'brown': {'rgb': (82, 57, 8), 'area': 'Piachy'},
        'yellow': {'rgb': (222, 206, 140), 'area': 'Pustynia'},
        'green': {'rgb': (0, 66, 0), 'area': 'Łąka'},
        'white': {'rgb': (181, 198, 198), 'area': 'Śnieg'},
        'rotten': {'rgb': (74, 132, 107), 'area': 'Bagno'},
        'gimble': {'rgb': (132, 115, 49), 'area': 'Skorupa'},
        'red': {'rgb': (132, 49, 0), 'area': 'Podziemia'},
        'highland': {'rgb': (74, 74, 74), 'area': 'Lawa'},
        'blue': {'rgb': (8, 82, 148), 'area': 'Woda'},
        'black': {'rgb': (0, 0, 0), 'area': 'Skały'},
    }
    return data
    
    
def calculate_distance(x1, y1, x2, y2):
    '''not in use'''
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist
    
    
def calculate_distance_xyz(x1, y1, z1, x2, y2, z2):
    '''ok for now'''
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return dist
    
    
def closest_point(points, single):
    '''match single point to the closest from the points list; coords are x, y
    -that won't work as i thought, because of ignoring amplitude e.g. (0, 0, 0) is equal to (255, 255, 255)
    '''
    distances = []
    for point in points:
        # dist = calculate_distance(*point, *single)
        dist = calculate_distance_xyz(*point, *single)
        distances.append((point, dist))
        
    closest = sorted(distances, key=lambda x: x[1])[0]  # get first item
    color = closest[0]
    return color
    
    
def generate_img_and_path(img, map_size):
    '''
    remember of double color revers:
        -1st time - original img (bgr2rgb)
        -2nd time - mapped img (rgb2bgr)
    optionally we can reverse h3 rgb colors twice
    '''
    
    half_of_size = map_size//2
    small_img = shrink_image(img, half_of_size, half_of_size)       # 144x144 with step of 2
    small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)
    
    
    # ******** h3 colors stuff ********
    data = h3_colors()
    h3_colors_values = [val['rgb'] for key, val in data.items()]
    
    # xyz (this one is better)
    h3_colors_xyz = [rgb_to_xyz(*color) for color in h3_colors_values]
    h3_colors_xyz_rgb = {rgb_to_xyz(*val['rgb']): val['rgb'] for key, val in data.items()}
    h3_colors_xyz_name = {rgb_to_xyz(*val['rgb']): val['area'] for key, val in data.items()}
    # h3_colors_xyz_name = {rgb_to_xyz(*val['rgb']): key for key, val in data.items()}
    
    
    # ******** convert colors to h3 map editor colors ********
    colors_sequence = []
    mapped_img = blank_image(*small_img.shape, value=0)
    for key, row in enumerate(small_img):
        line = []
        for index, px in enumerate(row):
            single_xyz = rgb_to_xyz(*px)
            out = closest_point(h3_colors_xyz, single_xyz)
            converted = h3_colors_xyz_rgb[out]
            mapped_img[key][index] = converted
            
            # get color name
            color_name = h3_colors_xyz_name[out]
            line.append(color_name)
        colors_sequence.append(line)
        
        
    # colors reverse
    mapped_img_bgr = cv2.cvtColor(mapped_img, cv2.COLOR_RGB2BGR)
    # cv2.imwrite('test_h3_colors.png', mapped_img_bgr)
    
    # move mouse on the corner of (0, 0) and press start
    
    
    return mapped_img_bgr, colors_sequence
    
    
def get_process_id(pattern):
    ''' return list of processes with using "tasklist" command '''
    tasks = subprocess.check_output(["tasklist"])
    tasks = tasks.decode("utf-8", "ignore")
    processes = []
    for line in tasks.split("\n")[3:]:
        for key, element in enumerate(line.split()):
            if element.isdigit():
                processes.append(["_".join(line.split()[:key]), line.split()[key]])     #when join use " " or "_"
                break
    processList = processes
    appId = [id for process, id in processList if pattern == process]                #get first app id (may be more than one)
    if appId:
        appId = int(appId[0])
    else:
        appId = False
    return appId
    
    
def send_keys_twice(key):
    '''function send_keys simple wrapper'''
    send_keys(key)
    # time.sleep(0.001)
    send_keys(key)
    return None
    
    
def some(app):
    app.top_window().set_focus()
    send_keys('{DOWN}')
    return None
    
    
def paint_area(app, color):
    app.top_window().menu_select('Narzędzia -> Teren -> {}'.format(color))
    # current_x, current_y = pyautogui.position()
    # app.top_window().click_input(button='left', coords=(current_x, current_y), button_down=True)
    # pyautogui.click()
    # pyautogui.leftClick()
    pyautogui.leftClick(duration=0.001)
    # pyautogui.dragTo(current_x, current_y, button='left')
    return None
    
    
def get_key_state(dll, key):
    '''
    VK_CAPITAL  - 0x14  - CAPS LOCK key
    VK_NUMLOCK  - 0x90  - NUM LOCK key
    VK_SCROLL   - 0x91  - SCROLL LOCK key
    '''
    val = hllDll.GetKeyState(key)
    if val in (1, -127):
        return True
    return False
    
    
if __name__ == "__main__":
    script_path()
    
    # *********** generate image and colors sequence ***********
    # '''
    file = 'doge.jpg'
    # file = 'pope.jpeg'
    map_size = 144
    
    img = cv2.imread(file, 1)
    mapped_img, colors_sequence = generate_img_and_path(img, map_size)
    # cv2.imwrite('out_h3_color.png', mapped_img)
    # sys.exit()
    # show_image('mapped_img', mapped_img)
    # '''
    
    
    # *********** connect with app ***********
    pattern = 'h3maped.exe'
    appId = get_process_id(pattern)
    app = Application().connect(process=appId)
    top = app.top_window()
    # sys.exit()
    
    
    # *********** get init values & init moves ***********
    wrap = top.wrapper_object()
    wrap.client_to_screen((0, 0))   # Maps point from client to screen coordinates
    coords = (50, 144)  # position (0, 0) from window corner
    corner_x, corner_y = wrap.client_to_screen(coords)
    # print('corner_x: {}, corner_y: {}'.format(corner_x, corner_y))
    # sys.exit()
    
    
    # *********** create sequence of moves ***********
    # need to be passed by user
    right_down_corner = (51, 28)
    
    # hardcoded for now
    move_mouse_hor = 26
    press_arrow_hor = 72 - move_mouse_hor
    move_mouse_ver = 13
    press_arrow_ver = 72 - move_mouse_ver
    
    
    
    # *********** calculate fixed value of step ***********
    # (0 - 51) -> (144 - 1684)
    # 51 steps -> (1682 - 144) = 1538
    # 1 step -> 1538/51 ~ 30.1569 [px]
    # step = 1540/51
    step = (1586 - 305)/40      # new calculations :)
    step_hor = step_ver = step*2       # for now use fixed values
    
    
    all_lines = []
    for key, line in enumerate(colors_sequence):
        # line_paint_func = [(app.top_window().menu_select, ('Narzędzia -> Teren -> {}'.format(color), )) for color in line]
        line_paint_func = [(paint_area, (app, color)) for color in line]
        
        if not key%2:
            direction_hor = '{RIGHT}'
        else:
            direction_hor = '{LEFT}'
            
        moves_arrow = [(send_keys_twice, (direction_hor, )) for x in range(press_arrow_hor)]
        down_additional = round(max(key - press_arrow_ver, 0)*step_ver)
        # print('down_additional: {}'.format(down_additional))
        # breakpoint()
        if not key%2:
            moves_mouse = [(pyautogui.moveTo, (corner_x + round(x*step_hor), corner_y)) for x in range(1, move_mouse_hor+1)]
        else:
            moves_mouse = [(pyautogui.moveTo, (corner_x + round(x*step_hor), corner_y)) for x in range(move_mouse_hor)]
            
        moves_hor = moves_arrow + moves_mouse
        line_sequence = [x for y in zip(line_paint_func, moves_hor) for x in y]
        
        if not key%2:
            line_sequence = line_sequence[:-1]  # remove last horizontal blank move
        else:
            line_sequence = line_sequence[::-1]
            line_sequence = line_sequence[1:]
            
        all_lines.append(line_sequence)
        
    # vertical moves list
    direction_ver = '{DOWN}'
    moves_arrow = [(send_keys_twice, (direction_ver, )) for x in range(press_arrow_ver)]
    # moves_mouse = [(pyautogui.moveTo, (corner_x + (move_mouse_hor*round(step_hor))*((x+1)%2), corner_y + x*round(step_ver))) for x in range(move_mouse_ver)]
    moves_mouse = [(pyautogui.moveTo, (corner_x + (round(move_mouse_hor*step_hor))*((x+1)%2), corner_y + round(x*step_ver))) for x in range(move_mouse_ver)]
    moves_ver = moves_arrow + moves_mouse
    
    
    # full sequence
    moves_sequence_packed = [x for y in zip(all_lines, moves_ver) for x in y]
    moves_sequence = []
    for item in moves_sequence_packed:
        if isinstance(item, list):
            moves_sequence.extend(item)
        else:
            moves_sequence.append(item)
            
            
    # *********** make moves ***********
    # 1) setup (base position, brush size, zoom in twice)
    # 2) paint
        # app.top_window().menu_select('Narzędzia -> Teren -> Bagno')
    # 3) move right twice (with arrow)
    
    input('start with sequence ')
    top.set_focus()                         # focus on main window
    pyautogui.moveTo(corner_x, corner_y)    # move cursor to init position
    top.menu_select('Narzędzia -> Teren -> 2x2')
    
    
    # *********** run sequence ***********
    hllDll = ctypes.WinDLL("User32.dll")
    
    
    for key, (func, args) in enumerate(moves_sequence):
        state = get_key_state(hllDll, 0x91)
        if state:
            current_pos = pyautogui.position()
            print('stopped. Place cursor and toggle scroll lock')
            print('last mouse position: {}'.format(current_pos))
            while True:
                state = get_key_state(hllDll, 0x91)
                if not state:
                    break
                    
        print('{}. {}({}), POS: {}'.format(key, func, args, pyautogui.position()))
        # top.set_focus()
        # time.sleep(0.1)
        func(*args)     # call function
        # time.sleep(0.002)
        # time.sleep(0.01)
        # time.sleep(0.05)
        # time.sleep(0.075)
        # time.sleep(0.20)
        # time.sleep(0.15)    # OK
        time.sleep(0.20)
        # time.sleep(0.25)
        
        
        
        
'''
info:
    -map 144x144
    -1px is 2x2 (minimal step for ground color)
    -colors:
        http://chir.ag/projects/name-that-color/#C2B570
        https://en.wikipedia.org/wiki/List_of_colors:_A–F
    -use 2x2 square for paint
    -to move right use arrow-right twice
    -to move down use arrow-down twice
    -move left to right and up to down
    -
'''

import sys
import os
import time
import random
import math
import numpy as np
import cv2


def script_path():
    '''change dir, to current script path'''
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
    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def blank_image(height, width, layers=3, value=255):
    '''create blank image, with specified shape, layers and initial value'''
    img = np.ones((height, width, layers), dtype=np.uint8)*value
    return img
    
    
def margin(img, space_size, color=(0, 0, 0)):
    '''space_size -integer; 2 is the lowest value for proper read; try to increase value and look for decoding time'''
    current_h, current_w, layers = img.shape
    new_image = np.ones((current_h+space_size*2, current_w+space_size*2, layers), dtype=np.uint8)*color
    new_image[space_size:-space_size, space_size:-space_size] = img
    return new_image
    
    
def bounce_angle(angle, side):
    '''calculate new angle (out), based on angle (in) and side'''
    out = 0
    return out
    
    
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
    
    
def paste_image(smaller, bigger, x_pos, y_pos):
    ''' paste some image with alpha channel, to another one '''
    
    # ************** handle position and size errors **************
    max_size_y , max_size_x = bigger.shape[:2]
    small_size_y, small_size_x = smaller.shape[:2]
    cut_x, cut_y = 0, 0
    if x_pos + small_size_x > max_size_x:
        cut_x = max_size_x - x_pos
        if cut_x < 1:
            return bigger
        smaller = smaller[:, 0:cut_x]
    if y_pos + small_size_y > max_size_y:
        cut_y = max_size_y - y_pos
        if cut_y < 1:
            return bigger
        smaller = smaller[0:cut_y, :]
    # print("cut_x: {:0=3d}, cut_y: {:0=3d}".format(cut_x, cut_y), end='\r', flush=True)
    
    
    # ************** paste smaller image into bigger, with including alpha channel **************
    B, G, R, alpha = cv2.split(smaller)
    smallerRGB = cv2.merge((B, G, R))
    mask_inv = cv2.bitwise_not(alpha)
    height, width = smallerRGB.shape[:2]
    
    roi = bigger[y_pos:y_pos+height, x_pos:x_pos+width]
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    img2_fg = cv2.bitwise_and(smallerRGB, smallerRGB, mask=alpha)
    
    # breakpoint()
    
    dst = cv2.add(img1_bg, img2_fg)
    out = bigger.copy()         # we shouldn't change original image
    out[y_pos:y_pos+height, x_pos:x_pos+width] = dst
    return out
    
    
class ObjectPosition():
    def __init__(self, name, radius, pos_x, pos_y, pos_z):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        
        
    def function(self):
        return None
        
        
        
def draw_grid(img, center, depth, counter):
    '''draw pseudo 3D grid'''
    # colors
    # color = (200, 200, 10)  # seledin
    # color = (200, 10, 200)  # violet
    
    # ************ setup ************
    color = (255, 30, 30)   # blue
    # color = (30, 255, 30)   # green
    out = img.copy()
    height, width = out.shape[:2]
    # move_center_x, move_center_y = (0, 0)
    # move_center_x, move_center_y = (0, 230)
    # move_center_x, move_center_y = (+350, +150)
    # move_center_x, move_center_y = (+50, +100)
    # move_center_x, move_center_y = (+400, +200)
    # move_center_x, move_center_y = (+600, +350)
    # move_center_x, move_center_y = (0, +450)
    # move_center_x, move_center_y = (300, 200)
    # move_center_x, move_center_y = (-200, +100)
    # move_center_x, move_center_y = (+400, +200)
    # move_center_x, move_center_y = (100, 100)
    # center = (width//2, height//2)      # center-center
    # center = (width//2+move_center_x, height//2+move_center_y)      # center-moved
    
    
    
    # ************ draw walls ************
    p_center = center
    p_left_up = (0, 0)
    p_right_up = (width-1, 0)
    p_left_down = (0, height-1)
    p_right_down = (width-1, height-1)
    walls = []
    
    # walls up down
    wall_up_color = (30, 30, 30)
    wall_up = np.array([p_left_up, p_right_up, p_center])
    wall_down = np.array([p_left_down, p_right_down, p_center])
    cv2.drawContours(out, [wall_up], 0, wall_up_color, -1)
    cv2.drawContours(out, [wall_down], 0, wall_up_color, -1)
    
    # wals left, right
    wall_down_color = (50, 50, 50)
    wall_left = np.array([p_left_up, p_left_down, p_center])
    wall_right = np.array([p_right_up, p_right_down, p_center])
    cv2.drawContours(out, [wall_left], 0, wall_down_color, -1)
    cv2.drawContours(out, [wall_right], 0, wall_down_color, -1)
    
    
    
    # ************ draw star lines ************
    lines_number = 10
    step_x = width/lines_number
    step_y = height/lines_number
    points_top = [(round(step_x*x), 0) for x in range(lines_number+1)]
    points_bottom = [(round(step_x*x), height-1) for x in range(lines_number+1)]
    points_left = [(0, round(step_y*x)) for x in range(lines_number+1)]
    points_right = [(width-1, round(step_y*x)) for x in range(lines_number+1)]
    points = list(set(points_top + points_bottom + points_left + points_right))
    
    for point in points:
        cv2.line(out, (point), (center), color, 1)
        
        
    # ************ draw squares ************
    blue = (255, 50, 50)
    green = (50, 255, 50)
    red = (50, 50, 255)
    
    # squares_number = 8
    squares_number = depth
    phi = (1 + 5 ** 0.5) / 2
    square_points = generate_squares(width, height, center, phi, squares_number)
    main_square = [((+1, +1), (width-2, height-2))]
    squares = main_square + square_points
    squares = squares[::-1]
    # squares = []    # SKIP SQUARES
    
    total_squares = len(squares)
    for key, (p1, p2) in enumerate(squares):
        if key == counter % total_squares:
            line_thickness = math.ceil(7/(2 + total_squares - (key + 1)))   # calculated based on hyperbole_values
            out = cv2.rectangle(out, p1, p2, (255, 150, 150), line_thickness)
            continue
        out = cv2.rectangle(out, p1, p2, blue, 1)
        # out = cv2.rectangle(out, p1, p2, green, 1)
    pass
    
    return out
    
    
def generate_squares(width, height, center, divider, number):
    '''generate squares'''
    half_width_left, half_height_top = center
    half_height_bot = height - half_height_top
    half_width_right = width - half_width_left
    
    # horizontal lines with golden division
    horizontal_points = []
    for x in range(1, number+1):
        line_step_top = round(half_height_top/(divider**x))
        line_step_bot = round(half_height_bot/(divider**x))
        top_pos = (half_height_top - line_step_top)
        bot_pos = (half_height_top + line_step_bot)
        horizontal_points.append(top_pos)
        horizontal_points.append(bot_pos)
        
    # vertical lines with golden division
    vertical_points = []
    for x in range(1, number+1):
        line_step_left = round(half_width_left/(divider**x))
        line_step_right = round(half_width_right/(divider**x))
        left_pos = (half_width_left - line_step_left)
        right_pos = (half_width_left + line_step_right)
        vertical_points.append(left_pos)
        vertical_points.append(right_pos)
        
    # math first and last points and draw square; continue by going to center
    horizontal_points = sorted(horizontal_points)
    vertical_points = sorted(vertical_points)
    diagonal_points = list(zip(vertical_points, horizontal_points))
    start_square = diagonal_points[:len(diagonal_points)//2]
    stop_square = diagonal_points[len(diagonal_points)//2:][::-1]
    square_points = list(zip(start_square, stop_square))
    return square_points
    
    
def tracker_func(val):
    '''tracker function'''
    # print('tracker used: {}'.format(val))
    return None
    
    
def hyperbole_values(number, val):
    '''use it for calculating radius value for squares'''
    for x in range(2, 2+number):
        yield math.ceil(val/x)
        
        
if __name__ == "__main__":
    script_path()
    
    
    # ******* video setup *******
    MAKE_VIDEO = False
    # MAKE_VIDEO = True
    
    if MAKE_VIDEO:
        size = None
        is_color = True
        format = "XVID"
        fps = 30
        fourcc = cv2.VideoWriter_fourcc(*format)
        vid = None
        outvid = "grid_test.avi"
        
        video_shots = 9
        speed_level = 0
    else:
        video_shots = 0
        speed_level = 10
        
        
        
    # window image
    # window_image = cv2.imread('space_window3.png', cv2.IMREAD_UNCHANGED)
    # window_image = cv2.imread('space_window4.png', cv2.IMREAD_UNCHANGED)
    # show_image('window_image', window_image)
    # height, width = window_image.shape[:2]
    
    # ******* image shape *******
    # height, width = (1080, 1920)
    # height, width = (720, 1280)
    height, width = (500, 1280)
    # height, width = (450, 800)
    
    
    
    # ******* generate points *******
    points = {}
    # points_number = 0
    points_number = 27
    # points_number = 54
    speed_values = [x for x in range(1, 8)]
    weights = (50, 25, 15, 5, 5, 3, 2)
    
    # where points are created
    center_x = width//2
    center_y = height//2
    
    for x in range(points_number):
        pos = (random.randrange(center_x-10, center_x+10), random.randrange(center_y-10, center_y+10))
        angle = random.randrange(360)
        # speed = random.randrange(1, 15)
        # speed = random.randrange(1, 8)
        speed = random.choices(speed_values, weights, k=1)[0]
        color = (random.randrange(40, 90),)*3
        key = 'p{:02}'.format(x)
        points[key] = (pos, angle, speed, color)
        
        
    # ******* match triangles *******
    points_keys = list(points.keys())
    triangles = {'t{}'.format(n//3): tuple(points_keys[n:n+3]) for n in range(0, len(points_keys), 3)}
    
    
    # ******* trackers *******
    # createTrackbar(...)
        # createTrackbar(trackbarName, windowName, value, count, onChange) -> None
    cv2.namedWindow('img')
    cv2.createTrackbar('horizontal', 'img', 0, width - 1, tracker_func)
    cv2.createTrackbar('vertical', 'img', 0, height - 1, tracker_func)
    cv2.createTrackbar('depth', 'img', 0, 16, tracker_func)
    cv2.setTrackbarPos('horizontal', 'img', width//2)
    cv2.setTrackbarPos('vertical', 'img', height//2)
    cv2.setTrackbarPos('depth', 'img', 8)
    
    
    counter = 0
    motion_counter = 0
    video_counter = 0
    while True:
        img = blank_image(height, width, layers=3, value=0)
        
        # ******* draw grid *******
        center_x = cv2.getTrackbarPos('horizontal', 'img')
        center_y = cv2.getTrackbarPos('vertical', 'img')
        depth = cv2.getTrackbarPos('depth', 'img')
        center = (center_x, center_y)
        img = draw_grid(img, center, depth, motion_counter)
        
        
        # ******* draw objects; update position *******
        # MAKE FUNCTION FROM THIS PART
        for key, point in points.items():
            pos, angle, speed, color = point
            
            # calc radius; make feeling, that closer planets are greater
            pos_x = abs(center_x - pos[0])
            pos_y = abs(center_y - pos[1])
            diag_len = (pos_x**2 + pos_y**2)**0.5
            radius = round(diag_len/100) + 1
            
            # draw object
            img = cv2.circle(img, pos, radius=radius, color=color, thickness=-1)
            
            # calculates new points positions
            # new_pos_x = (pos[0] + round(speed*(1 + angle/180))) + random.randrange(2)
            new_pos_x = (pos[0] + round(speed*(1 + angle/180)))
            # new_pos_y = (pos[1] + int(speed)) + random.randrange(2)
            new_pos_y = (pos[1] + int(speed))
            pos = (new_pos_x, new_pos_y)
            
            if not (0 < new_pos_x < width) or not (0 < new_pos_y < height):
                pos = (random.randrange(center_x-10, center_x+10), random.randrange(center_y-10, center_y+10))
                speed = random.choices(speed_values, weights, k=1)[0]
                
            # update points dict
            points[key] = (pos, angle, speed, color)
            
            
        # ******* paste foreground *******
        # img = paste_image(window_image, img, 0, 0)
        
        
        if MAKE_VIDEO:
            # ******* video part *******
            print(video_counter)
            video_counter += 1
            if video_counter > video_shots:
                break
                
            for _ in range(5):
                if vid is None:
                    if size is None:
                        size = img.shape[1], img.shape[0]
                    vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
                if size[0] != img.shape[1] and size[1] != img.shape[0]:
                    img = cv2.resize(img, size)
                vid.write(img)
        else:
            # ******* show image *******
            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.01)
            # time.sleep(0.1)
            
            
        # ******* counter stuff *******
        counter += 1
        if counter > speed_level:
            counter = 0
            motion_counter += 1
            # if motion_counter > 6:
                # motion_counter = 0
                
                
    # ******* CLEANUP *******
    if MAKE_VIDEO:
        vid.release()
    else:
        cv2.destroyAllWindows()
        
        
        
'''
info:
    cv2.line(img, (start_point), (stop_point), (155, 255, 155), 2)
    image = cv2.circle(image, (x,y), radius=0, color=(0, 0, 255), thickness=-1)
    
    draw triangle:
        triangle_cnt = np.array( [pt1, pt2, pt3] )
        cv2.drawContours(image, [triangle_cnt], 0, (0,255,0), -1)
        
    -for now its side effect of triangles script
    -it looks like asteroids in space :)
    -random choice with weights:
        https://pynative.com/python-weighted-random-choices-with-probability/
    -
    
todo:
    -make angle to make sense (for now it doesn't affect for anything)
    -
    
'''


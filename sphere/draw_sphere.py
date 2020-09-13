import sys
import os
import time
import math
import numpy as np
import cv2
import vision_stuff as vs
from handle_mouse import MouseHandler


def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path
    
    
def draw_cross(img, width, height):
    '''draw cross in the center of the image'''
    color = (255, 50, 255)
    thickness = 1
    start_point_hor = (0, height//2)
    end_point_hor = (width-1, height//2)
    start_point_ver = (width//2, 0)
    end_point_ver = (width//2, height-1)
    cv2.line(img, start_point_hor, end_point_hor, color, thickness) 
    cv2.line(img, start_point_ver, end_point_ver, color, thickness) 
    return None
    
    
def generate_ellipses_seq(sphere_center_x, sphere_center_y, sphere_radius, short_axis_divider, ellipses_number):
    '''
    variables:
        -number of ellipse
        -short_axis divider
        -center of sphere
        -radius of sphere
        
    out:
        -generate different colors
        -reverse container
        
    '''
    # sphere_center = tuple(map(int, (sphere_center_x, sphere_center_y)))
    sphere_diameter = sphere_radius*2
    divider = ellipses_number + 1
    step = sphere_diameter/divider
    
    
    ellipses_container = []
    for x in range(ellipses_number):
        step_sum = step*(x+1)
        center = tuple(map(int, (sphere_center_x, sphere_center_y - sphere_radius + step_sum)))
        
        # calc axes
        
        if False:
            # this one is very simillar, but its false
            long_axis = round(sphere_radius*math.cos((math.pi/2)*(abs(sphere_radius - step_sum)/sphere_radius))**0.5)
        else:
            # this one is true
            long_axis = round(((sphere_radius**2 - (abs(sphere_radius - step_sum))**2)**0.5))
            
            
        # print(long_axis)
        # short_axis = round(long_axis/short_axis_divider)
        # short_axis = round(long_axis * short_axis_divider)
        # short_axis = round(long_axis/6 * abs(short_axis_divider))
        short_axis = round(long_axis/3 * abs(short_axis_divider))
        # breakpoint()
        
        if False:
            # ******* common ellipse setup *******
            color_b = min(int(round(10 + (ellipses_number - x)/ellipses_number*150)), 255)
            color_g = min(int(round(50 + (ellipses_number - x)/ellipses_number*255)), 255)
            color_r = min(int(round(10 + (ellipses_number - x)/ellipses_number*50)), 255)
            color = (color_b, color_g, color_r)
            ellipses_container.append((center, long_axis, short_axis, color, 0, 360))
            
        else:
            # ******* splitted ellipse setup *******
            if short_axis_divider >= 0:
                start_angle_front, end_angle_front = 0, 180
                start_angle_back, end_angle_back = 180, 360
            else:
                start_angle_front, end_angle_front = 180, 360
                start_angle_back, end_angle_back = 0, 180
                
            full_ellipse = []
            # back part
            color_b = min(int(round(10 + (ellipses_number - x)/ellipses_number*40)), 255)
            color_g = min(int(round(30 + (ellipses_number - x)/ellipses_number*80)), 255)
            color_r = min(int(round(10 + (ellipses_number - x)/ellipses_number*40)), 255)
            color = (color_b, color_g, color_r)
            # ellipses_container.append((center, long_axis, short_axis, color, start_angle_back, end_angle_back))
            full_ellipse.append((center, long_axis, short_axis, color, start_angle_back, end_angle_back))
            
            # front part
            color_b = min(int(round(50 + (ellipses_number - x)/ellipses_number*150)), 255)
            color_g = min(int(round(100 + (ellipses_number - x)/ellipses_number*255)), 255)
            color_r = min(int(round(50 + (ellipses_number - x)/ellipses_number*150)), 255)
            color = (color_b, color_g, color_r)
            # ellipses_container.append((center, long_axis, short_axis, color, start_angle_front, end_angle_front))
            full_ellipse.append((center, long_axis, short_axis, color, start_angle_front, end_angle_front))
            
            # draw back part first
            if short_axis_divider >= 0:
                full_ellipse.reverse()
            ellipses_container.extend(full_ellipse)
            
            
    if short_axis_divider >= 0:
        return ellipses_container[::-1]
    return ellipses_container
    
    
if __name__ == "__main__":
    script_path()
    width, height = (800, 800)
    center = tuple(map(int, (width/2, height/2)))
    img = vs.blank_image(height, width, value=0)
    
    
    # ******* window setup *******
    fullscreen = False
    window_title = 'img'
    if fullscreen:
        cv2.namedWindow(window_title, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow(window_title)
        
        
    # ******* mouse events *******
    handler = MouseHandler(height, width)
    cv2.setMouseCallback(window_title, handler.handle_event)
    
    
    # ******* main loop *******
    quit_app = False
    while True:
        img[:, :] = 0

        # ******* map keyboard events *******
        code = cv2.waitKey(1) & 0xFF
        if code != 255:
            char = chr(code)

            if char == 'q':
                # set quit_app
                quit_app = True
                
                

        
        
        # *********** mouse handler ***********
        center_x = handler.center_x
        center_y = handler.center_y
        cursor_x = handler.cursor_x
        cursor_y = handler.cursor_y
        
        
        short_axis_divider = max(int(round((center_y/height)*30)), 1)
        short_axis_divider = (center_y-(height/2))/(height/2)
        ellipses_number = max(int(round((center_x/height)*100)), 1)
        print('short_axis_divider: {}, ellipses_number: {}'.format(short_axis_divider, ellipses_number))
        sphere_center_x = width/2
        sphere_center_y = height/2
        sphere_radius = 300
        sphere_center = tuple(map(int, (sphere_center_x, sphere_center_y)))
        
        
        # *********** draw additional ***********
        # draw_cross(img, width, height)
        # cv2.circle(img, sphere_center, sphere_radius, (50, 50, 255), 1)
        
        
        
        # *********** draw horizontal ellipses ***********
        # ellipses_container = generate_ellipses_seq(sphere_center_x, sphere_center_y, sphere_radius, short_axis_divider, ellipses_number)
        ellipses_container = generate_ellipses_seq(sphere_center_x, sphere_center_y, sphere_radius, short_axis_divider, 20)
        for (center, long_axis, short_axis, color, start_angle, end_angle) in ellipses_container:
            cv2.ellipse(img, center, (long_axis, short_axis), 0, start_angle, end_angle, color, 2, lineType=cv2.LINE_AA)
            
            
        # *********** draw vertical ellipses ***********
        pass
        
        # ******* show image *******
        cv2.imshow(window_title, img)
        
        
        if quit_app:
            # break loop, close window and quit from main
            break
            
            
    # ******* CLEANUP *******
    cv2.destroyAllWindows()
    # return None
    cv2.imwrite('sphere.png', img)
    # vs.show_image('img', img)
    
    
'''
info:
    image = cv2.ellipse(image, center_coordinates, axesLength, angle, startAngle, endAngle, color, thickness) 
    
    
'''


import sys
import os
import numpy as np
import cv2
import vision_stuff as vs


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def blank_image(height, width, layers=3, value=255):
    '''create blank image, with specified shape, layers and initial value'''
    img = np.zeros([height, width, layers], dtype=np.uint8)
    img[:, :] = value
    return img
    
    
def colors_list():
    data = [
        (255, 30, 30),      # blue
        (30, 255, 30),      # green
        (30, 30, 255),      # red
        (255, 255, 30),     # blue-green
        (30, 255, 255),     # green-red
        (255, 30, 255),     # blue-red
        (30, 30, 30),       # black
        (180, 180, 180),    # white
        (50, 100, 150),     # some
        (150, 50, 100),     # thing
        ]
        
    # data = [
        # (255, 100, 100),    # blue
        # (100, 255, 100),    # green
        # (100, 100, 255),    # red
        # (255, 255, 100),    # blue-green
        # (100, 255, 255),    # green-red
        # (255, 100, 255),    # blue-red
        # (40, 40, 40),       # black
        # (220, 220, 220),    # white
        # (100, 150, 200),    # some
        # (200, 100, 150),    # thing
        # ]
        
    return data
    
    
if __name__ == "__main__":    
    script_path()
    
    images = []
    colors = colors_list()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_black = (0, 0, 0)
    font_white = (255, 255, 255)
    
    for key, color in enumerate(colors):
        img = blank_image(100, 600, layers=3, value=color)
        cv2.putText(img, str(key), (25, 80), font, 3, font_black, 5, cv2.LINE_AA) # black letter
        cv2.putText(img, str(key), (25, 80), font, 3, font_white, 2, cv2.LINE_AA) # white letter
        images.append(img)
        
    out = np.concatenate(images, axis=0)
    cv2.imwrite('out.png', out)
    vs.show_image('img', out)

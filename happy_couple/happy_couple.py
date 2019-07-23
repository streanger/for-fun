''' this is script, for make animation from "revnege of the nerds" movie '''
import sys
import os
import time
import random
import numpy as np
import cv2


def script_path():
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)
    return currentPath
    
    
def random_codes():
    # codes = [random.randrange(21, 65) for x in range(5)]
    codes = [random.randrange(21, 112) for x in range(5)]
    return codes
    
    
def time_template():
    template = time.strftime("%Y%m%d_%H%M%S")
    return template
    
    
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
    
    
def create_blank_image(height, width):
    image = np.zeros((height, width, 3), np.uint8)
    image += 55
    return image
    
    
def draw_tv_background_and_backlight(img):
    return img*1
    
    
def extract_countours(img):
    return True
    
    
def get_views(key):
    ''' store here all views
        think of cut single view, to parts
        store data with alpha layer
    '''
    data = {
        'view_00': 1,
        'view_01': 1,
        'view_02': 1,
        'view_03': 1
        }
    return data[key]
    
    
def help_content():
    some = '''
    start       --create window to draw image
    exit, quit  --finish drawing
    help        --this help content
    save        --save image as "drawing.png"
    draw        --draw some random line
    '''
    return some
    
    
if __name__ == "__main__":
    currentPath = script_path()
    if False:
        height, width = 500, 700
        blank = create_blank_image(height, width)
        img = draw_tv_background_and_backlight(blank)       # draw some background(for now return the same image)
        # show_image('img', img)
        toStart = False
        print("> type commands, to start drawing")
        while True:
            command = input("> ")
            
            if command == 'help':
                content = help_content()
                print(content)
                
            elif command == 'draw':
                cv2.line(img, (random.randrange(height), random.randrange(width)),
                              (random.randrange(height), random.randrange(width)),
                              (155, 255, 155), 2)
                              
            elif command == 'start':
                toStart = True
                
            elif command in ('exit', 'quit'):
                break
                
            elif command == 'save':
                cv2.imwrite('drawing_{}.png'.format(time_template()), img)
                
            elif command == 'move':
                print("(move scene is now executed)")
                
            if toStart:
                # script need to update image when commands are typed
                
                # images need to be join, just before drawing
                cv2.imshow('img', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            time.sleep(0.1)     # is it really needed?
        cv2.destroyAllWindows()
        print("\n> drawing finished")
    
    
    currentPath = script_path()
    dir = 'extracted_views'
    if not os.path.exists(dir):
        os.makedirs(dir)
    newPath = os.path.join(currentPath, dir)
    
    
    files = [item for item in os.listdir() if item.startswith('view') and item.endswith('.png')]
    for key, file in enumerate(files):
        img = cv2.imread(file, 0)
        height, width = img.shape[:2]
        blank = create_blank_image(height, width)
        
        
        # ************** threshold **************
        '''
        # th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)
        th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)        # image save in this configuration
        # th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 19, 6)
        # cv2.imwrite(os.path.join(newPath, "th_{}".format(file)), th)
        show_image('th', th)
        '''
        
        
        # ************** contours **************
        '''
        # ret,thresh = cv2.threshold(img,127,255,0)
        thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 19, 6)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # To draw all the contours in an image:
        cv2.drawContours(blank, contours, -1, (0,255,0), 1)
        
        #To draw an individual contour, say 4th contour:
        # cv2.drawContours(blank, contours, 3, (0,255,0), 1)

        #But most of the time, below method will be useful:
        # cnt = contours[4]
        # cv2.drawContours(blank, [cnt], 0, (0,255,0), 1)
    
        show_image('blank', blank)
        '''
        
        
        # ************** extract from edited manually **************
        
        
        
'''
info:
    -humans originally are orange
    -make real tv background
    -store extracted data(from original views) in extracted_views directory
    -make function for tilting image
    -think of some sounds while drawing
    -every added image should exist as subimage, which let us to move it
    -for lazy people make sequence, which executes every time enter is typing into input
    -
    
    
'''

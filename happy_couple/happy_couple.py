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
    
    
def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))
           
           
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
    
    
def smooth_image(img, numberOfBlurs=5):
    ''' https://stackoverflow.com/questions/37409811/smoothing-edges-of-a-binary-image '''
    ret, thresh = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY);
    blurredImage = cv2.pyrUp(thresh);
    for x in range(numberOfBlurs):
        # blurredImage = cv2.medianBlur(blurredImage, 7);
        blurredImage = cv2.medianBlur(blurredImage, 5);
    blurredImage = cv2.pyrDown(blurredImage);
    ret, thresh = cv2.threshold(blurredImage, 155, 255, cv2.THRESH_BINARY);
    return thresh
    # return blurredImage
    
    
def cat_images(img1, img2, axisVal):
    if not axisVal in (0, 1):
        return img1             # if wrong axisVal parameter, return first image
    return np.concatenate((img1, img2), axis=axisVal)
    
    
def create_new_dir(dir):
    currentPath = script_path()
    # dir = 'extracted_views'
    if not os.path.exists(dir):
        os.makedirs(dir)
    newPath = os.path.join(currentPath, dir)
    return newPath
    
    
def path_last_element(path):
    return os.path.basename(os.path.normpath(path))
    
    
def generate_images():
    ''' function was used in early stage '''
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
        
        
        # ************** make one-time smooth operation **************
        '''
        smoothedDir = create_new_dir('smoothed')
        paths = absoluteFilePaths('edited_manually')
        for file in paths:
            img = cv2.imread(file, 0)
            smoothed = smooth_image(img, 2)
            fileOut = os.path.join(smoothedDir, path_last_element(file))
            cv2.imwrite(fileOut, smoothed)
            print(fileOut)
            # out = cat_images(img, smoothed, 1)
            # show_image('out', out)
        '''
        
        
        # ************** extract colored lines **************
        '''
        lines_only = create_new_dir('lines_only')
        paths = absoluteFilePaths('colored')
        colors = (132, 170, 237)     # is it orange?
        colors = (62, 158, 255)     # is it orange?
        for file in paths:
            img = cv2.imread(file, 1)
            # https://pythonprogramming.net/color-filter-python-opencv-tutorial/
            lower_green = np.array([00, 150, 00])
            upper_green = np.array([255, 200, 255])
            mask = cv2.inRange(img, lower_green, upper_green)   # this extracts green elements
            B, G, R = [cv2.bitwise_and(mask+color, mask+color, mask=mask) for color in colors]
            
            alpha = mask*1
            BGR = cv2.merge((B, G, R, alpha)) # join layers
            # show_image('BGR', BGR)
            fileOut = os.path.join(lines_only, path_last_element(file))
            cv2.imwrite(fileOut, BGR)
        '''
        
    return True
    
    
def draw_parts():
    ''' extract parts from image, which are not connected, and draw them one by one '''
    return True
    

def draw_up_down():
    ''' draw image from up to down, line by line '''
    return True
    
    
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
                
            elif command == 'light':
                print("(put some light on the top of the image")
                
            if toStart:
                # script need to update image when commands are typed
                
                # images need to be join, just before drawing
                cv2.imshow('img', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            time.sleep(0.1)     # is it really needed?
        cv2.destroyAllWindows()
        print("\n> drawing finished")
        
        
    # ************** do something here **************
    pass
    
    
    # ************** make morphologial operations **************
    # images need to be thicker
    
    
    
    
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

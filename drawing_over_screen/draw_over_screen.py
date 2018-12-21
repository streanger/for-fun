import win32gui
import win32api
import time

import sys
import os
import ctypes
import random
import cv2
import numpy as np


def script_path():
    '''change current path to script one'''
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)
    return currentPath
    
    
def get_state(key):
    '''
    VK_CAPITAL  - 0x14  - CAPS LOCK key
    VK_NUMLOCK  - 0x90  - NUM LOCK key
    VK_SCROLL   - 0x91  - SCROLL LOCK key
    VK_ADD      - 0x6B  - ADD key
    VK_SUBTRACT - 0x6D  - SUBSTRACT key
    
    static states:
        off             ->  0
        on              ->  1
        off & pressed   ->  -128
        on & pressed    ->  -127
        
    https://docs.microsoft.com/pl-pl/windows/desktop/inputdev/virtual-key-codes
    '''
    hllDll = ctypes.WinDLL("User32.dll")
    return hllDll.GetKeyState(key)
    
    
def draw_on_screen():
    print("--> use scroll lock, to stop/start drawing")
    dc = win32gui.GetDC(0)
    currentColor = win32api.RGB(255, 100, 220)
    radius = 10
    
    radiusBufferRange = 10                  # it affects on speed of size changes
    radiusBuffer = radiusBufferRange // 2
    while True:
        pos_x, pos_y = win32gui.GetCursorPos()
        
        # read 'add' 'sub' keys
        addKey = get_state(0x6b)
        subKey = get_state(0x6d)
        if addKey in (-127, -128):
            radiusBuffer += 1
        if subKey in (-127, -128):
            radiusBuffer -= 1

        
        # resize buffer
        if radiusBuffer > radiusBufferRange:
            radius += 1
            radiusBuffer = 1
            continue
        if radiusBuffer < 1:
            radius -= 1
            radiusBuffer = radiusBufferRange
            time.sleep(0.01)
            continue
        
        # resize brush
        if radius < 1:
            radius = 1
        if radius > 40:
            radius = 40
            
        # print("radiusBuffer: {}, {}".format(radiusBuffer, radius))
        
        circlePoints = get_circle_array(radius)
        positions = tuple([(pos_x + item[0], pos_y + item[1]) for item in circlePoints])
        keyState = get_state(0x91)      # scroll lock
        if keyState == 1:
            for posX, posY in positions:
                try:
                    win32gui.SetPixel(dc, posX, posY, currentColor)
                    # think of drawing image instead of circle
                except:
                    time.sleep(0.001)
        currentColor = win32api.RGB(random.randrange(256), random.randrange(256), random.randrange(256))
    return True
    
    
def get_circle_array(radius):
    '''
    -radius must be integer 
    -based on: https://stackoverflow.com/questions/8647024/how-to-apply-a-disc-shaped-mask-to-a-numpy-array
    '''
    a = b = radius                          # circle center
    n = radius*2 + 1                        # size of square
    y,x = np.ogrid[-a:n-a, -b:n-b]
    mask = x*x + y*y <= radius*radius
    circle = np.zeros((n, n))
    circle[mask] = 1
    onePoints = np.where(circle > 0)
    pairs = tuple(zip(onePoints[0]-radius, onePoints[1]-radius))
    return pairs
    
    
def draw_image(file):
    colorful = 1
    img = cv2.imread(file, colorful)
    if colorful:
        shapeX, shapeY, _ = img.shape
    else:
        shapeX, shapeY = img.shape
    dc = win32gui.GetDC(0)
    startPos = (100, 100)
    failed = False
    for level in range(shapeX):
        if failed:
            break
        vector = img[level]
        for key, pixel in enumerate(vector):
            if colorful:
                currentColor = win32api.RGB(pixel[2], pixel[1], pixel[0])
            else:
                currentColor = win32api.RGB(pixel, pixel, pixel)
            try:
                win32gui.SetPixel(dc, key+startPos[0], level+startPos[1], currentColor)
            except:
                failed = True
                print("--> image went over screen")
                break
    print("--> drawing finished")
    return True
    
    
if __name__ == "__main__":    
    currentPath = script_path()
    # draw_image("python.jpg")
    draw_on_screen()
    
    
'''
todo:
-add resizing brush with using +-   (done)
-add refresh for screen
-add colors manipulation
'''

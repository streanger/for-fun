import win32gui
import win32api
import time

import sys
import os
import ctypes
import random
import cv2

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
    '''
    hllDll = ctypes.WinDLL("User32.dll")
    # return hllDll.GetAsyncKeyState(key)
    return hllDll.GetKeyState(key)
    
    
def draw_on_screen():
    print("--> use scroll lock, to stop/start drawing")
    dc = win32gui.GetDC(0)
    currentColor = win32api.RGB(255, 0, 0)
    while True:
        pos_x, pos_y = win32gui.GetCursorPos()
        positions = ((pos_x, pos_y),
                     (pos_x+1, pos_y),
                     (pos_x, pos_y+1),
                     (pos_x-1, pos_y),
                     (pos_x, pos_y-1),
                     (pos_x+1, pos_y+1),
                     (pos_x-1, pos_y-1))
        keyState = get_state(0x91)      # scroll lock
        if keyState == 1:
            for posX, posY in positions:
                try:
                    win32gui.SetPixel(dc, posX, posY, currentColor)
                except:
                    time.sleep(0.001)
        currentColor = win32api.RGB(random.randrange(256), random.randrange(256), random.randrange(256))
    return True
    
    
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
    draw_image("python.jpg")
    draw_on_screen()
    
'''
todo:
-add resizing brush with using +-
-add refresh for screen
-add colors manipulation
'''
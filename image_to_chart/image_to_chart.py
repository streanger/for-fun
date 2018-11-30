#!/usr/bin/python3
import math
import os
import sys
import time
import matplotlib.pyplot as plt
from pylab import savefig
import cv2
import numpy as np

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
def execute_decorator(func):
    def f(*args, **kwargs):
        # input("next step: {}...\t".format(func.__name__))
        before = time.time()
        val = func(*args, **kwargs)
        total = round((time.time() - before), 6)
        print("--> <{}> finished in {} [s]".format(func.__name__, total))
        return val
    return f
    
def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def make_vector(someArray):
    #convert 2d, n-size array/matrix to 1d vector
    h = someArray.shape[0]
    someArray = someArray.flatten(1)
    # print(h)
    return [mean(someArray[i:i+h]) for i in range(0,len(someArray),h)]
    
# @execute_decorator
def vertical_sharpening(img):
    '''
    -makes image thinner
    -remember: try to avoid converting numpy array to list -> it slows app down
    '''
    ySize, xSize = img.shape
    for x in range(xSize):
        # print("{}/{}".format(x, xSize))
        vector = img[:, x]
        if not 0 in vector:
            continue
        indexes = np.where(vector == 0)[0]
        start = indexes[0]
        stop = indexes[-1] + 1
        if start == 0:
            start = None
        if stop == 0:
            stop = None
        center = vector[start:stop]
        center.fill(1)
        center[len(center)//2] = 0       # put '0' in the center
        vector[start:stop] = center
        img[:, x] = vector
    return img
    
def plot_chart(xData, yData, title):
    plt.plot(xData, yData, linewidth=1)
    # plt.axis([0, 6, 0, 20])
    plt.grid()
    plt.title(title)
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')       #full window
    plt.show()
    plt.close()
    return True

# @execute_decorator
def shrink_img(img, side):
    position = 0
    factor = 1
    ySize, xSize = img.shape
    if side in ("left", "right"):
        if side == "right":
            factor = -1
        for x in range(xSize):
            column = img[:, factor*x]
            if np.any(column == 0):
                if side == "right":
                    position = xSize - x
                else:
                    position = x
                break
    if side in ("up", "down"):
        if side == "down":
            factor = -1
        for y in range(ySize):
            column = img[factor*y,:]
            if np.any(column == 0):
                if side == "down":
                    position = ySize - y
                else:
                    position = y
                break
    return position

@execute_decorator
def image_to_chart(img, scaleY, title):
    '''
    todo:
        -add some scaling (for x in y axis)
        -think of creating class
    '''
    ret, thresh = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
    thresh = thresh//255
    leftSide = shrink_img(thresh, "left")
    rightSide = shrink_img(thresh, "right")
    upSide = shrink_img(thresh, "up")
    downSide = shrink_img(thresh, "down")
    
    outImg = thresh[upSide:downSide, leftSide:rightSide]
    sharpen = vertical_sharpening(outImg)
    sharpen = np.flipud(sharpen)
    points = np.where(sharpen == 0)
    xData, yData = zip(*sorted(zip(points[1].tolist(), points[0].tolist())))
    
    ySize, xSize = outImg.shape     # use shape of shrinked image
    yFactor = scaleY/ySize
    yData = [item*yFactor for item in yData]
    plot_chart(xData, yData, title)
    
    # show_image("sharpen", sharpen)
    # cv2.imwrite("out.png", outImg)    
    return True
    
    
if __name__ == "__main__":
    path = script_path()
    files = [item for item in os.listdir() if item.endswith(('png', 'jpg'))]
    for file in files:
        img = cv2.imread(file, 0)
        image_to_chart(img, 7, file)
        
'''
flipud -> Flip an array vertically (axis=0).
fliplr -> Flip an array horizontally (axis=1). 

column -> test[:,0] -> array([1, 3, 5])
row -> test[1,:] -> array([3, 4])
'''

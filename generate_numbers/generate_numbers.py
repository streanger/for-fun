import os
import sys
import time
import numpy as np
import cv2

def script_path():
    '''set current path to script_path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    

def generate_mirror(data):
    mirror = [item[::-1] for item in data[::-1]]
    return mirror
    
    
def generate_half(n):
    out = [(n, x) for x in range((n-1), -n, -2)]
    out.extend([(x, -n) for x in range((n-1), -n, -2)])
    return out
    
    
def generate_rn(n):
    if n == 1:
        data = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # values for start
    else:
        half = generate_half(n)
        mirror = generate_mirror(half)
        data = half + mirror
    return data
    
    
def create_image(shape):
    zeros = np.zeros((shape[0], shape[1], 3), dtype=np.uint8)
    # resized = np.array(np.repeat(np.repeat(pixel, 100, axis=0), 100, axis=1))
    return zeros
    
    
def generate_numbers():
    '''
    define some formula to calc number in sequence
    -x + x -> 0
    0 + 0 -> -1
    x + y -> -(x + y)
    '''
    return 42
    
    
def create_picture(data, shape):
    img = create_image(shape)            # create blank image
    centerX = round(shape[0]/2)
    centerY = round(shape[1]/2)
    for key, (x_pos, y_pos) in enumerate(data):
        # img[x_pos+centerX, y_pos+centerY] = (key*centerX % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key % 255)
        img[x_pos+centerX, y_pos+centerY] = (key**2 % 255)
        
        # Display the resulting frame
        # size = 3
        # frame = np.repeat(np.repeat(img, size, axis=0), size, axis=1)
        # cv2.imshow('frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
            # break
        # time.sleep(0.001)
    # cv2.destroyAllWindows()
    return img
    
    
if __name__ == "__main__":
    script_path()

    # generate data in some range
    data = []
    for x in range(1, 450):
        data.extend(generate_rn(x))
        
    # this is just the side effect of my work, but its very impressive
    picture = create_picture(data, (900, 900))
    out = np.repeat(np.repeat(picture, 2, axis=0), 2, axis=1)
    cv2.imwrite('hole.png', out)
    
    # do something with the data
    
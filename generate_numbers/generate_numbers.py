import os
import sys
import time
import numpy as np
import cv2
import math

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
        # img[x_pos+centerX, y_pos+centerY] = (key*(math.sin(x_pos/360) + math.sin(y_pos/360)) % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*(math.sin((x_pos**2)/360000) + math.sin((y_pos**2)/360000)) % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*(math.sin(math.sin(x_pos*(y_pos + x_pos)/360000)) + math.sin(0.000010007*key)*0.002*(x_pos/(2)) + math.sin(math.sin((x_pos + y_pos)/360000))) % 255)
        # img[x_pos+centerX, y_pos+centerY] = (x_pos*(math.sin(math.sin(x_pos*(y_pos + x_pos)/360000)) + math.sin(0.000010007*key)*0.002*(x_pos/(2))*math.cos(0.00015007*key)*0.002*(y_pos/(2))*10 + math.sin(math.sin((x_pos + y_pos)/360000))) % 255)
        
        # '''
        out = (x_pos**2 + y_pos**2)**(0.5)
        p = (abs(x_pos) + abs(y_pos) + key)/2
        trip = (abs(p*(p-x_pos)*(p-y_pos)*(p-key)))**(0.4)
        # print(trip)
        # print(p, x_pos, y_pos, key)
        # trip = trip.real
        # trip = trip.real
        # '''
        # img[x_pos+centerX, y_pos+centerY] = (key*(x_pos+50)*(y_pos/10)*(math.tan((out)/100) + math.sin((out)/100))/1000000 % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*(x_pos+50)*(y_pos/10)*(math.tan((trip)/100)**2 + 1/(math.tan((out)/100)**2) + math.sin((out)/120)**2 - math.cos((out)/110)**2)/100000000 % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*(x_pos+50)*(y_pos/10)*(math.tan((trip)/100)**2*1/(math.tan((out)/100)**2)*math.sin((trip)/120)**2*math.cos((out)/110)**2)/100000 % 255)
        
        # img[x_pos+centerX, y_pos+centerY] = (key*(x_pos+50)*(y_pos/10)*((math.sin((out)/120)+1)**(math.cos((out)/110)*2))/100000 % 255)
        img[x_pos+centerX, y_pos+centerY] = (key*x_pos*y_pos*((math.sin((trip + out)/180)+1)**(math.cos((y_pos + x_pos)/36)))/10000000 % 255)
        
        
        
        # print(math.sin(trip*10000))
        # print(out, p, trip)
        # img[x_pos+centerX, y_pos+centerY] = (key*(math.sin(0.000000010007*y_pos*key))*(math.sin(math.sin(x_pos*(y_pos + x_pos)/360000)) + math.sin(0.000010007*key)*0.002*(x_pos/(2))*math.cos(0.00015007*key)*0.002*(y_pos/(2))*10 + math.sin(math.sin((x_pos + y_pos)/360000))) % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*x_pos*y_pos*(math.tan((out)/100) + math.sin((out)/100))/1000000 % 255)
        # img[x_pos+centerX, y_pos+centerY] = x_pos*(math.sin(trip*100000 + out/100000)*10000 % 255)
        
        
        # img[x_pos+centerX, y_pos+centerY] = ((key+1)**(-0.23*(centerX/centerY))*300) % 255
        # img[x_pos+centerX, y_pos+centerY] = (math.sin((key/1800)*math.pi)*key + 1020) % 255
        # img[x_pos+centerX, y_pos+centerY] = 350-(key**((math.sin(math.sin((centerX/180)*centerY**(0.5)))))*20) % 255
        # img[x_pos+centerX, y_pos+centerY] = (key*(x_pos*math.sin((y_pos/36000000)*math.pi) + y_pos*math.sin((x_pos/36000000)*math.pi)) % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*((math.sin((y_pos/36000)*math.pi)) + math.sin((x_pos/36000)*math.pi)) % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*(x_pos*(math.sin((x_pos*y_pos/360000000)*math.pi)) + y_pos*math.sin((x_pos*y_pos/360000000)*math.pi)) % 255)
        # img[x_pos+centerX, y_pos+centerY] = ((key + out)*(x_pos*(math.sin((x_pos*y_pos*out/36000000000)*math.pi)) + y_pos*(math.sin((x_pos*y_pos*key/36000000000000)*math.pi)) + 0.0222) + 146 % 255)
        # img[x_pos+centerX, y_pos+centerY] = (centerX*(key/centerY)**(math.sin((centerY/45)))) % 255
        
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
    size = 500
    for x in range(1, size):
        data.extend(generate_rn(x))
        
    # this is just the side effect of my work, but its very impressive
    picture = create_picture(data, (size*2, size*2))
    out = np.repeat(np.repeat(picture, 2, axis=0), 2, axis=1)
    cv2.imwrite('hole.png', out)
    
    # do something with the data
    

import os
import sys
import time
import hashlib
import numpy as np
import cv2
import math


def script_path():
    """set current path to script_path"""
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def md5_sum(content):
    """calc md5 sum of content
    
    content is type of bytes
    keywords: md5, hash
    """
    md5_hash = hashlib.md5(content).hexdigest()
    return md5_hash
    
    
def generate_mirror(data):
    mirror = [item[::-1] for item in data[::-1]]
    return mirror
    
    
def generate_half(n):
    if True:
        out = [(n, x) for x in range((n-1), -n, -2)]
        out.extend([(x, -n) for x in range((n-1), -n, -2)])
    else:
        # this will make full image, not only chessboard
        out = [(n, x) for x in range((n-1), -n, -1)]
        out.extend([(x, -n) for x in range((n-1), -n, -1)])
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
    
    
def pixel_val(centerX, centerY, key, x_pos, y_pos, mode=1):
    """generate pixel color value"""
    if mode == 1:
        val = (key*centerX % 255)
    elif mode == 2:
        val = (key*(math.sin(x_pos/360) + math.sin(y_pos/360)) % 255)
    elif mode == 3:
        val = (key*(math.sin((x_pos**2)/360000) + math.sin((y_pos**2)/360000)) % 255)
    elif mode == 4:
        # val = (key*(math.sin(math.sin(x_pos*(y_pos + x_pos)/360000)) + math.sin(0.000010007*key)*0.002*(x_pos/(2)) + math.sin(math.sin((x_pos + y_pos)/360000))) % 255)
        # val = (key*(math.sin(math.sin(x_pos*(y_pos + x_pos)/260000)) + math.sin(0.000010007*key)*0.002*(x_pos/(2)) + math.sin(math.sin((x_pos + y_pos)/360000))) % 255)
        val = (key*(math.sin(math.sin(x_pos*(y_pos + x_pos)/460000)) - math.sin(0.000020007*key)*0.0015*(x_pos/(3)) + math.sin(math.sin((x_pos + y_pos)/16000))) % 255)
    elif mode == 5:
        # val = (x_pos*(math.sin(math.sin(x_pos*(y_pos + x_pos)/360000)) + math.sin(0.000010007*key)*0.002*(x_pos/(2))*math.cos(0.00015007*key)*0.002*(y_pos/(2))*10 + math.sin(math.sin((x_pos + y_pos)/360000))) % 255)
        val = (x_pos*(math.sin(math.sin(x_pos*(y_pos + x_pos)/460000)) + math.sin(0.00040007*key)*0.002*(x_pos/(2))*math.cos(0.0015007*key)*0.03*(y_pos/(14.5))*10 + math.sin(math.sin((x_pos + y_pos)/360000))) % 255)
    elif mode == 6:
        val = ((key+1)**(-0.23*(centerX/centerY))*300) % 255
    elif mode == 7:
        val = (math.sin((key/1800)*math.pi)*key + 1020) % 255
    elif mode == 8:
        val = 0
    elif mode == 9:
        val = 0
    elif mode == 10:
        val = (key*(x_pos*math.sin((y_pos/36000000)*math.pi) + y_pos*math.sin((x_pos/36000000)*math.pi)) % 255)
    elif mode == 11:
        val = (key*(x_pos*math.sin((y_pos/36000000)*math.pi) + y_pos*math.sin((x_pos/36000000)*math.pi)) % 255)
    elif mode == 12:
        val = (key*((math.sin((y_pos/36000)*math.pi)) + math.sin((x_pos/36000)*math.pi)) % 255)
    elif mode == 13:
        val = (key*(x_pos*(math.sin((x_pos*y_pos/360000000)*math.pi)) + y_pos*math.sin((x_pos*y_pos/360000000)*math.pi)) % 255)
    elif mode == 14:
        val = ((x_pos*(math.sin(math.sin(x_pos*(y_pos + x_pos)/360000)) + math.sin(0.000010007*key)*0.002*(x_pos/(2))*math.cos(0.00015007*key)*0.002*(y_pos/(2))*10 + math.sin(math.sin((x_pos + y_pos)/360000)))) - (key*(math.sin(math.sin(x_pos*(y_pos + x_pos)/360000)) + math.sin(0.00010007*key)*0.002*(x_pos/(2)) + math.sin(math.sin((x_pos + y_pos)/360000))))) % 255
    elif mode == 15:
        # centerX, centerY, key, x_pos, y_pos
        # val = ((centerX ** 2.2) * math.cos(math.sin(0.000001 * y_pos)) - (centerY ** 2.5) * math.cos(0.001 * x_pos) + key) % 255
        # val = ((centerX ** 2.2) * math.cos(math.sin(0.000001 * y_pos)) + (centerY ** 2.5) * math.cos(0.001 * x_pos) + key) % 255
        # val = (((centerX ** 0.0002) * math.cos(math.sin(0.001 * y_pos))) ** ((centerY ** 0.001) * math.cos(0.0001 * x_pos) + key)) % 255
        # val = (((centerX ** 0.0002) * math.cos(math.sin(0.0015 * y_pos))) ** ((centerY ** 0.001) * math.cos(0.0001 * x_pos) + key)) % 255
        val = (((centerX ** 0.00015) * math.cos(math.sin(0.000245 * (y_pos + x_pos)))) ** ((centerY ** 0.01) * math.cos(0.001 * x_pos/2) + key)) % 255
        # val = (((centerX ** 0.00015) * math.cos(math.sin(0.000445 * (y_pos + (x_pos/2)**2)))) ** ((centerY ** 0.01) * math.cos(0.001 * x_pos/2) + key)) % 255
    elif mode == 16:
        val = 0
    elif mode == 17:
        val = 0
    elif mode == 18:
        val = 0
    elif mode == 19:
        val = 0
    elif mode == 20:
        val = 0
    return val
    
    
def create_picture(data, shape, mode):
    img = create_image(shape)            # create blank image
    centerX = round(shape[0]/2)
    centerY = round(shape[1]/2)
    for key, (x_pos, y_pos) in enumerate(data):
        img[x_pos+centerX, y_pos+centerY] = pixel_val(centerX, centerY, key, x_pos, y_pos, mode=mode)
        # img[x_pos+centerX, y_pos+centerY] = (key*centerX % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*(math.sin(x_pos/360) + math.sin(y_pos/360)) % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*(math.sin((x_pos**2)/360000) + math.sin((y_pos**2)/360000)) % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*(math.sin(math.sin(x_pos*(y_pos + x_pos)/360000)) + math.sin(0.000010007*key)*0.002*(x_pos/(2)) + math.sin(math.sin((x_pos + y_pos)/360000))) % 255)
        # img[x_pos+centerX, y_pos+centerY] = (x_pos*(math.sin(math.sin(x_pos*(y_pos + x_pos)/360000)) + math.sin(0.000010007*key)*0.002*(x_pos/(2))*math.cos(0.00015007*key)*0.002*(y_pos/(2))*10 + math.sin(math.sin((x_pos + y_pos)/360000))) % 255)
        
        # '''
        # out = (x_pos**2 + y_pos**2)**(0.5)
        # p = (abs(x_pos) + abs(y_pos) + key)/2
        # trip = (abs(p*(p-x_pos)*(p-y_pos)*(p-key)))**(0.4)
        
        # print(trip)
        # print(p, x_pos, y_pos, key)
        # trip = trip.real
        # trip = trip.real
        # '''
        # img[x_pos+centerX, y_pos+centerY] = (key*(x_pos+50)*(y_pos/10)*(math.tan((out)/100) + math.sin((out)/100))/1000000 % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*(x_pos+50)*(y_pos/10)*(math.tan((trip)/100)**2 + 1/(math.tan((out)/100)**2) + math.sin((out)/120)**2 - math.cos((out)/110)**2)/100000000 % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*(x_pos+50)*(y_pos/10)*(math.tan((trip)/100)**2*1/(math.tan((out)/100)**2)*math.sin((trip)/120)**2*math.cos((out)/110)**2)/100000 % 255)
        
        # img[x_pos+centerX, y_pos+centerY] = (key*(x_pos+50)*(y_pos/10)*((math.sin((out)/120)+1)**(math.cos((out)/110)*2))/100000 % 255)
        # img[x_pos+centerX, y_pos+centerY] = (key*x_pos*y_pos*((math.sin((trip + out)/180)+1)**(math.cos((y_pos + x_pos)/36)))/10000000 % 255)
        
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
    for x in range(1, 16):
        x = 15
        picture = create_picture(data, (size*2, size*2), mode=x)
        out = np.repeat(np.repeat(picture, 2, axis=0), 2, axis=1)
        out_bytes = out.tobytes()
        out_md5_sum = md5_sum(out_bytes)
        filename = '{}-{}.png'.format(x, out_md5_sum)
        cv2.imwrite(filename, out)
        print('[*] saved to: {}'.format(filename))
        break
    # do something with the data
    
    
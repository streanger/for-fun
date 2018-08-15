#!/usr/bin/python3
#updated version of resizeImageV2.py
import sys
import os
import cv2
import numpy as np

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path

def get_files(fileTypes=("png", "jpeg", "jpg")):
    files = [item for item in os.listdir() if (item.lower()).split('.')[-1] in fileTypes]
    return files

def make_dir(new_dir):
    'make new dir, switch to it and retur new path'
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(path, new_dir)
    return new_path    

def show_img(img, title):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
def resize_cut_and_alpha_image(file_name, new_height, new_width):
    subDir = "RESIZED"
    image = cv2.imread(file_name)
    resized = cv2.resize(image, (new_width, new_height))
    #cut circle here
    b_channel, g_channel, r_channel = cv2.split(resized)
    alpha_channel = np.zeros((new_width, new_height,1), dtype='uint8')      #add alpha channel; in ones multiply e.g. *100
    cv2.ellipse(alpha_channel, (int(new_width/2), int(new_height/2)), (int(new_width/2), int(new_height/2)), 0, 0 , 360, (255), -1)     #draw circle
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))   
    maskedImg = cv2.bitwise_and(img_BGRA, img_BGRA, mask=alpha_channel)
    #show_img(alpha_channel, "alpha image")
    #show_img(maskedImg, "masked")
    path = make_dir(subDir)
    path = os.path.join(path, file_name)
    cv2.imwrite(path, maskedImg)
    return True

def read_alpha_channel_image(file_name):
    #
    some = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    channels = cv2.split(some)      #split channels
    return some
    
    
if __name__ == "__main__":
    args = sys.argv[1:]
    path = script_path()
    #file = args[0]
    #file = "berk.png"
    #status = resize_cut_and_alpha_image(file, 80, 80)
    files = get_files()
    for file in files:
        status = resize_cut_and_alpha_image(file, 80, 80)
    print("finished...")
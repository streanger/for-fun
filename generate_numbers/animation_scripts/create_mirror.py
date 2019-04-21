import os
import sys
import numpy as np
import cv2


def script_path():
    '''set current path to script_path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def create_images_mirror():
    ''' get the list of images, reverse it, rename to be sequence and save '''
    images = [item for item in os.listdir() if item.endswith('.png')]
    reversed = images.copy()
    reversed.reverse()
    renamed = ['{}_{}.png'.format(item.split('_')[0], str(len(reversed)+key).zfill(2)) for key, item in enumerate(reversed)]
    pairs = list(zip(renamed, reversed))
    for (new, file) in pairs:
        img = cv2.imread(file)
        cv2.imwrite(new, img)
        # pass
        print("{} created".format(new))
    return True
    
    
if __name__ == "__main__":
    script_path()
    create_images_mirror()
    
    
    
    
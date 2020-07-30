import sys
import os
import numpy as np
import cv2


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
if __name__ == "__main__":
    script_path()
    directory = 'muminek'
    files = [(file, os.path.join(directory, file)) for file in os.listdir(directory)]
    
    left = 30
    up = 50
    right = 305
    down = 220
    
    
    new_directory = 'muminek_cut'
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
        
    for file, file_path in files:
        img = cv2.imread(file_path, 1)
        out = img[up:down, left:right]
        file_out = os.path.join(new_directory, file)
        cv2.imwrite(file_out, out)
        
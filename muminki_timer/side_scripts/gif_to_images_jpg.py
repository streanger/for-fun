import sys
import os

from PIL import Image, ImageFile
import numpy as np
import cv2

# from plot_3d import plot_figure

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path
    
    
def make_dir(current_path, new_dir):
    ''' make new dir and return new path '''
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(current_path, new_dir)
    return new_path
    
    
def gif_to_images(file):
    '''think of catching frames directly to memory
    https://stackoverflow.com/questions/6788398/how-to-save-progressive-jpeg-using-python-pil-1-1-7
    https://stackoverflow.com/questions/21669657/getting-cannot-write-mode-p-as-jpeg-while-operating-on-jpg-image
    '''
    ImageFile.MAXBLOCK = 2**20
    
    img = Image.open(file)
    counter = 0
    newDir = make_dir(script_path(), file.split('.')[0])
    while True:
        try:
            # frame = os.path.join(newDir, "frame{:02}.png".format(counter))
            frame = os.path.join(newDir, "frame{:02}.jpg".format(counter))
            img.seek(counter)
            # img = img.convert('RGB')
            # img.save(frame)
            # img.save(frame, "JPEG", quality=80, optimize=True, progressive=True)
            img.convert('RGB').save(frame, "JPEG", quality=80, optimize=True, progressive=True)
            counter += 1
            # print("frame: {} saved".format(frame))
        except EOFError:
            # print("end of gif")
            break
    return True
    
    
def image_to_3d_shape(img):
    ''' at first think of using matplotlib 3d '''
    return True
    
    
if __name__ == "__main__":
    script_path()
    # data = gif_to_images("champion.gif")
    # data = gif_to_images("behemot.gif")
    data = gif_to_images("muminek.gif")
    
    
    '''
    img_path = os.path.join(script_path(), 'champion', 'frame00.png')
    # print(img_path)
    img = cv2.imread(img_path, 0)
    img[img == 178] = 0         # replace all elements in array equal to X
    img = (img/20)
    img[img > 0] += 20
    plot_figure(img)
    '''

    
    
    
    
'''
-at first think of using matplotlib 3d


'''

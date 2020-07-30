#!/usr/bin/python3
import sys
import os
import time
import random
import numpy as np
import cv2


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def show_image(title, image):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def blank_image(height, width, layers=3):
    img = np.ones((height, width, layers), dtype=np.uint8)*255
    return img
    
    
def make_video(images, outvid="video.avi", fps=5, size=None,
               is_color=True, format="XVID"):
    fourcc = cv2.VideoWriter_fourcc(*format)
    vid = None
    imNumber = len(images)
    for key, file in enumerate(images):
        print(file)
        img = cv2.imread(file)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = cv2.resize(img, size)
        vid.write(img)
        #print("Progress: {0}%".format((key+1)/imNumber*100), end="\r", flush=True)
    cv2.destroyAllWindows()
    vid.release()
    return vid
    
    
def make_video(points_pairs, outvid="video.avi", fps=5, size=None, is_color=True, format="XVID"):
    fourcc = cv2.VideoWriter_fourcc(*format)
    vid = None

    color = (50, 50, 255)
    thickness = 3
    img = blank_image(150, 600)
    points_pairs.insert(0, ((0, 0), (0, 0)))
    points_pairs += [points_pairs[-1]]*10
    for key, (p1, p2) in enumerate(points_pairs):
        if key:
            img = cv2.line(img, p1, p2, color, thickness)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = cv2.resize(img, size)
        vid.write(img)
    vid.release()
    return vid
    
    
def clear_timer(total_time_in_seconds=60):
    '''it creates video with timer of time specified in parameter'''
    # ******* SETUP *******
    
    # image setup
    height, width = 720, 1280
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale, thickness = 6, 5
    
    
    # video setup
    size = None
    is_color = True
    format = "XVID"
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*format)
    vid = None
    color = (50, 50, 255)
    
    # total_time_in_seconds = 60
    outvid = "out_{}.avi".format(total_time_in_seconds)
    
    
    for val in range(total_time_in_seconds+1)[::-1]:
        text = '{:02}:{:02}'.format(*divmod(val, 60))
        print(text)
        img = blank_image(height, width)
        
        
        # calc text position
        (label_width, label_height), baseline = cv2.getTextSize(text, font, fontScale, thickness)
        text_start_x = round((width - label_width)/2)
        text_start_y = round((height - label_height)/2)
        cv2.putText(img, text, (text_start_x, text_start_y+label_height), font, fontScale, (55, 55, 55), thickness, cv2.LINE_AA)
        
        # draw rounded rectangle
        pass
        
        # draw muminek gif
        
        # total time need to be equal total_time_in_seconds
        # thats why, we cut of 0.5[s] from first and last seconds
        frames_per_second = fps
        if not val or val == total_time_in_seconds:
            frames_per_second = int(fps//2)     # half of time
            
        for x in range(frames_per_second):
            if vid is None:
                if size is None:
                    size = img.shape[1], img.shape[0]
                vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
            if size[0] != img.shape[1] and size[1] != img.shape[0]:
                img = cv2.resize(img, size)
            vid.write(img)
    vid.release()
    return True
    
    
def muminki_timer(total_time_in_seconds=60):
    # image setup
    height, width = 720, 1280
    font = cv2.FONT_HERSHEY_COMPLEX
    fontScale, thickness = 6, 5
    font_color = (55, 55, 55)
    
    # video setup
    size = None
    is_color = True
    format = "XVID"
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*format)
    vid = None
    background_color = (242, 245, 249)      # muminek gif background
    # total_time_in_seconds = 30
    outvid = "out_{}.avi".format(total_time_in_seconds)
    
    counter = 0
    muminek_dir = 'muminek_cut'
    muminek_files = [os.path.join(muminek_dir, file) for file in os.listdir(muminek_dir)]
    muminek_frame_no = len(muminek_files)
    muminek_current_frame = 0
    
    
    for val in range(total_time_in_seconds+1)[::-1]:
        text = '{:02}:{:02}'.format(*divmod(val, 60))
        print(text)
        img = blank_image(height, width)
        img[::] = background_color
        
        # calc text position
        (label_width, label_height), baseline = cv2.getTextSize(text, font, fontScale, thickness)
        text_start_x = round((width - label_width)/2)
        text_start_y = round((height - label_height)/2)
        cv2.putText(img, text, (text_start_x, text_start_y+label_height), font, fontScale, font_color, thickness, cv2.LINE_AA)
        
        # draw muminek gif (for now single frame)
        muminek_img = cv2.imread(muminek_files[muminek_current_frame], 1)
        muminek_height, muminek_width = muminek_img.shape[:2]
        move_up, move_right = -50, 50
        img[height-muminek_height-1+move_up:height-1+move_up, 0+move_right:muminek_width+move_right] = muminek_img
        
        # total time need to be equal total_time_in_seconds
        # thats why, we cut of 0.5[s] from first and last seconds
        frames_per_second = fps
        if not val or val == total_time_in_seconds:
            frames_per_second = int(fps//2)     # half of time
            
        for x in range(frames_per_second):
            counter += 1
            if not counter%7:
                # switch muminek frame
                muminek_current_frame += 1
                muminek_current_frame = muminek_current_frame%muminek_frame_no
                
                # draw muminek over image
                muminek_img = cv2.imread(muminek_files[muminek_current_frame], 1)
                muminek_height, muminek_width = muminek_img.shape[:2]
                move_up, move_right = -50, 50
                img[height-muminek_height-1+move_up:height-1+move_up, 0+move_right:muminek_width+move_right] = muminek_img
                
                
            if vid is None:
                if size is None:
                    size = img.shape[1], img.shape[0]
                vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
            if size[0] != img.shape[1] and size[1] != img.shape[0]:
                img = cv2.resize(img, size)
            vid.write(img)
    vid.release()
    return True
    
    
if __name__ == "__main__":
    path = script_path()
    muminki_timer(total_time_in_seconds=30)
    
    
'''
info:
    -get gif duration:
        http://gifduration.konstochvanligasaker.se
        
    -muminek gif shape, and duration:
        muminek gif lasts 2220 milliseconds
        muminek cut shape: (270x175)
        
'''

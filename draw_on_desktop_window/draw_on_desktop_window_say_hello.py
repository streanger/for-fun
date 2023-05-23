import os
import random
import sys
import time
from pathlib import Path
import tkinter as tk
from PIL import Image,ImageTk


"""
useful:
    https://www.reddit.com/r/learnpython/comments/4z5pvv/draw_ontop_of_screen_with_python/
    https://stackoverflow.com/questions/4310489/how-do-i-remove-the-light-grey-border-around-my-canvas-widget
    https://www.tutorialspoint.com/how-to-move-an-image-in-tkinter-canvas-with-arrow-keys
    https://python-course.eu/tkinter/events-and-binds-in-tkinter.php
    
"""


def script_path():
    """set current path, to script path"""
    current_path = str(Path(__file__).parent)
    os.chdir(current_path)
    return current_path


def left(e):
    print('left')
    x = -15
    y = 0
    canvas.move(img, x, y)
    
    
def right(e):
    x = 15
    y = 0
    canvas.move(img, x, y)
    
    
def up(e):
    x = 0
    y = -15
    canvas.move(img, x, y)
    
    
def down(e):
    x = 0
    y = 15
    canvas.move(img, x, y)
    
    
def hello():
    y_position = random.randrange(50, 800)
        
    canvas.moveto(img, 1600, y_position)
    for x in range(150):
        canvas.move(img, -2, 0)
        time.sleep(0.00001)
        root.update()
        
    for x in range(150):
        canvas.move(img, +2, 0)
        time.sleep(0.00001)
        root.update()


def move_sometimes():
    hello()  # say hello
    canvas.after(10*SECOND, move_sometimes)
    
    

# **** constants ****
SECOND = 1000

script_path()

# **** root setup ****
root = tk.Tk()
# root.lift()
root.attributes("-fullscreen", True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "#ffffff")

# **** canvas ****
canvas = tk.Canvas(root, height=1080, width=1920, bg='white', bd=0, highlightthickness=0, relief='ridge')
# canvas = tk.Canvas(root, height=1080, width=1920, bg='white', bd=2, highlightthickness=35, relief='ridge')
canvas.pack()

# Add image to the Canvas Items
image = ImageTk.PhotoImage(Image.open("pigeon.png"))
img = canvas.create_image(100, 100, anchor=tk.NW, image=image)

# **** Bind the move function ****
root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<Up>", up)
root.bind("<Down>", down)

# **** time dependend function ****
move_sometimes()

# **** mainloop ****
root.mainloop()

import os
import sys
from pathlib import Path
import tkinter as tk
from PIL import Image,ImageTk


# https://www.reddit.com/r/learnpython/comments/4z5pvv/draw_ontop_of_screen_with_python/
# https://stackoverflow.com/questions/4310489/how-do-i-remove-the-light-grey-border-around-my-canvas-widget


def script_path():
    """set current path, to script path"""
    current_path = str(Path(__file__).parent)
    os.chdir(current_path)
    return current_path


script_path()

root = tk.Tk()
root.overrideredirect(True)
root.geometry("+250+250")
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "#ffffff")

# canvas = tk.Canvas(root, bg='white', height=500, width=500)
canvas = tk.Canvas(root, height=500, width=500, bg='white', bd=0, highlightthickness=0, relief='ridge')
canvas.pack()

# canvas.create_line(250, 0, 250, 500, fill='red', width=2)
# canvas.create_line(0, 250, 500, 250, fill='red', width=2)

#Add image to the Canvas Items
img= ImageTk.PhotoImage(Image.open("pigeon.png"))
canvas.create_image(10, 10, anchor=tk.NW, image=img)

root.mainloop()

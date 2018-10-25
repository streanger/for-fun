import os
import sys
import time
import datetime
from tkinter import *
from termcolor import colored
import ctypes
from PIL import ImageTk, Image
import pyperclip

def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

def get_time():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime("%Y-%m-%d %H:%M:%S"))
    return date

class Application_grid(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.geometry('{}x{}'.format(365, 265))
        self.master.resizable(width=False, height=False)
        self.master.title("gui app - grid")
        self.master.iconbitmap("python_ico.ico")
        self.outlineColor = "gray"
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):    
        outlineColor = "gray"
        self.row01 = Frame(self.master, highlightbackground=self.outlineColor, highlightcolor="green", highlightthickness=1, bd=0)
        self.row01.grid(row=0, sticky=W)
        self.row02 = Frame(self.master, highlightbackground=self.outlineColor, highlightcolor="green", highlightthickness=1, bd=0)
        self.row02.grid(row=1, sticky=W)
        self.row03 = Frame(self.master, highlightbackground=self.outlineColor, highlightcolor="green", highlightthickness=1, bd=0)
        self.row03.grid(row=2, sticky=W)
        self.row04 = Frame(self.master, highlightbackground=self.outlineColor, highlightcolor="green", highlightthickness=1, bd=0)
        self.row04.grid(row=3, sticky=W)
        self.row05 = Frame(self.master, highlightbackground=self.outlineColor, highlightcolor="green", highlightthickness=1, bd=0)
        self.row05.grid(row=4, sticky=W)
        self.row06 = Frame(self.master, highlightbackground=self.outlineColor, highlightcolor="green", highlightthickness=1, bd=0)
        self.row06.grid(row=5, sticky=W)
        
        self.winRightUp = Frame(self.master, highlightbackground=self.outlineColor, highlightcolor="green", highlightthickness=1, bd=0)
        self.winRightUp.grid(row=0, column=2, rowspan=3, padx=20, pady=5, sticky="nsew")
        self.winRightDown = Frame(self.master, highlightbackground=self.outlineColor, highlightcolor="green", highlightthickness=1, bd=0)
        self.winRightDown.grid(row=3, column=2, rowspan=3, padx=20, pady=5, sticky="nsew")
        bottomLabel = Frame(self.master)
        bottomLabel.grid(row=6, column=0, columnspan=3, padx=0, pady=5, sticky="nsew")
        
        Label(self.row01, text="just label 1").grid(row=0, column=0, padx=5, pady=5)
        Entry(self.row01).grid(row=0, column=1, padx=5, pady=5)
        Label(self.row02, text="just label 2").grid(row=1, column=0, padx=5, pady=5)
        Entry(self.row02).grid(row=1, column=1, padx=5, pady=5)
        Label(self.row03, text="just label 3").grid(row=2, column=0, padx=5, pady=5)
        Entry(self.row03).grid(row=2, column=1, padx=5, pady=5)
        Label(self.row04, text="just label 4").grid(row=3, column=0, padx=5, pady=5)
        Entry(self.row04).grid(row=3, column=1, padx=5, pady=5)
        Label(self.row05, text="just label 5").grid(row=4, column=0, padx=5, pady=5)
        Entry(self.row05).grid(row=4, column=1, padx=5, pady=5)
        Label(self.row06, text="just label 6").grid(row=5, column=0, padx=5, pady=5)
        Entry(self.row06).grid(row=5, column=1, padx=5, pady=5)
        
        imgPath = "oldman.png"
        img = Image.open(imgPath)
        img.thumbnail((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        logoLabel = Label(self.winRightUp, image=img)
        logoLabel.image = img                           #remember to keep a reference
        logoLabel.grid(row=0, column=2, padx=10, pady=0)
        Button(self.winRightDown, text=" "*8 + "send data" + " "*8, command=lambda: print(">>> data sent at [{}]".format(get_time()))).grid(row=3, column=2, padx=10, pady=5, sticky="nsew")
        Button(self.winRightDown, text="read data", command=lambda: print(">>> data sent at [{}]".format(get_time()))).grid(row=4, column=2, padx=10, pady=5, sticky="nsew")
        Button(self.winRightDown, text="clear stuff", command=lambda: print(">>> data sent at [{}]".format(get_time()))).grid(row=5, column=2, padx=10, pady=5, sticky="nsew")
        Label(bottomLabel, text="someone copyright 2018").grid(row=6, column=0, padx=0, sticky="nsew")
        return True
        
        
class Application_pack(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.geometry('{}x{}'.format(365, 265))
        self.master.resizable(width=False, height=False)
        self.master.wm_title("gui app - pack")
        self.outlineColor = "gray"
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.leftFrame = Frame(self.master)
        self.leftFrame.pack(expand=YES, fill=BOTH, side=LEFT)
        self.leftFrameLeft = Frame(self.leftFrame)
        self.leftFrameLeft.pack(expand=YES, fill=BOTH, side=LEFT)
        self.leftFrameRight = Frame(self.leftFrame)
        self.leftFrameRight.pack(expand=YES, fill=BOTH, side=RIGHT)

        labelEntry01 = Label(self.leftFrameLeft, text="first line label")
        labelEntry01.pack(expand=YES, fill=BOTH, side=TOP)
        entry01 = Entry(self.leftFrameRight)
        entry01.pack(expand=YES, side=TOP)                                      #(expand=YES, fill=BOTH, side=TOP)
        labelEntry02 = Label(self.leftFrameLeft, text="second line label")
        labelEntry02.pack(expand=YES, fill=BOTH, side=TOP)
        entry02 = Entry(self.leftFrameRight)
        entry02.pack(expand=YES, side=TOP)
        labelEntry03 = Label(self.leftFrameLeft, text="third line label")
        labelEntry03.pack(expand=YES, fill=BOTH, side=TOP)
        entry03 = Entry(self.leftFrameRight)
        entry03.pack(expand=YES, side=TOP)         
        labelEntry04 = Label(self.leftFrameLeft, text="fourth line label")
        labelEntry04.pack(expand=YES, fill=BOTH, side=TOP)
        entry04 = Entry(self.leftFrameRight)
        entry04.pack(expand=YES, side=TOP)
        labelEntry05 = Label(self.leftFrameLeft, text="fifth line label")
        labelEntry05.pack(expand=YES, fill=BOTH, side=TOP)
        entry05 = Entry(self.leftFrameRight)
        entry05.pack(expand=YES, side=TOP)
        labelEntry06 = Label(self.leftFrameLeft, text="sixth line label")
        labelEntry06.pack(expand=YES, fill=BOTH, side=TOP)
        entry06 = Entry(self.leftFrameRight)
        entry06.pack(expand=YES, side=TOP)
        
        self.rightFrame = Frame(self.master)
        self.rightFrame.pack(expand=YES, fill=BOTH, side=RIGHT)
        self.rightUpper = Frame(self.rightFrame, highlightbackground=self.outlineColor, highlightcolor="green", highlightthickness=1, bd=0)                    #put image/logo here
        self.rightUpper.pack(expand=YES, fill=BOTH, side=TOP)
        self.rightLower = Frame(self.rightFrame)
        self.rightLower.pack(expand=YES, fill=BOTH, side=BOTTOM)
        
        imgPath = "oldman.png"
        imgPath = "favicon.ico"
        img = Image.open(imgPath)
        img.thumbnail((150, 150), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        logoLabel = Label(self.rightUpper, image=img)
        logoLabel.image = img                           #remember to keep a reference
        logoLabel.pack(expand=YES, fill=BOTH)
        
        rightLowerButton01 = Button(self.rightLower, text='SEND', command=lambda: print(">>> data sent at [{}]".format(get_time())))
        rightLowerButton01.pack(expand=YES, fill=BOTH)
        rightLowerButton02 = Button(self.rightLower, text='RECEIVE', command=lambda: print(">>> data received at [{}]: {}".format(get_time(), entry01.get())))
        rightLowerButton02.pack(expand=YES, fill=BOTH)
        rightLowerButton03 = Button(self.rightLower, text='CLEAR', command=(lambda: print(">>> data cleared at [{}]".format(get_time())) \
                                                                                    or entry01.delete(0, 'end') \
                                                                                    or entry02.delete(0, 'end') \
                                                                                    or entry03.delete(0, 'end') \
                                                                                    or entry04.delete(0, 'end') \
                                                                                    or entry05.delete(0, 'end') \
                                                                                    or entry06.delete(0, 'end')))
        rightLowerButton03.pack(expand=YES, fill=BOTH)
        rightLowerButton04 = Button(self.rightLower, text='CLIPBOARD', command=lambda: print(">>> copied to clipboard at [{}]".format(get_time())) \
                                                                                    or pyperclip.copy("\n".join([entry01.get(), entry02.get()])))       #put here all labels and entries: label01: "entry text"...
        rightLowerButton04.pack(expand=YES, fill=BOTH)        
        rightLowerButton05 = Button(self.rightLower, text='QUIT', command=(lambda: print(">>> quit from app at [{}]".format(get_time())) or self.master.destroy()))
        rightLowerButton05.pack(expand=YES, fill=BOTH)
        return True
        
    def local_decorator(f):
        def func(*args, **kwargs):
            before = time.time()
            val = f(**args, **kwargs)
            total = round(time.time() - before, 4)
            print("executed after {}[s]".format(total))
            return val
        return func
    
    def send_data():
        return True
          
    def receive_data():
        return True

        
if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)         #for hiding window
    PATH = script_path()
    root = Tk()
    if True:
        app = Application_pack(master=root)             #app example with using pack
    else:
        app = Application_grid(master=root)             #app example with using grid
    app.mainloop()
    
    
'''
todo:
-gui application with 6 'edits', two buttons (send, receive), and one logo (png image)
-set fixed size
-server client communication
'''



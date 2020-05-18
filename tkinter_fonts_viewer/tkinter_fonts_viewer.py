from tkinter import Tk, font
from functools import partial
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import tkinter.font as TkFont
import tkinter.ttk



class Application_pack(Frame):
    '''
    for now this works for fixed values of macs and names
    
    unicode arrows:
        https://en.wikipedia.org/wiki/Arrows_(Unicode_block)
        
    '''
    def __init__(self, master):
        # *********** INIT, HIDE, CLOSING ***********
        # self.hide_console()
        super().__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        
        # *********** APP GUI, CONST, VARIABLES ***********
        # raised, sunken, flat, ridge, solid, groove     
        self.RELIEF_TYPE = 'groove'
        self.ROW_RELIEF = 'raised'
        self.INFO_RELIEF = 'flat'
        # self.MONO_FONT_NAME = TkFont.Font(family="Lucida console", size=50, weight="normal")
        self.MONO_FONT_NAME = TkFont.Font(family="Lucida console", size=40, weight="normal")
        self.MONO_FONT_INFO = TkFont.Font(family="Lucida console", size=9, weight="normal")
        self.MONO_BUTTON = TkFont.Font(family="Lucida console", size=30, weight="normal")
        self.MONO_FONT_INFO_UPPER = TkFont.Font(family="Lucida console", size=12, weight="normal")
        self.CENTER_CHAR = ' '      # 'x'
        
        self.padx = 0
        self.pady = 1
        self.master.geometry('{}x{}+333+50'.format(800, 500))
        self.master.resizable(width=False, height=True)
        self.master.wm_title("gui_app")
        self.pack()
        
        
        # *********** ALL FONTS ***********
        self.ALL_FONTS = font.families()
        self.NUMBER_OF_FONTS = len(self.ALL_FONTS)
        self.INDEX = 0
        
        
        # *********** CREATE WIDGETS ***********
        self.create_widgets()
        
        
    def on_closing(self):
        '''
        handle closing
        https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
        '''
        
        if messagebox.askokcancel('Quit', 'Do you want to quit?'):
            # destroy main app
            self.master.destroy()
            
        return None
        
        
    def index_down(self):
        self.INDEX += 1         # need to be swapped :)
        if self.INDEX > max(self.NUMBER_OF_FONTS-1, 1):
            self.INDEX = 0
        # print(self.INDEX)
        self.config_widgets()
        return None
        
        
    def index_up(self):
        self.INDEX -= 1         # need to be swapped :)
        if self.INDEX < 0:
            self.INDEX = max(self.NUMBER_OF_FONTS-1, 1)
        # print(self.INDEX)
        self.config_widgets()
        return None
        
        
    def config_widgets(self):
        center_val = 20
        
        # ******** current index entry ********
        self.top_info_right_entry.delete(0, 'end')
        self.top_info_right_entry.insert(0, str(self.INDEX).center(center_val))
        
        
        first_font = self.ALL_FONTS[(self.INDEX-2)%self.NUMBER_OF_FONTS]
        second_font = self.ALL_FONTS[(self.INDEX-1)%self.NUMBER_OF_FONTS]
        third_font = self.ALL_FONTS[(self.INDEX)%self.NUMBER_OF_FONTS]
        fourth_font = self.ALL_FONTS[(self.INDEX+1)%self.NUMBER_OF_FONTS]
        fifth_font = self.ALL_FONTS[(self.INDEX+2)%self.NUMBER_OF_FONTS]
        
        
        # REMEBER TO DELETE ENTRIES
        # self.first_text.config(text=first_font)
        self.first_text.delete(0, 'end')
        self.first_text.insert(0, first_font.center(center_val))
        
        self.second_text.delete(0, 'end')
        self.second_text.insert(0, second_font.center(center_val))
        
        self.third_text.delete(0, 'end')
        self.third_text.insert(0, third_font.center(center_val))
        
        self.fourth_text.delete(0, 'end')
        self.fourth_text.insert(0, fourth_font.center(center_val))
        
        self.fifth_text.delete(0, 'end')
        self.fifth_text.insert(0, fifth_font.center(center_val))
        
        
        
        center_text = third_font
        if len(center_text.split()) > 2:
            center_text = '\n'.join(center_text.split())
            
        self.FONT = TkFont.Font(family=third_font, size=50, weight="normal")
        self.main_label.config(font=self.FONT, text=center_text)
        return None
        
        
    def entry_callback(self, event):
        '''entries callback'''
        
        # ******** perform value ********
        value = self.top_info_right_entry.get()
        try:
            self.INDEX = (int(value.strip()))%self.NUMBER_OF_FONTS
        except ValueError:
            pass
            
        # ******** update entry ********
        self.top_info_right_entry.delete(0, 'end')
        self.top_info_right_entry.insert(0, str(self.INDEX).center(20))
        
        
        # ******** update widgets ********
        self.config_widgets()
        return None
        
        
    def key_event(self, event):
        '''key events callback'''
        # print('event: {}'.format(event))
        code = event.keycode
        
        if code == 38:
            # arrow up - 38
            self.index_up()
        elif code == 40:
            # arrow down - 40
            self.index_down()
        return None
        
        
    def create_widgets(self):
        '''create widgets from dict object'''
        
        # ********* bind key event for master widget *********
        self.master.bind('<Key>', self.key_event)
        
        
        self.top_label = Label(self.master, font=self.MONO_FONT_INFO_UPPER, text="TKINTER FONTS VIEWER")
        self.top_label.pack(expand=NO, fill=X, side=TOP)
        
        
        self.main_frame = Frame(self.master)
        self.main_frame.pack(expand=YES, fill=BOTH, side=BOTTOM)
        
        self.left_buttons = Frame(self.main_frame)
        self.left_buttons.pack(expand=NO, fill=BOTH, side=LEFT)
        
        
        # ********* up - down buttons *********
        self.button_up = Button(self.left_buttons, font=self.MONO_BUTTON, text='↑', command=self.index_up)
        self.button_up.pack(expand=YES, fill=BOTH, side=TOP)
        
        self.button_down = Button(self.left_buttons, font=self.MONO_BUTTON, text='↓', command=self.index_down)
        self.button_down.pack(expand=YES, fill=BOTH, side=BOTTOM)
        
        
        # ********* LEFT FRAME *********
        self.left_frame = Frame(self.main_frame)
        self.left_frame.pack(expand=NO, fill=BOTH, side=LEFT)
        
        
        
        center_val = 20
        self.first_sv = StringVar()
        self.first_text = Entry(self.left_frame, font=self.MONO_FONT_INFO, textvariable=self.first_sv)
        self.first_text.insert(0, self.ALL_FONTS[self.INDEX-2].center(center_val))
        self.first_text.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        self.second_sv = StringVar()
        self.second_text = Entry(self.left_frame, font=self.MONO_FONT_INFO, textvariable=self.second_sv)
        self.second_text.insert(0, self.ALL_FONTS[self.INDEX-1].center(center_val))
        self.second_text.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        self.third_sv = StringVar()
        self.third_text = Entry(self.left_frame, font=self.MONO_FONT_INFO, textvariable=self.third_sv)
        self.third_text.insert(0, self.ALL_FONTS[self.INDEX].center(center_val))
        self.third_text.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        self.fourth_sv = StringVar()
        self.fourth_text = Entry(self.left_frame, font=self.MONO_FONT_INFO, textvariable=self.fourth_sv)
        self.fourth_text.insert(0, self.ALL_FONTS[self.INDEX+1].center(center_val))
        self.fourth_text.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        self.fifth_sv = StringVar()
        self.fifth_text = Entry(self.left_frame, font=self.MONO_FONT_INFO, textvariable=self.fifth_sv)
        self.fifth_text.insert(0, self.ALL_FONTS[self.INDEX+2].center(center_val))
        self.fifth_text.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        
        # ********* RIGHT FRAME *********
        self.right_frame = Frame(self.main_frame)
        self.right_frame.pack(expand=YES, fill=BOTH, side=RIGHT)
        
        
        
        # righ top info
        self.top_info = Frame(self.right_frame)
        self.top_info.pack(expand=NO, fill=X, side=TOP)
        self.top_info_left = Frame(self.top_info, relief=self.RELIEF_TYPE)
        self.top_info_left.pack(expand=YES, fill=X, side=LEFT)
        self.top_info_left_label = Label(self.top_info_left, relief=self.RELIEF_TYPE, font=self.MONO_FONT_INFO_UPPER, text='TOTAL FONTS: {}'.format(self.NUMBER_OF_FONTS))
        self.top_info_left_label.pack(expand=YES, fill=X, side=LEFT)
        self.top_info_right = Frame(self.top_info, relief=self.RELIEF_TYPE)
        self.top_info_right.pack(expand=YES, fill=X, side=RIGHT)
        self.top_info_right_label = Label(self.top_info_right, relief=self.RELIEF_TYPE, font=self.MONO_FONT_INFO_UPPER, text='CURRENT FONT:')
        self.top_info_right_label.pack(expand=YES, fill=X, side=LEFT)
        self.top_info_right_entry_sv = StringVar()
        self.top_info_right_entry = Entry(self.top_info_right, font=self.MONO_FONT_INFO_UPPER, textvariable=self.top_info_right_entry_sv)
        self.top_info_right_entry.insert(0, str(self.INDEX).center(center_val))
        self.top_info_right_entry.bind('<Return>', self.entry_callback)
        self.top_info_right_entry.pack(expand=NO, fill=Y, side=RIGHT)
        
        
        
        self.main_label = Label(self.right_frame, relief=self.RELIEF_TYPE, font=self.MONO_FONT_NAME, text="MAIN LABEL")
        self.main_label.pack(expand=YES, fill=BOTH, side=BOTTOM)
        
        
        return True
        
        
        
        
if __name__ == "__main__":
    # script_path()
    app = Application_pack(master=Tk())             #app example with using pack
    app.mainloop()
    
    
from tkinter import Tk, font
# root = Tk()
# font.families()



from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import tkinter.font as TkFont
import tkinter.ttk

    
class Application_pack(Frame):
    '''
    for now this works for fixed values of macs and names
    '''
    def __init__(self, master):
        # *********** INIT, HIDE, CLOSING ***********
        # self.hide_console()
        super().__init__(master)
        # self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        
        
        # *********** APP GUI, CONST, VARIABLES ***********
        self.RELIEF_TYPE = 'raised'                 # raised, sunken, flat, ridge, solid, groove
        self.ROW_RELIEF = 'raised'
        self.INFO_RELIEF = 'flat'
        self.MONO_FONT_NAME = TkFont.Font(family="Lucida console", size=50, weight="normal")
        self.MONO_FONT_INFO = TkFont.Font(family="Lucida console", size=9, weight="normal")
        # self.MONO_FONT_INFO = TkFont.Font(family="Courier", size=9, weight="normal")    # for debug
        self.CENTER_CHAR = ' '      # 'x'
        
        self.padx = 0
        self.pady = 1
        # init_number_of_clients = len(list(self.KNOWN_DEVICES.keys()))
        # init_height = (init_number_of_clients + 1)*61
        # https://yagisanatode.com/2018/02/23/how-do-i-change-the-size-and-position-of-the-main-window-in-tkinter-and-python-3/
        self.master.geometry('{}x{}+333+50'.format(900, 500))
        self.master.resizable(width=False, height=True)
        self.master.wm_title("gui_app")
        self.pack()
        
        
        # all fonts
        self.ALL_FONTS = font.families()
        self.NUMBER_OF_FONTS = len(self.ALL_FONTS)
        print(self.NUMBER_OF_FONTS)
        self.INDEX = 10
        
        
        
        # *********** CREATE WIDGETS ***********
        # self.WIDGETS_LAST_KEY = 0
        # devices_list = self.dict_to_widgets_list(self.KNOWN_DEVICES)
        self.create_widgets()
        
        
        
        
        
    def index_up(self):
        self.INDEX += 1
        if self.INDEX > 199:
            self.INDEX = 0
        # print(self.INDEX)
        self.config_widgets()
        return None
        
        
    def index_down(self):
        self.INDEX -= 1
        if self.INDEX < 0:
            self.INDEX = 199
        # print(self.INDEX)
        self.config_widgets()
        return None
        
        
    def config_widgets(self):
        first_font = self.ALL_FONTS[(self.INDEX-2)%200]
        second_font = self.ALL_FONTS[(self.INDEX-1)%200]
        third_font = self.ALL_FONTS[(self.INDEX)%200]
        fourth_font = self.ALL_FONTS[(self.INDEX+1)%200]
        fifth_font = self.ALL_FONTS[(self.INDEX+2)%200]
        
        self.FONT = TkFont.Font(family=third_font, size=50, weight="normal")
        self.main_label.config(font=self.FONT, text=third_font)
        return None
        
        
    def create_widgets(self):
        '''create widgets from dict object'''
        self.top_label = Label(self.master, text="FONTS VIEWER")
        self.top_label.pack(expand=NO, fill=X, side=TOP)
        self.main_frame = Frame(self.master)
        self.main_frame.pack(expand=YES, fill=BOTH, side=BOTTOM)
        
        self.left_buttons = Frame(self.main_frame)
        self.left_buttons.pack(expand=NO, fill=BOTH, side=LEFT)
        
        # Button for some action
        self.button_up = Button(self.left_buttons, font=self.MONO_FONT_INFO, text='/\\'.center(8, self.CENTER_CHAR), command=self.index_up)
        self.button_up.pack(expand=YES, fill=BOTH, side=TOP)
        
        self.button_down = Button(self.left_buttons, font=self.MONO_FONT_INFO, text='\\/'.center(8, self.CENTER_CHAR), command=self.index_down)
        self.button_down.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        self.left_frame = Frame(self.main_frame)
        self.left_frame.pack(expand=NO, fill=BOTH, side=LEFT)
        
        
        
        center_val = 20
        self.first_sv = StringVar()
        self.first_text = Entry(self.left_frame, font=self.MONO_FONT_INFO, textvariable=self.first_sv)
        self.first_text.insert(0, self.ALL_FONTS[self.INDEX-2].center(center_val))
        # self.first_text.bind('<Return>', partial(self.entry_callback, key))
        self.first_text.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        self.second_sv = StringVar()
        self.second_text = Entry(self.left_frame, font=self.MONO_FONT_INFO, textvariable=self.second_sv)
        self.second_text.insert(0, self.ALL_FONTS[self.INDEX-1].center(center_val))
        # self.second_text.bind('<Return>', partial(self.entry_callback, key))
        self.second_text.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        self.third_sv = StringVar()
        self.third_text = Entry(self.left_frame, font=self.MONO_FONT_INFO, textvariable=self.third_sv)
        self.third_text.insert(0, self.ALL_FONTS[self.INDEX].center(center_val))
        # self.third_text.bind('<Return>', partial(self.entry_callback, key))
        self.third_text.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        self.fourth_sv = StringVar()
        self.fourth_text = Entry(self.left_frame, font=self.MONO_FONT_INFO, textvariable=self.fourth_sv)
        self.fourth_text.insert(0, self.ALL_FONTS[self.INDEX+1].center(center_val))
        # self.fourth_text.bind('<Return>', partial(self.entry_callback, key))
        self.fourth_text.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        self.fifth_sv = StringVar()
        self.fifth_text = Entry(self.left_frame, font=self.MONO_FONT_INFO, textvariable=self.fifth_sv)
        self.fifth_text.insert(0, self.ALL_FONTS[self.INDEX+2].center(center_val))
        # self.fifth_text.bind('<Return>', partial(self.entry_callback, key))
        self.fifth_text.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        # self.right_frame = Frame(self.main_frame)
        # self.right_frame.pack(expand=YES, fill=BOTH, side=RIGHT)
        self.main_label = Label(self.main_frame, relief=self.RELIEF_TYPE, font=self.MONO_FONT_NAME, text="MAIN LABEL")
        self.main_label.pack(expand=YES, fill=BOTH, side=RIGHT)
            
            
        return True
        
        
        
        
if __name__ == "__main__":
    # script_path()
    app = Application_pack(master=Tk())             #app example with using pack
    app.mainloop()
    
    
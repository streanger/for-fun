import sys
import os
import time
import ctypes
import tkinter.font as TkFont
from tkinter import *
from tkinter import messagebox
from threading import Thread



class FontsMonoCheck(Frame):
    '''class for testing fonts mono status
    https://stackoverflow.com/questions/4481880/minimizing-a-tk-window
    '''
    def __init__(self, master):
        super().__init__(master)
        self.master.geometry('30x30')
        self.master.iconify()      # minimized window
        
        self.test_label = Label(self.master)
        self.test_label.pack(expand=NO, fill=Y, side=BOTTOM)
        
        fonts = font.families()
        self.fonts_mono_status = {}
        self.test_thread = Thread(target=self.check_fonts_thread, args=(fonts,))
        self.test_thread.start()
        
        
    def cleanup(self):
        '''join thread and destroy window'''
        self.test_thread.join()
        self.master.destroy()
        
        
    def check_fonts_thread(self, fonts):
        '''check fonts in thread'''
        default_color = self.master.cget('bg')
        for key, font in enumerate(fonts):
            # set proper font
            self.test_font = TkFont.Font(family=font, size=11)
            self.test_label.config(font=self.test_font, fg=default_color)  #invisible color
            
            # set '.' as text
            self.test_label.config(text=".")
            self.master.update()        # this is needed for true width value
            dot_width = self.test_label.winfo_width()
            
            # set 'm' as text
            self.test_label.config(text='m')
            self.master.update()        # this is needed for true width value
            m_width = self.test_label.winfo_width()
            
            # show & compare sizes
            status = bool(m_width == dot_width)
            # out[font] = status
            self.fonts_mono_status[font] = status
            
        self.test_label.pack_forget()
        self.master.update()
        
        self.master.quit()
        self.master.update()
        return None
        
        
        
class TkinterFontsViewer(Frame):
    '''
    info:
        https://en.wikipedia.org/wiki/Arrows_(Unicode_block)
        https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
        https://stackoverflow.com/questions/16115378/tkinter-example-code-for-multiple-windows-why-wont-buttons-load-correctly
        https://stackoverflow.com/questions/1892339/how-to-make-a-tkinter-window-jump-to-the-front
    '''
    
    def __init__(self, master):
        # *********** INIT, HIDE, CLOSING ***********
        # self.hide_console()
        super().__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.geometry('{}x{}+333+50'.format(800, 500))
        self.master.resizable(width=True, height=True)
        self.master.wm_title("gui_app")
        self.pack()
        
        
        # *********** APP GUI, CONST, VARIABLES ***********
        # raised, sunken, flat, ridge, solid, groove     
        self.RELIEF_TYPE = 'groove'
        self.MONO_FONT_NAME = TkFont.Font(family="Lucida console", size=40, weight="normal")
        self.MONO_FONT_INFO = TkFont.Font(family="Lucida console", size=10, weight="normal")
        self.MONO_BUTTON = TkFont.Font(family="Lucida console", size=25, weight="normal")
        self.MONO_FONT_INFO_UPPER = TkFont.Font(family="Lucida console", size=12, weight="normal")
        
        
        # *********** FONTS MONO STATUS ***********
        self.ALL_FONTS = font.families()
        self.FONTS_MONOSPACE_STATUS = self.check_if_mono(self.ALL_FONTS)
        self.NUMBER_OF_FONTS = len(self.ALL_FONTS)
        self.INDEX = 0
        
        
        # *********** CREATE WIDGETS ***********
        self.default_color = self.master.cget('bg')
        self.BG_COLOR_MONO = '#ADD8E6'
        self.BG_COLOR_NORMAL = self.default_color
        self.create_widgets()
        
        
        # *********** LIFT, GET FOCUS ***********
        self.master.lift()                          # move window to the top
        self.master.focus_force()
        # self.master.attributes("-topmost", True)    # always on top
        
        
    def hide_console(self):
        '''hide console window'''
        if os.name == 'nt':
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        return None
        
        
    def check_if_mono(self, fonts):
        '''check fonts mono status with new window
        https://stackoverflow.com/questions/16115378/tkinter-example-code-for-multiple-windows-why-wont-buttons-load-correctly
        '''
        self.newWindow = Toplevel(self.master)
        test_app = FontsMonoCheck(self.newWindow)
        test_app.mainloop()
        test_app.cleanup()
        return test_app.fonts_mono_status
        
        
    def on_closing(self):
        '''handle closing; https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter'''
        if messagebox.askokcancel('Quit', 'Do you want to quit?'):
            self.master.destroy()       # destroy main app
            self.master.quit()
        return None
        
        
    def index_down(self):
        self.INDEX -= 1
        if self.INDEX < 0:
            self.INDEX = max(self.NUMBER_OF_FONTS-1, 1)
            
        self.config_widgets()
        return None
        
        
    def index_up(self):
        self.INDEX += 1
        if self.INDEX > max(self.NUMBER_OF_FONTS-1, 1):
            self.INDEX = 0
            
        self.config_widgets()
        return None
        
        
    def bg_color(self, status):
        '''get bg color depend on status'''
        if status:
            return self.BG_COLOR_MONO
        return self.BG_COLOR_NORMAL
        
        
    def mono_status_text(self, status):
        '''get mono text depend on status'''
        if status:
            return ' MONO '
        return 'NORMAL'
        
        
    def config_widgets(self):
        center_val = 20
        
        # ******** current index entry ********
        self.top_info_right_entry.delete(0, 'end')
        self.top_info_right_entry.insert(0, str(self.INDEX).center(center_val))
        
        
        first_index = (self.INDEX+2)%self.NUMBER_OF_FONTS
        second_index = (self.INDEX+1)%self.NUMBER_OF_FONTS
        third_index = (self.INDEX)%self.NUMBER_OF_FONTS
        fourth_index = (self.INDEX-1)%self.NUMBER_OF_FONTS
        fifth_index = (self.INDEX-2)%self.NUMBER_OF_FONTS
        
        
        first_font = self.ALL_FONTS[first_index]
        second_font = self.ALL_FONTS[second_index]
        third_font = self.ALL_FONTS[third_index]
        fourth_font = self.ALL_FONTS[fourth_index]
        fifth_font = self.ALL_FONTS[fifth_index]
        
        
        # ******** indexes labels ********
        first_status = self.FONTS_MONOSPACE_STATUS[first_font]
        first_index_text = '{}\n{}'.format(first_index, self.mono_status_text(first_status))
        self.first_index.config(text=first_index_text, bg=self.bg_color(first_status))
        
        
        second_status = self.FONTS_MONOSPACE_STATUS[second_font]
        second_index_text = '{}\n{}'.format(second_index, self.mono_status_text(second_status))
        self.second_index.config(text=second_index_text, bg=self.bg_color(second_status))
        
        
        third_status = self.FONTS_MONOSPACE_STATUS[third_font]
        third_index_text = '{}\n{}'.format(third_index, self.mono_status_text(third_status))
        self.third_index.config(text=third_index_text, bg=self.bg_color(third_status))
        
        
        fourth_status = self.FONTS_MONOSPACE_STATUS[fourth_font]
        fourth_index_text = '{}\n{}'.format(fourth_index, self.mono_status_text(fourth_status))
        self.fourth_index.config(text=fourth_index_text, bg=self.bg_color(fourth_status))
        
        
        fifth_status = self.FONTS_MONOSPACE_STATUS[fifth_font]
        fifth_index_text = '{}\n{}'.format(fifth_index, self.mono_status_text(fifth_status))
        self.fifth_index.config(text=fifth_index_text, bg=self.bg_color(fifth_status))
        
        
        
        # REMEBER TO DELETE ENTRIES
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
        elif len(center_text.split()) == 2 and len(center_text) > 12:
            center_text = '\n'.join(center_text.split())
        else:
            if len(center_text) > 14:
                center_text = '\n'.join(center_text.split('_'))
                
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
        
        
        
        # ********* INDEXES & MONO INFO *********
        self.left_indexes = Frame(self.main_frame)
        self.left_indexes.pack(expand=NO, fill=BOTH, side=LEFT)
        
        
        # SETUP
        first_index = (self.INDEX+2)%self.NUMBER_OF_FONTS
        second_index = (self.INDEX+1)%self.NUMBER_OF_FONTS
        third_index = (self.INDEX)%self.NUMBER_OF_FONTS
        fourth_index = (self.INDEX-1)%self.NUMBER_OF_FONTS
        fifth_index = (self.INDEX-2)%self.NUMBER_OF_FONTS
        
        
        first_font = self.ALL_FONTS[first_index]
        second_font = self.ALL_FONTS[second_index]
        third_font = self.ALL_FONTS[third_index]
        fourth_font = self.ALL_FONTS[fourth_index]
        fifth_font = self.ALL_FONTS[fifth_index]
        
        
        first_status = self.FONTS_MONOSPACE_STATUS[first_font]
        second_status = self.FONTS_MONOSPACE_STATUS[second_font]
        third_status = self.FONTS_MONOSPACE_STATUS[third_font]
        fourth_status = self.FONTS_MONOSPACE_STATUS[fourth_font]
        fifth_status = self.FONTS_MONOSPACE_STATUS[fifth_font]
        
        
        first_index_text = '{}\n{}'.format(first_index, self.mono_status_text(first_status))
        second_index_text = '{}\n{}'.format(second_index, self.mono_status_text(second_status))
        third_index_text = '{}\n{}'.format(third_index, self.mono_status_text(third_status))
        fourth_index_text = '{}\n{}'.format(fourth_index, self.mono_status_text(fourth_status))
        fifth_index_text = '{}\n{}'.format(fifth_index, self.mono_status_text(fifth_status))
        
        
        # TEXT DATA NEED TO BE SET AUTOMATICALLY HERE
        self.first_index = Label(self.left_indexes, relief=self.RELIEF_TYPE, font=self.MONO_FONT_INFO, text=first_index_text, bg=self.bg_color(first_status))
        self.first_index.pack(expand=YES, fill=BOTH, side=TOP)
        self.second_index = Label(self.left_indexes, relief=self.RELIEF_TYPE, font=self.MONO_FONT_INFO, text=second_index_text, bg=self.bg_color(second_status))
        self.second_index.pack(expand=YES, fill=BOTH, side=TOP)
        self.third_index = Label(self.left_indexes, relief=self.RELIEF_TYPE, font=self.MONO_FONT_INFO, text=third_index_text, bg=self.bg_color(third_status))
        self.third_index.pack(expand=YES, fill=BOTH, side=TOP)
        self.fourth_index = Label(self.left_indexes, relief=self.RELIEF_TYPE, font=self.MONO_FONT_INFO, text=fourth_index_text, bg=self.bg_color(fourth_status))
        self.fourth_index.pack(expand=YES, fill=BOTH, side=TOP)
        self.fifth_index = Label(self.left_indexes, relief=self.RELIEF_TYPE, font=self.MONO_FONT_INFO, text=fifth_index_text, bg=self.bg_color(fifth_status))
        self.fifth_index.pack(expand=YES, fill=BOTH, side=TOP)
        
        
        
        # ********* LEFT FRAME *********
        self.left_frame = Frame(self.main_frame)
        self.left_frame.pack(expand=NO, fill=BOTH, side=LEFT)        
        
        # ********* ENTRIES *********
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
    app = TkinterFontsViewer(master=Tk())
    app.mainloop()

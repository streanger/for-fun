import sys
import os
import ctypes
import time
import ast
import win32gui
from ctypes import windll
from termcolor import colored
from PIL import Image, ImageGrab
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter, Terminal256Formatter


def script_path():
    """set current path, to script path"""
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def highlight_code(code, style):
    """
    https://pygments.org/docs/styles/
    styles:
        pygments.styles.get_all_styles()
        ['default', 'emacs', 'friendly', 'friendly_grayscale', 'colorful', 'autumn', 'murphy', 'manni', 'material', 'monokai', 'perldoc', 'pastie', 'borland', 'trac', 'native', 'fruity', 'bw', 'vim', 'vs', 'tango', 'rrt', 'xcode', 'igor', 'paraiso-light', 'paraiso-dark', 'lovelace', 'algol', 'algol_nu', 'arduino', 'rainbow_dash', 'abap', 'solarized-dark', 'solarized-light', 'sas', 'stata', 'stata-light', 'stata-dark', 'inkpot', 'zenburn', 'gruvbox-dark', 'gruvbox-light', 'dracula', 'one-dark', 'lilypond']
        
    looks fine:
        monokai
    """
    highlighted = highlight(code, PythonLexer(), Terminal256Formatter(style=style))
    return highlighted
    
    
def get_image(window_title):
    """
    https://stackoverflow.com/questions/40869982/dpi-scaling-level-affecting-win32gui-getwindowrect-in-python
    https://stackoverflow.com/questions/9983263/how-to-crop-an-image-using-pil
    
    for later to make it better:
        https://stackoverflow.com/questions/18034975/how-do-i-find-position-of-a-win32-control-window-relative-to-its-parent-window
        https://docs.microsoft.com/pl-pl/windows/win32/api/winuser/nf-winuser-mapwindowpoints?redirectedfrom=MSDN
        use GetWindowRect & MapWindowPoints. To debug:
            bbox = user32.MapWindowPoints(hwnd, win32gui.GetParent(hwnd), bbox, 2)
    """
    # Make program aware of DPI scaling
    user32 = windll.user32
    user32.SetProcessDPIAware()
    
    toplist = []
    winlist = []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        
    win32gui.EnumWindows(enum_cb, toplist)
    windows = [(hwnd, title) for hwnd, title in winlist if window_title in title.lower()]
    windows = windows[0]
    hwnd = windows[0]
    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    return img
    
    
def concat_images(images, horizontal=True):
    """concat images horizontally using PIL"""
    widths, heights = zip(*(i.size for i in crop_images))
    if horizontal:
        total_width = sum(widths)
        max_height = max(heights)
        new_im = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for img in images:
            new_im.paste(img, (x_offset,0))
            x_offset += img.size[0]
    else:
        total_height = sum(heights)
        max_width = max(widths)
        new_im = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for img in images:
            new_im.paste(img, (0, y_offset))
            y_offset += img.size[1]
    return new_im
    
    
class tagPOINT(ctypes.Structure):
    """creates a struct (for later, for debug)"""
    _fields_ = [
        ('x', ctypes.POINTER(ctypes.c_double)),
        ('y', ctypes.POINTER(ctypes.c_double)),
        ]
        
        
example = """
def add(a, b):
    '''the docstrings'''
    some = [1,2,3,\
    \
    \
    \
    \
    \
    \
    \
    \
    \
    \
    \
    43,4,(1023013, 3232)]
    things = {
        1:2,
        3:4,
        5:6,
        }
    s = 'This is sentence'
    here = int(str(int(str(42))))
    return a+b
"""


if __name__ == "__main__":
    # ********** DEBUG **********
    # point = tagPOINT()
    # sys.exit()
    
    script_path()
    os.system('color')
    time.sleep(0.1)
    input()
    
    styles = ['default', 'emacs', 'friendly', 'friendly_grayscale', 'colorful', 'autumn', 'murphy', 'manni', 'material', 'monokai', 'perldoc', 'pastie', 'borland', 'trac', 'native', 'fruity', 'bw', 'vim', 'vs', 'tango', 'rrt', 'xcode', 'igor', 'paraiso-light', 'paraiso-dark', 'lovelace', 'algol', 'algol_nu', 'arduino', 'rainbow_dash', 'abap', 'solarized-dark', 'solarized-light', 'sas', 'stata', 'stata-light', 'stata-dark', 'inkpot', 'zenburn', 'gruvbox-dark', 'gruvbox-light', 'dracula', 'one-dark', 'lilypond']
    print()
    save_each = True
    crop_images = []
    for index, style in enumerate(styles):
        if not (index+1) % 6:
            print('\n')
            time.sleep(0.1)
            img = get_image('python.exe')
            w, h = img.size
            crop = img.crop((9, 38, 450, h-9-75))
            # crop.show()
            crop_images.append(crop)
            if save_each:
                crop.save('img{}.png'.format(index))
        try:
            print(colored(style, 'white', None, ['reverse']) + '|')
            tree = ast.parse(example)
            func_content = ast.unparse(tree)
            highlighted = highlight_code(func_content, style)
            print(highlighted)
        except SyntaxError:
            pass
            
        finally:
            pass
            
    # ********** combined image **********
    new_horizontal = concat_images(crop_images, horizontal=True)
    new_vertical = concat_images(crop_images, horizontal=False)
    new_horizontal.save('horizontal.png')
    new_vertical.save('vertical.png')
    
"""
useful:
    https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
    
"""

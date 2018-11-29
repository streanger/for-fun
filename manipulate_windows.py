import ctypes
import win32gui
import win32con

'''
based on:
    https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-all-window-titles/
    
info:
    http://docs.activestate.com/activepython/3.3/pywin32/win32gui.html
 
'''

def get_windows():
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    
    titles = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True
        
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles
    
def minimize_windows(titles):
    for window in titles:
        winHandle = win32gui.FindWindow(None, window)
        win32gui.ShowWindow(winHandle, win32con.SW_MINIMIZE)
    return True
    
def maximize_windows(titles):
    for window in titles:
        winHandle = win32gui.FindWindow(None, window)
        win32gui.ShowWindow(winHandle, win32con.SW_MAXIMIZE)
    return True
    
    
if __name__ == "__main__":
    titles = get_windows()
    print(titles)
    minimize_windows(titles)
    maximize_windows(titles)

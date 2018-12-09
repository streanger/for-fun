'''
-use for enemies :)
-pyinstaller proper command:
    pyinstaller -F --noconsole clear_paste.py
'''
import time
import pyperclip
    
def clear_clipboard():
    ''' clear clipboard continously '''
    while True:
        content = pyperclip.paste()
        if content:
            pyperclip.copy("")
        time.sleep(0.01)
    return True
    
    
if __name__ == "__main__":
    clear_clipboard()

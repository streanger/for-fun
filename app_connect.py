'''
connect with running app, and use it with clicks
'''
import os
import sys
import time
import pyautogui
import re
import pywinauto
from pywinauto.application import Application
import subprocess
import warnings

def script_path():
    ''' set current path to script_path '''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
def get_process_id(pattern):
    ''' return list of processes with using "tasklist" command '''
    tasks = subprocess.check_output(["tasklist"])
    tasks = tasks.decode("utf-8", "ignore")
    processes = []
    for line in tasks.split("\n")[3:]:
        for key, element in enumerate(line.split()):
            if element.isdigit():
                processes.append(["_".join(line.split()[:key]), line.split()[key]])     #when join use " " or "_"
                break
    processList = processes
    appId = [id for process, id in processList if pattern == process]                #get first app id (may be more than one)
    if appId:
        appId = int(appId[0])
    else:
        appId = False
    return appId
    
class app_handler():
    ''' handler for connected app with using pywinauto Application '''
    def __init__(self, app):
        self.app = app
        self.clickTimeout = 0.25
        
    def execute_decorator(func):
        def f(*args, **kwargs):
            # input("next step: {}...\t".format(func.__name__))
            before = time.time()
            val = func(*args, **kwargs)
            total = round((time.time() - before), 4)
            print("--> <{}> finished in {}[s]".format(func.__name__, total))
            time.sleep(0.25)
            return val
        return f
        
    @execute_decorator
    def all_actions(self):
        self.focus()                    # maximize & focus main window
        self.minimize_app()
        self.focus()
        return True
    
    @execute_decorator
    def focus(self):
        self.app.top_window().maximize()
        self.app.top_window().set_focus()
        return True
        
    @execute_decorator    
    def close_top(self):
        time.sleep(self.clickTimeout)
        self.app.top_window().close()
        return True

    @execute_decorator 
    def minimize_app(self):
        time.sleep(self.clickTimeout)
        self.app.top_window().minimize()
        return True
        
    def top_name(self):
        return self.app.top_window().texts()
        
    def close_app(self):
        ''' close application '''
        self.focus()
        time.sleep(self.clickTimeout)
        self.app.top_window().close()
        return True
	
    def mouse_coordinates(self):
        mouseCoords = '''
        0,0       X increases -->
        +---------------------------+
        |                           | Y increases
        |                           |     |
        |   1920 x 1080 screen      |     |
        |                           |     V
        |                           |
        |                           |
        +---------------------------+ 1919, 1079    
        '''
        # currentPosition = pyautogui.position()
        return mouseCoords
    
def usage():
    print("> click script usage:")
    print("\t-h\t-this usage content")
    return True
    
    
if __name__ == "__main__":
    warnings.resetwarnings()
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    args = sys.argv[1:]
    # args = ['-h']
    if "-h" in args:
        usage()
    path = script_path()
    pattern = "mspaint.exe"     # put app name here, to be found
    appId = get_process_id(pattern)
    if not appId:
        print(">>> no process '{}' found...".format(pattern))
        sys.exit()
        
    # ***********  connect with application  ***********
    print("appId: {}".format(appId))    
    app = Application().connect(process=appId)
    appWrap = app_handler(app)
    appWrap.all_actions()
    top_name = appWrap.top_name()
    print(top_name)
    
    

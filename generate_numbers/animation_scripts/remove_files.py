import sys
import os

def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
    
if __name__ == "__main__":
    path = script_path()
    files = [item for item in os.listdir() if item.endswith((".jpg", ".png"))]
    for file in files:
        os.remove(file)
        print("{} file removed...".format(file))

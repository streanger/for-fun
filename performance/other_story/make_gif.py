#story with anime
import imageio
import os
import sys

def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path
    
if __name__ == "__main__":
    path = script_path()
    files_path = os.path.join(path, "animation")
    images = []
    for file in os.listdir(files_path):
        filename = os.path.join(files_path, file)
        print(filename)
        images.append(imageio.imread(filename))
    imageio.mimsave('movie.gif', images, duration=0.0001)
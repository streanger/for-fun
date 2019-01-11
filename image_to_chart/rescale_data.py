import time
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pylab import savefig
import numpy as np

def execute_decorator(func):
    def f(*args, **kwargs):
        before = time.time()
        val = func(*args, **kwargs)
        total = round((time.time() - before), 9)
        print("--> <{}> finished in {}[s]".format(func.__name__, total))
        return val
    return f
    
    
def rescale_data(data_dict, point):
    data = list(data_dict.keys())
    start = stop = 0
    for key, value in enumerate(data[:-1]):
        start = data[key]
        stop = data[key+1]
        if point >= float(start) and point <= float(stop):
            break
    
    # count value in point
    value = data_dict[start] + (data_dict[stop]-data_dict[start])*((point - float(start))/(float(stop) - float(start)))
    return value
    
    
@execute_decorator
def rescale_wrap(data, range_out):
    ''' docs '''
    key_range = len(data)
    linspace_data = [str(item) for item in np.linspace(0, range_out, key_range)]
    data_dict = dict(zip(linspace_data, data))
    wanted = {key: rescale_data(data_dict, key) for key in range(0, range_out)}
    rescaled = list(wanted.values())
    return rescaled
    
    
def just_draw(data, title):
    plt.plot(data, 'ro--', linewidth=1, markersize=5)
    plt.ylabel("y data")
    plt.xlabel("x data")
    plt.grid()
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2))
    plt.suptitle(title)
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')       #full window
    # plt.savefig(title.split('.')[0] + "_max.png")
    if 1:
        plt.show()
        plt.close()
    return True
    
    
if __name__ == "__main__":
    data = [math.sin(x/10) for x in range(100)]     # create data
    rescaled = rescale_wrap(data, 176)              # calc rescaled data
    just_draw(rescaled, "rescaled")
    
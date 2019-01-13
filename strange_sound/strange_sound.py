import os
import sys
import winsound
import time
import random
import wavio
import numpy as np
import matplotlib.pyplot as plt
import math


def script_path():
    '''change current path to script one'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def just_draw(data, title):
    plt.plot(data, linewidth=1)
    plt.ylabel("y data")
    plt.xlabel("x data")
    plt.grid()
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2))
    plt.suptitle(title)
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')       #full window
    # plt.savefig(title.split('.')[0] + ".png")
    if 1:
        plt.show()
        plt.close()
    return True
    
    
def make_wav(sound):
    ''' sounds -> 'beep', 'scary', 'frog' '''
    rate = 22050        # samples per second
    if sound == 'beep':
        x = np.array([math.sin((x**2)/10000) for x in range(1, 220000)])                                                    # beep
    elif sound == 'scary':
        x = np.array([math.sin((x**(math.sin(x/100)))/10000) for x in range(1, 500000)])                                    # scary sound
    elif sound == 'frog':
        x = np.array([(math.sin((x**(math.sin(x**(math.sin(x/10000))/10000)))/10000)) for x in range(200000, 470000)])      # a frog
    else:
        x = np.array([15*math.sin(x/2)*math.e**(-0.0001*x) for x in range(1, 100000)])                                      # asymptotic
    # just_draw(x, 'wave')                                                                                                    # take a lot how on the wave
    wavio.write(sound + ".wav", x, rate, sampwidth=3)
    return True

    
if __name__ == "__main__":
    script_path()
    sound = random.choice(['beep', 'scary', 'frog'])
    make_wav(sound)
    time.sleep(0.1)
    print("current sound: {}".format(sound))
    winsound.PlaySound(sound, winsound.SND_ALIAS | winsound.SND_ASYNC)
    
    
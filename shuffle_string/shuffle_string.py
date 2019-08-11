import sys
import os
from random import shuffle


def script_path():
    '''change current path to script one'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def simple_read(file):
    '''simple_read data from specified file'''
    with open(file, "r") as f:
        s = f.read()
        f.close
    return s
    
    
def simple_write(file, s):
    '''simple_write data to .txt file, with specified s'''
    with open(file, "w") as f:
        f.write(str(s))
        f.close()
    return True
    
    
def shuffle_string(s):
    '''or maybe line by line'''
    lines = s.splitlines()
    out = []
    for line in lines:
        out.append(' '.join([shuffle_word(item) for item in line.split()]))
    out = '\n'.join(out)
    
    # out = '\n'.join([' '.join([swap_word(item) for item in line.split()]) for line in s.splitlines()])  # one-line-version
    return out
    
    
def shuffle_word(s):
    '''shuffle word if item s.strip() is more than three characters'''
    if (len(s.strip()) > 3):
        center = list(s[1:-1])
        shuffle(center)
        out = s[0] + ''.join(center) + s[-1]
    else:
        out = s
    return out
    
    
if __name__ == "__main__":
    script_path()
    s = simple_read('file_in.txt')
    out = shuffle_string(s)
    print(out)
    simple_write('file_out.txt', out)

import time
import random


def rotate(s, n, d):
    n = n%len(s)
    if d:
        n = -n
    return s[n:] + s[:n]
    
    
def ping_pong(s, cycle, flush=True, timeout=0.05):
    '''
        s - string, to be rotated
        cycle - number of significant elements. Examples:
            1) s = '*      '
                cycle -> 1
            2) s = '<*>------------------'
                cycle -> 3
    '''
    direction = False
    counter = 0
    cycleLen = len(s) - cycle
    while True:
        if not counter%(cycleLen):
            direction = not direction
        out = rotate(s, counter, True)
        if flush:
            print("{}".format(out), end='\r', flush=True)
        else:
            print("{}".format(out))
        
        if direction:
            counter += 1
        else:
            counter -= 1
        time.sleep(timeout)
    return True
    
    
if __name__ == "__main__":
    print("this is very example of ping_pong_string script")
    examples = [('< * >' + '/\\'*20, 5),
                ('< * >' + '~'*20, 5),
                ('*' + ' '*20, 1),
                ('`-`' + ' '*20, 3),
                ('*' + ' '*20, 1),
                ('<*>' + '~'*20, 3)]
    example, cycle = random.choice(examples)
    # example, cycle = ('< * >' + ' '*20, 5)
    example, cycle = examples[4]
    ping_pong(example, cycle, True, 0.02)

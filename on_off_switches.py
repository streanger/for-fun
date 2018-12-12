'''
100 switches
turn on/off all of them with sequence
'''

def states(some):
    for x in range(1, 101):
        some = [item if key%x else not item for key, item in enumerate(some)]
        print(x, some.count(True))
    return some.count(True)
    
    
if __name__ == "__main__":
    switches = [False]*100
    out = states(switches)
    print("switches turn on after 100 times: {}".format(out))

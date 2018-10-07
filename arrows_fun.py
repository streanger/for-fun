'''arrows script, just for fun'''
import time
 
def arrows(size=10, speed=0.1, arrowType=0):
    cannon = "\t>>>>"
    cannon = "\t8==D"
    cannon = "\t|"
    
    wall = tuple(3*'|')
    # wall = ('||', '+|', '#|')
    # wall = ('||', '*|', '#|')
    
    if arrowType == 0:
        arrowRight = "-->"*size
        arrowCenter = "->-"*size
        arrowLeft = ">--"*size
    elif arrowType == 1:
        arrowRight = "    -"*size
        arrowCenter = "  -  "*size
        arrowLeft = "-    "*size 
    elif arrowType == 2:
        arrowRight = "><><"*size
        arrowCenter = "<><>"*size
        arrowLeft = "><><"*size        
    elif arrowType == 3:
        arrowRight = ">->-"*size
        arrowCenter = "->->"*size
        arrowLeft = ">->-"*size
        
    print()
    for x in range(100):
        if x%3 == 0:
            print("{}{}{}".format(cannon, arrowLeft, wall[0]), end='\r', flush=True)
        elif x%3 == 1:
            print("{}{}{}".format(cannon, arrowCenter, wall[1]), end='\r', flush=True)
        else:
            print("{}{}{}".format(cannon, arrowRight, wall[2]), end='\r', flush=True)
        time.sleep(speed)
    print()
    return True
    
    
if __name__ == "__main__":
    arrows(size=10, speed=0.05, arrowType=0)
    
#digital ascii clock
import time
import datetime

def get_time():
    now = datetime.datetime.now()
    if True:
        hour = now.hour
        minute = now.minute
    else:
        hour = now.minute
        minute = now.second
    return str(hour), str(minute)

def ascii_digits(val):
    #size 5x6
    digits = {
    "0":
    """
      __
     /  \\
    |    |
    |    |
     \\__/""",
    "1":
    """
    
     /|
    / |
      |
     _|_""",
    "2":
    """
      __
     /   \\
    |    |
        /
      _/__""",    
    "3":
    """
      __
     /   \\
    |   _/
         \\
     \___/""",   
    "4":
    """
    
     /  |
    /   |
    ----|
        |""",
    "5":
    """
     ___
    |   
    |___
        \\
    \___/""",
    "6":
    """
      __
     /  
    |___
    |   \\
     \__/""",
    "7":
    """
    ____
        |
       /
      /
     /""", 
    "8":
    """
     __
    /   \\
    \___/
    /   \\
    \___/""",
    "9":
    """
     __
    /   \\
    \\___|
        |
    \___/""",
    ":":
    """
    
    <>
    
    <>
    """}
    
    digit = digits[val]
    digit = "\n".join([line[4:12] for line in digit.split("\n")])    #remove 4 leading spaces
    return digit

def longest_str(l):
    return max(len(x) for x in l)
    
def join_digits(leftDigit, rightDigit):
    #digits should be 5 line height
    if not leftDigit:
        leftDigit = "\n"*5
    if not rightDigit:
        rightDigit = "\n"*5
    left = leftDigit.split("\n")
    right = rightDigit.split("\n")
    maxL = longest_str(left)
    maxR = longest_str(right)
    new = "\n".join([left[x] + (maxL-len(left[x]))*" " + "  " + right[x] for x in range(6)])
    return new     

def join_digits_list(l):
    #think about class and method for that
    new = ""
    for item in l:
        new = join_digits(new, item)
    return new

def perform_time():
    #get real time and perform it to the useful one
    return True
    
def main():
    last = get_time()
    while 1:
        if last == get_time():
            continue
        else:
            hour, minute = get_time()
            if len(hour) == 1:
                hour = "0" + hour
            if len(minute) == 1:
                minute = "0" + minute
            #just for now
            h0 = ascii_digits(hour[0])
            h1 = ascii_digits(hour[1])
            center = ascii_digits(":")
            m0 = ascii_digits(minute[0])
            m1 = ascii_digits(minute[1])
            clock = [h0, h1, center, m0, m1]
            asciiClock = join_digits_list(clock)
            print("{}".format(asciiClock))
            last = get_time()
    return True
            
if __name__ == "__main__":
    #print(join_digits_list([ascii_digits(str(x)) for x in range(0,10)]))       #example
    main()

      
    
    
    
    

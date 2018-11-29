#digital ascii clock; 29.11.18 - refactored
import time
import datetime

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
    
def get_time(full=False):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second    
    if full:
        return [str(hour), str(minute), str(second)]
    return [str(hour), str(minute)]
    
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
    
def main():
    # secondRefresh = True                # True -> every 1s, False -> every 1m
    # fullFormat = True                   # True -> hh:mm:ss, False -> hh:mm
    fullFormat = secondRefresh = True   # True -> every second full; False -> every minute hh:mm
    last = get_time(secondRefresh)
    while True:
        if last == get_time(secondRefresh):
            continue
        currentTime = ':'.join([item.zfill(2) for item in get_time(fullFormat)])
        asciiClock = join_digits_list([ascii_digits(sign) for sign in currentTime])
        print(asciiClock)
        last = get_time(secondRefresh)
    return True
    
    
if __name__ == "__main__":
    #print(join_digits_list([ascii_digits(str(x)) for x in range(0,10)]))       #example
    main()
    

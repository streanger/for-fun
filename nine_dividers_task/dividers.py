"""by ps, 28.12.2024
Find the number of positive integers not greater than N that have exactly 9 positive divisors.
"""
import sys
try:
    from rich import print
except:
    pass

def positive_dividers_equals_nine(n):
    counter = 0
    for x in range(1, n+1):
        dividors_number = 0
        dividors = []
        for y in range(1, x+1):
            if not x % y:
                dividors_number += 1
                dividors.append(y)
        if DEBUG:
            print(f'{x} -> {dividors_number=} -> {dividors}')
        if dividors_number == 9:
            # we have number that fit conditions
            counter += 1
    return counter

args = sys.argv[1:]
if not args:
    print('usage: python3 dividers.py <number> [-d]')
    sys.exit(0)
n = int(args[0])
if '-d' in args:
    DEBUG = True
else:
    DEBUG = False
counter = positive_dividers_equals_nine(n=n)
print(f'number of integers that in range ({n}): {counter}')

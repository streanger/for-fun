'''just for fun'''

def czy_liczba_jest_podzielna_przez_dwa(liczba):
    if liczba == 0:
        return True
    elif liczba == 1:
        return False
    elif liczba == 2:
        return True
        
        
def write_func(n):
    out = '\n' + 'def czy_liczba_jest_podzielna_przez_dwa(liczba):\n'
    out +=  + 4*' ' + 'if liczba == 0:\n' + 8*' ' + 'return True\n'
    for x in range(1, n):
       out += '{}elif liczba == {}:\n{}return {}\n'.format(4*' ', x, 8*' ', not bool(x%2))
       
    out += 3*'\n' + 'if __name__ == "__main__":\n' + 4*' '
    out += 'print(czy_liczba_jest_podzielna_przez_dwa(4))\n'
    return out
    
    
if __name__ == "__main__":
    some = write_func(20)
    print(some)

import sys
import ctypes

'''
info about functions in most common dlls:
https://www.win7dll.info/user32_dll.html
'''

def help_content():
    some = '''{}
    usage:
        get_key_state.exe [key_code]
    example:
        get_key_state.exe   0x90    -- will return state of numlock
    args:
        -s                          -- show chosen key
        -h                          -- this help content
    more info:
        https://docs.microsoft.com/pl-pl/windows/desktop/inputdev/virtual-key-codes
        https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-getkeystate

        VK_CAPITAL  - 0x14  - CAPS LOCK key
        VK_NUMLOCK  - 0x90  - NUM LOCK key
        VK_SCROLL   - 0x91  - SCROLL LOCK key

    static states:
        off             ->  0
        on              ->  1
        off & pressed   ->  -128
        on & pressed    ->  -127
    \n{}'''.format('***'*31, '***'*31).split('\n')
    out = "\n".join(["*{:<93s}*".format(item) for item in some])
    print(out)
    return True

def get_state(key):
    hllDll = ctypes.WinDLL("User32.dll")
    # return hllDll.GetAsyncKeyState(key)
    return hllDll.GetKeyState(key)
    
def main(args):
    if '-h' in args:
        help_content()
        return False
    key = 0x90
    if args:
        try:
            if args[0].startswith("0x"):
                key = int(args[0], 16)
            else:
                key = int(args[0], 10)
        except ValueError as err:
            print("error: {}".format(err))
            return False
    state = get_state(key)
    if '-s' in args:
        print("state of {}: {}".format(hex(key), state))
    else:
        print(state)
    return True
    
    
if __name__ == "__main__":
    main(sys.argv[1:])
    

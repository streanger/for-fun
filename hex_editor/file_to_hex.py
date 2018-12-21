''' such as simple hex editor '''
import sys
import os
import codecs
import hashlib

def usage():
    print("todo:")
    print("put usage content here:")
    print("\t-specify file in")
    print("\t-specify file out")
    print("\t-specify number of bytes in column")
    print("\t-specify number of columns in row")
    print("\t-out data -> print or save into file")
    print("\t-with -c parameter, sha1 hash is calculated")
    return True
    
    
def script_path():
    '''change current path to script one'''
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)
    return currentPath
    
    
def simple_read(file):
    '''simple_read data from specified file'''
    with codecs.open(file, "r", encoding="utf-8", errors='ignore') as f:
        content = f.read()
    return content
    
    
def simple_write(file, content):
    '''simple_write data to specified file'''
    with codecs.open(file, "w", encoding="utf-8", errors='ignore') as f:
        f.write(str(content))
    return True
    
    
def address(n, value):
    return '{:08x}'.format(n*value)
    
    
def calc_hash(file, type):
    '''
    copied from https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    TL;DR use buffers to not use tons of memory.
    '''
    
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
            
    if type == 'md5':
        return md5.hexdigest()
    elif type == 'sha1':
        return sha1.hexdigest()
    else:
        return False
        
        
def data_to_hex(data, bytesInColumn, columnsInRow):
    out = ''.join(['{:02x}'.format(ord(item)) for item in data])
    outBytes = [out[n:n+bytesInColumn*2] for n in range(0, len(out), bytesInColumn*2)]
    rowBytes = [outBytes[n:n+columnsInRow] for n in range(0, len(outBytes), columnsInRow)]
    hexContent = '\n'.join([address(key, bytesInColumn*columnsInRow) + ': ' + ' '.join(row) for key, row in enumerate(rowBytes)])
    return hexContent
    
    
def hex_to_data():
    ''' reverse way on conversion '''
    data = 'after conversion'
    return data
    
    
if __name__ == "__main__":
    currentPath = script_path()
    args = sys.argv[1:]
    args = ['example.py']
    if args:
        file = args[0]
        if '-c' in args:
            out = calc_hash(file, 'sha1')
            print(out)
        else:
            data = simple_read(file)
            bytesInColumn = 2
            columnsInRow = 8
            out = data_to_hex(data, bytesInColumn, columnsInRow)
            # print(out)
            simple_write(file.split('.')[0], out)
    else:
        usage()
        
        
'''
todo:
-clean it up
-make help/usage content
-use parameters

-create hex_to_data function
'''
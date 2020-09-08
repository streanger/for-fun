'''
info:
    -script which encodes any file to .txt with phone numbers
'''
import sys
import os


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
# *********** phone chars encoding ***********
def chars_dict():
    data = {
        '1': '',
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz',
        '0': ' ',
        '*': '+',
        }
    return data
    
    
def map_chars_to_num(data):
    chars_map = {}
    for key, val in data.items():
        if not val:
            continue
        for char in val:
            chars_map[char] = key*(val.find(char)+1)
    return chars_map
    
    
def char_encoder(s, chars_map):
    out = []
    for char in s:
        out.append(chars_map[char])
    return ' '.join(out)
    
    
def char_decoder(s, chars_map):
    out = ''
    for char in s.split():
        out += chars_map[char]
    return out
    

    
    
# *********** covnert hex to chars and vice-versa ***********
def hex_to_char():
    chars = list('abcdefghijklmnopqrstuvwxyz'[:16])
    hex_vals = [ord('{:01x}'.format(x)) for x in range(16)]
    data = dict(zip(hex_vals, chars))
    # return data[val]
    return data
    
    
def char_to_hex():
    chars = [ord(char) for char in 'abcdefghijklmnopqrstuvwxyz'[:16]]
    hex_vals = ['{:01x}'.format(x) for x in range(16)]
    data = dict(zip(chars, hex_vals))
    # return data[val]
    return data
    
    
def read_bin(file):
    data = b''
    with open(file, 'rb') as f:
        data = f.read()
    return data
    
    
def write_bin(file, data):
    with open(file, 'wb') as f:
        f.write(data)
    return None
    
    
def img_to_hexstring(img):
    '''convert img to lowercase hexstring'''
    out = ''.join(['{:02x}'.format(item) for item in img])
    return out
    
    
def hexstring_to_img(s):
    # out = b''
    out = bytes([int(s[n:n+2], 16) for n in range(0, len(s), 2)])
    return out
    
    
def example():
    '''
    data = chars_dict()
    chars_map = map_chars_to_num(data)
    chars_map_reversed = {val:key for key, val in chars_map.items()}
    
    # ******** encode ********
    s = 'testowy string'
    # s = 'daj plusa'
    out = char_encoder(s, chars_map)
    print(out)
    
    
    # ******** decode ********
    decoded = char_decoder(out, chars_map_reversed)
    print(decoded)
    '''
    
    # ******** hexstring to chars encode & decode example ********
    '''
    hexstring = 'aabbccddeeff'
    print(hexstring)
    hex_to_char_dict = hex_to_char()
    encoded = hexstring.translate(hex_to_char_dict)
    print(encoded)
    
    char_to_hex_dict = char_to_hex()
    decoded = encoded.translate(char_to_hex_dict)
    print(decoded)
    '''
    return None
    
    
def write_file(file, s):
    with open(file, 'w', encoding="utf-8") as f:
        f.write(s)
    return None
    
    
def read_file(file):
    data = ''
    with open(file, 'r', encoding="utf-8") as f:
        data = f.read()
    return data
    
    
def file_to_phone_numbers(file):
    # ******** conver img to hexstring ********
    img_bytes = read_bin(file)
    img_hexstring = img_to_hexstring(img_bytes)
    
    # ******** hexstring to chars encode********
    hex_to_char_dict = hex_to_char()
    encoded = img_hexstring.translate(hex_to_char_dict)
    
    # ******** encode to phone numbers ********
    data = chars_dict()
    chars_map = map_chars_to_num(data)
    out = char_encoder(encoded, chars_map)
    
    # ******** write to file ********
    filename = '{}_encoded.txt'.format(file.split('.')[0])
    write_file(filename, out)
    return None
    
    
def phone_numbers_to_file(file):
    encoded_phone_chars = read_file(file)
    
    # phone chars to text
    data = chars_dict()
    chars_map = map_chars_to_num(data)
    chars_map_reversed = {val:key for key, val in chars_map.items()}
    decoded = char_decoder(encoded_phone_chars, chars_map_reversed)    
    
    # ascii lowercase to hex
    char_to_hex_dict = char_to_hex()
    hexstring = decoded.translate(char_to_hex_dict)
    
    # hex to img
    img_bytes = hexstring_to_img(hexstring)
    
    # write bytes to img file
    if img_bytes.startswith(b'\xff\xd8\xff\xe0'):
        file_format = 'jpg'
    else:
        file_format = 'png'
    filename = '{}_decoded.{}'.format(file.split('.')[0], file_format)
    write_bin(filename, img_bytes)
    return None
    
    
if __name__ == "__main__":
    script_path()
    file = 'image.jpg'
    file_to_phone_numbers(file)     # create file with extension changed to .txt
    
    
    file = 'image_encoded.txt'
    phone_numbers_to_file(file)    # write to jpg. or .png file with original name + '_decoded'

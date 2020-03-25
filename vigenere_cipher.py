

def vigenere_cipher(s, key, encode=True, ignore_foreign=False, own_string=''):
    '''vigenere_cipher
        -strings are ascii_lowercase and ascii_uppercase
        -use for encode (encode=True) or decode(encode=False)
        -use ignore_foreign (True/False), to ommit not specified characters 
        -for different type of strings, use your own (own_string)
    '''
    
    if own_string:
        ascii_lowercase = own_string.lower()
    else:
        from string import ascii_lowercase
    ascii_uppercase = ascii_lowercase.upper()
    
    if encode:
        value = 1
    else:
        value = -1
        
    key = key.lower()
    out = ''
    key_index = 0
    for index, item in enumerate(s):
        key_value = ascii_lowercase.find(key[key_index])
        if item in ascii_lowercase:
            key_index += 1
            new_index = (ascii_lowercase.find(item) + value*key_value)%len(ascii_lowercase)
            out += ascii_lowercase[new_index]
        elif item in ascii_uppercase:
            key_index += 1
            new_index = (ascii_uppercase.find(item) + value*key_value)%len(ascii_lowercase)
            out += ascii_uppercase[new_index]
        else:
            if not ignore_foreign:
                out += item
                
        if key_index == len(key):
            key_index = 0
            
    return out
    
if __name__ == "__main__":
    key = 'something'
    print('key: {}'.format(key))    
    s = 'the very message, to encrypt'
    print('s: {}'.format(s))
    # own_string = ''.join(list(set(list(s+key))))  # optional
    encoded = vigenere_cipher(s, key, encode=True, ignore_foreign=False)
    print('encoded: {}'.format(encoded))
    decoded = vigenere_cipher(encoded, key, encode=False, ignore_foreign=False)
    print('decoded: {}'.format(decoded))
    
'''
info:
    -in vigenere_cipher non-ascii (string) characters are not countered
    -increase key index only if encounter ascii char

'''

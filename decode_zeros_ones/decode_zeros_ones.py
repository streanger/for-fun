

def decode_zeros_ones(s):
    return ''.join([chr(int(item, 2)) for item in s.split()])
    
    
def encode_zeros_ones(s):
    return ' '.join(['{:08b}'.format(ord(item)) for item in s])
    
    
if __name__ == "__main__":
    # examples
    text = 'this is very secret text'
    encoded = encode_zeros_ones(text)
    print(encoded)
    
    encoded = "01110100 01101000 01101001 01110011 00100000 01101001 01110011 00100000 01110110 01100101 01110010 01111001 00100000 01110011 01100101 01100011 01110010 01100101 01110100 00100000 01110100 01100101 01111000 01110100"
    decoded = decode_zeros_ones(encoded)
    print(decoded)

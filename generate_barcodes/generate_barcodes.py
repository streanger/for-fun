import sys
import os
import barcode
from barcode.writer import ImageWriter


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def create_barcodes(str_to_encode, specified_type=''):
    '''create barcode(s) from specified str_to_encode
       if specified_type is default, it iters through all types
    '''
    barcode_types = barcode.PROVIDED_BARCODES
    if specified_type in barcode_types:
        barcode_types = [specified_type]
        
    for item in barcode_types:
        try:
            status = True
            barcode_object = barcode.get_barcode_class(item)
            encoded = barcode_object(str_to_encode, writer=ImageWriter())
            fullname = encoded.save('{}_barcode'.format(item))
        except:
            status = False
        print('type: {}, status: {}'.format(item, status))
    return True
    
    
if __name__ == "__main__":
    script_path()
    str_to_encode = '123456789'
    create_barcodes(str_to_encode, specified_type='')
    create_barcodes(str_to_encode, specified_type='code128')
    
    
'''
info, barcode types:
    code128     -common
    code39
    ean
    ean13
    ean14
    ean8
    gs1
    gs1_128
    gtin
    isbn
    isbn10
    isbn13
    issn
    itf
    jan
    pzn
    upc
    upca
    code128
    code39
    ean
'''

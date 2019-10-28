import sys
import os


def read_dictio(file):
    with open(file, 'r') as f:
        data = [item.lower() for item in f.read().splitlines()]
        f.close()
    return data
    
    
def adjust_word(w, dictio):
    '''my own adjut alghoritm
        conditional:
            -startswith
            -endswith
            -contain
            -number of the same letters (not in use for now)
            -len
            
        vovel_mode, tip: for long words vovel_mode=True is more accurate. For short words is more dismatch
       
        think of:
            -item_chunk_center
            
        modes = ['normal', 'vovel_mode', 'replace_double']
        
        THIS IS WITH THREE MODES
    '''
    vowels = ['a', 'e', 'i', 'o', 'u']
    modes = ['normal', 'vovel_mode', 'replace_double']
    best_adjusted = []
    # cut_off_level = 10
    cut_off_level = 100
    from string import ascii_lowercase
    
    for mode in modes:
        adjusted = []
        store_w = w
        for item in dictio:
            rate = 0
            
            # ************ NORMAL ************
            if mode == 'normal':
                correct = 0
                
                
            # ************ VOVEL_MODE ************
            if mode == 'vovel_mode':
                correct = 1
                store_item = item
                for vowel in vowels:    
                    item = item.replace(vowel, '')
                    w = w.replace(vowel, '')
                    
                    
            # ************ REPLACE_DOUBLE ************
            # replace double and more same characters near to each other
            # for now just for two same characters
            if mode == 'replace_double':
                correct = 0
                store_item = item
                for c in ascii_lowercase:    
                    item = item.replace(c*2, c)
                    w = w.replace(c*2, c)
                    
                # most powerful
                if item == w:
                    rate = 99
                    adjusted.append((store_item, rate))
                    break
                    
            if item.startswith(w) or item.endswith(w):
                rate += 8 - correct
            if w.startswith(item) or w.endswith(item):
                rate += 8 - correct
            if item in w or w in item:
                rate += 5 - correct
                
            if len(item) > 2:
                item_chunk_begin = item[:round(len(item)*(2/3))]
                item_chunk_end = item[round(len(item)*(1/3)):]
                # item_chunk_center     # think of
                if w.startswith(item_chunk_begin) or w.endswith(item_chunk_end) or item_chunk_begin in w or item_chunk_end in w:
                    rate += 3 - correct
                    
            if len(w) > 2:
                w_chunk_begin = w[:round(len(w)*(2/3))]
                w_chunk_end = w[round(len(w)*(1/3)):]
                if item.startswith(w_chunk_begin) or item.endswith(w_chunk_end) or w_chunk_begin in item or w_chunk_end in item:
                    rate += 3 - correct
                    
            if len(item) == len(w):
                rate += 4 - correct
            if abs(len(item) - len(w)) == 1:
                rate += 3 - correct
            if abs(len(item) - len(w)) == 2:
                rate += 2 - correct
            if abs(len(item) - len(w)) > 0.5*len(w):
                rate -= 5 + correct
                
                
            if mode == 'vovel_mode':
                adjusted.append((store_item, rate))
                w = store_w         # it need to be restored
            elif mode == 'replace_double':
                adjusted.append((store_item, rate))
                w = store_w         # it need to be restored
            else:
                adjusted.append((item, rate))
                
                
        adjusted = sorted(adjusted, key = lambda x: x[1], reverse=True)
        if adjusted[0][1] > cut_off_level:
            # print('break in mode: {}'.format(mode))
            return adjusted[0][0]
        best_adjusted.append(adjusted[0])
        
    # print('best_adjusted: {}'.format(best_adjusted))
    out = sorted(best_adjusted, key = lambda x: x[1], reverse=True)
    return out[0][0]
    
    
def s_preprocessor(s):
    '''preprocessing input string(s) to more readable value:
        things:
            -lowercase
            -remove nonascii
            -compare with dictionary
    '''
    from string import ascii_lowercase
    # dictio = ['some', 'thing']
    dictio = read_dictio('3000_english_words.txt')
    s = s.lower()
    s = [''.join([c for c in item if c in ascii_lowercase]) for item in s.split()]
    
    # s = ' '.join([item if item in dictio else '?'*len(item) for item in s])             # change wrong words to questionmarks
    # s = ' '.join([item if item in dictio else item + '(?)' for item in s])              # show which words are  wrong
    s = ' '.join([item if item in dictio else adjust_word(item, dictio) for item in s])              # adjusted
    return s
    
    
def example():
    os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
    dictio = read_dictio('3000_english_words.txt')
    wrong_words = ['thisn',
                   'eecontinuueeeeeeed',
                   'rthhiinngs',
                   'edownr',
                   'veryds',
                   'mordered',
                   'eppeersonality',
                   'profesesionalled',
                   'qrtrbck',
                   'asdqaddres',
                   'meanned'
                   ]
    for w in wrong_words:
        out = adjust_word(w, dictio)
        print('{}, {}'.format(w, out))
    return True
    
    
if __name__ == "__main__":
    os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
    
    # some = "The Very s'omething no.w. Let?s ta[LK abo(ut IT"
    # some = "this is veRY mEE myse;'lf and i]"
    some = "thisn veryd thhings heree edownr noww"
    print(some)
    out = s_preprocessor(some)
    print(out)
    print()
    
    example()
    
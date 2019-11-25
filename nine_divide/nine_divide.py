import random
from juster import justify


def shuffled_val(val):
    item = list(str(val))
    random.shuffle(item)
    thing = int(''.join(item))
    return thing
    
    
def iter_val(val):
    header = ['val', 'shuffled', 'result', 'result/9']
    total = []
    total.append(header)
    for x in range(19):
        out = shuffled_val(val)
        total.append((val, out, val-out, (val-out)/9))
    justified = justify(total, frame=True, enumerator=True, header=True)
    return justified
    
    
if __name__ == "__main__":
    val = 75343902
    justified = iter_val(val)
    print(justified)



def reverse_str(data, patterns):
    ''' reverse string with patterns list '''
    left = ""
    right = ""
    last = len(data)
    for key, item in enumerate(data):
        if item in patterns:
            left += item
        else:
            if not (len(left) - last):
                break
            elif abs(len(left) - last) == 1:
                left += item
                break
            for thing in data[len(left):last][::-1]:
                last -= 1
                if thing in patterns:
                    right += thing
                else:
                    right += item
                    left += thing
                    break
    return left + right[::-1]
    
    
if __name__ == "__main__":
    data = '123456789'
    # data = '124879'
    # data = '123456784111488418143'*10
    out = reverse_str(data, ['1', '4', '8'])
    print(out)
    
    
    
    
    
    
    

# py2.x
def parts(value, divider):
    out = [divider]*(value/divider)
    if value%divider:
        out.append(value%divider)
    return out
    
# py3.x
def parts(value, divider):
    out = [divider]*(value//divider)
    if value%divider:
        out.append(value%divider)
    return out
    
    
out = parts(1023, 240)
print(out)
for key, item in enumerate(out):
    print(key, item)
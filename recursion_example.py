''' recursion example '''

def some(n):
    if n < 3:
        return [1]*n
    else:
        return some(n-1) + some(n-2) + some(n-3)

for x in range(30):
    out = len(some(x))
    print(x, out)

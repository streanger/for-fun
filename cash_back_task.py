import random


def cash_in_register():
    coins = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.00, 2.00, 5.00, 10.00, 20.00, 50.00, 100.00, 200.00, 500.00]
    data = [(coin, random.randrange(20)) for coin in coins]
    return data
    
    
def calc_rest(prize, cash, register):
    '''for now without use of register'''
    coins = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.00, 2.00, 5.00, 10.00, 20.00, 50.00, 100.00, 200.00, 500.00]
    diff = cash - prize
    possible_coins = [coin for coin in coins if coin <= diff][::-1]
    
    out = []
    for coin in possible_coins:
        number = diff//coin
        if not number:
            continue
        out.append((coin, int(number)))
        diff -= number*coin
        diff = round(diff, 2)
        # print('current coin: {}, diff: {}'.format(coin, diff))
        
    return out
    
    
if __name__ == "__main__":
    prize = 17.43                               # how much u need to pay
    cash = 200.00                               # the money u have
    register = cash_in_register()               # total cash in register
    out = calc_rest(prize, cash, register)      # rest for u
    print('out: {}'.format(out))
    
    sum_of = round(sum([item[0]*item[1] for item in out]), 2)
    print(sum_of)

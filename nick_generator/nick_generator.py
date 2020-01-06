import random
from string import ascii_lowercase


def generate_nick(fully_random=True, vowel_start=False, max_vowels_len=2, max_consonants_len=2, max_nick_len=8):
    '''
        -start -from vowel or consonant
        -max consonants in neighborhood (1-3)
        -max vowels in neighborhood (1-2)
        -max nick lenght
    '''

    full = 'abcdefghijklmnopqrstuvwxyz'
    vowels = 'aeijouy'
    consonants = 'bcdfghklmnpqrstvwxz'
    
    nick = ''
    
    if fully_random:
        vowel_start = random.choice((True, False))
        max_vowels_len = random.randrange(1, 3)         # values 1, 2
        max_consonants_len = random.randrange(1, 4)     # values 1, 2, 3
        max_nick_len = random.randrange(5, 11)          # values 4 - 10
        
        while (max_nick_len - len(nick)) > 1:
            if vowel_start:
                nick += ''.join([random.choice(vowels) for x in range(max_vowels_len)])
            else:
                nick += ''.join([random.choice(consonants) for x in range(max_consonants_len)])
            vowel_start = not vowel_start
    else:
        if vowel_start is None:
            vowel_start = random.choice((True, False))
            
        while (max_nick_len - len(nick)) > 1:
            if vowel_start:
                nick += ''.join([random.choice(vowels) for x in range(max_vowels_len)])
            else:
                nick += ''.join([random.choice(consonants) for x in range(max_consonants_len)])
            vowel_start = not vowel_start
            
    return nick
    
    
    
if __name__ == "__main__":
    nicks = sorted([generate_nick(fully_random=False, vowel_start=None, max_vowels_len=1, max_consonants_len=1) for x in range(1000)])
    for nick in nicks:
        print(nick)

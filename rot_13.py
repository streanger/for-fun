# task: Cryptography can be easy, do you know what ROT13 is? cvpbPGS{abg_gbb_onq_bs_n_ceboyrz}

def rot_13(s):
    '''my own one-line-implementation of rot13'''
    return ''.join([chr(((65+32*(ord(c)//97)))+(ord(c)-((65+32*(ord(c)//97)))+13)%26) if (ord(c) in range(65, 91)) or (ord(c) in range(97, 123)) else c for c in s])
    
    
if __name__ == "__main__":
    some = 'aAdDzZ'
    out = rot_13(some)              # encryption
    print(some, out)
    
    out = rot_13(rot_13(some))      # encryption and decryption example
    print(some, out)
    
    some = 'cvpbPGS{abg_gbb_onq_bs_n_ceboyrz}'
    out = rot_13(some)
    print(out)
    # out: picoCTF{not_too_bad_of_a_problem}
    
    test = 'qwertyuiopasdfghjklzxcvbnm_@!#$#Q_(%*7'*9000
    print(len(test))
    out = rot_13(test)
    
    
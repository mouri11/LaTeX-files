from functools import reduce

def hashing(msg): 
    print("String:",msg)
    print("Binary:",''.join(['{:08b}'.format(ord(m),'b') + ' ' for m in msg]))
    hashed = ''
    for m in msg:
        hashed += str(reduce(lambda i,j: int(i) ^ int(j), format(ord(m),'b')))
    print("Hash:",hashed)

hashing('CRYPTO') # 110011
hashing('FINALE')
import numpy as np

def rn_box(n): # random permutation of input symbols
    arr = [hex(int(i)) for i in np.arange(n)]# hex symbols
    # mapping each symbol to its random substitute
    return {i:j for i,j in zip(arr,
                               np.random.permutation(arr))}

def main(sbox): # takes plaintext and performs confusion
    p = input("Enter your plaintext:")
    if not all(x in [format(i,'x') for i in sbox] 
               for x in p):# checking if in range [0-f]
        exit("Enter valid characters[0-f]!")
    str1 = {format(i,'x'):format(j,'x') for i,j 
    in sbox.items()}
    return "".join([str1[i] for i in p])

sbox = {0x0: 0x5, 0x1: 0x4, 0x2: 0xd, 0x3: 0x1, 0x4: 0x2, 
        0x5: 0xf, 0x6: 0x6, 0x7: 0x0, 0x8: 0x8, 0x9: 0xc, 
        0xa: 0xb, 0xb: 0x9, 0xc: 0x7, 0xd: 0xe, 0xe: 0xa, 
        0xf: 0x3} # generated using rn_box(int)
        
# print(rn_box(16)) # to generate a random s-box
print(main(sbox))
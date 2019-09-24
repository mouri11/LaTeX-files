from functools import reduce
from operator import xor
import numpy as np

sbox1 = {0x0: 0xf, 0x1: 0xe, 0x2: 0xb, 0x3: 0xc, 0x4: 0x6, 
       0x5: 0xd, 0x6: 0x7, 0x7: 0x8, 0x8: 0x0, 0x9: 0x3, 
       0xa: 0x9, 0xb: 0xa, 0xc: 0x4, 0xd: 0x2, 0xe: 0x1, 
       0xf: 0x5}

keys = list('6fec') # generated using openssl rand -hex 2
mask = int('d',16) # mask d has highest bias

def sbox(p):
    if format(p,'x') not in [format(i,'x') for i in sbox1]:
        exit("Invalid literal")
    return sbox1[p]

def sbox_inv(c):
    for i,j in sbox1.items():
        if c == int(format(j,'x'),16):
            return int(format(i,'x'),16)

def Sypher00C(p,n):
    for i in range(n):
        p = sbox(p ^ int(keys[i],16))
    return p ^ int(keys[-1],16)

def lin_crypt_k3():
    sum = [0]*16
    print("k3 =",keys[-1])
    frmt = "{:>3}"*len(sum)
    print("Guesses",frmt.format(*[format(i,'x') 
                                for i in range(16)]))

    for p in range(16):
        c = Sypher00C(p,3)
        lst = []
        for k in range(16):
            y_ = sbox_inv(c ^ k)
            # mask & p and then changing to binary list
            p_ = np.array([int(i) 
                for i in list('{:04b}'.format(p & mask,'b'))])
            
            # mask & y' and then changing to binary list
            c_ = np.array([int(i) 
                for i in list('{:04b}'.format(y_ & mask,'b'))])
            
            # (d.m) xor (d.y')
            xored = reduce(xor,p_) ^ reduce(xor,c_)
            lst.append(xored)
        
        sum = [i+j for i,j in zip(lst,sum)]
        print((format(p,'x')+'-'+format(c,'x')).ljust(5),
              '|'.rjust(1),frmt.format(*lst))

    print("T0---> ",frmt.format(*[16-i for i in sum]))
    print("T1---> ",frmt.format(*sum))
    candidates = [i for i,j in enumerate(sum) if j == max(sum) 
    or j == min(sum)]
    candidates.sort()
    print("Candidate keys:",*[format(i,'x') for i in 
          candidates],'\n')
    
def lin_crypt_k0():
    sum = [0]*16
    print("k0 =",keys[0])
    frmt = "{:>3}"*len(sum)
    print("Guesses",frmt.format(*[format(i,'x') 
                                for i in range(16)]))
    
    for p in range(16):
        c = Sypher00C(p,3)
        lst = []
        for k in range(16):
            v_ = sbox(p ^ k)
            # mask & m' and then changing to binary list
            p_ = np.array([int(i) 
                for i in list('{:04b}'.format(v_ & mask,'b'))])
            
            # mask & c and then changing to binary list
            c_ = np.array([int(i) 
                for i in list('{:04b}'.format(c & mask,'b'))])
            
            # (d.v') xor (d.c)
            xored = reduce(xor,p_) ^ reduce(xor,c_)
            lst.append(xored)
        
        sum = [i+j for i,j in zip(lst,sum)]
        print((format(p,'x')+'-'+format(c,'x')).ljust(5),
              '|'.rjust(1),frmt.format(*lst))
    
    print("T0---> ",frmt.format(*[16-i for i in sum]))
    print("T1---> ",frmt.format(*sum))
    candidates = [i for i,j in enumerate(sum) if j == max(sum) 
    or j == min(sum)]
    candidates.sort()
    print("Candidate keys:",*[format(i,'x') for i in 
          candidates])

lin_crypt_k3()
lin_crypt_k0()
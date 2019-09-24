from functools import reduce
from operator import xor
import numpy as np

sbox = {0x0: 0x5, 0x1: 0x4, 0x2: 0xd, 0x3: 0x1, 0x4: 0x2, 
       0x5: 0xf, 0x6: 0x6, 0x7: 0x0, 0x8: 0x8, 0x9: 0xc, 
       0xa: 0xb, 0xb: 0x9, 0xc: 0x7, 0xd: 0xe, 0xe: 0xa, 
       0xf: 0x3}

def lat(sbox):
    lst1 = [format(i,'x') for i,j in sbox.items()]
    print("in\\out|",("{:>3}"*len(lst1[1:])).format(*lst1[1:])) 
    print('-'*56)

    lat_dict = {} # to store count for each mask
    for alpha in range(1,16):
        for beta in range(1,16):
            lat_dict[beta] = 0

            for x,sx in sbox.items():
                x_arr = np.array([int(i) for i in # x . alpha
                        list('{:04b}'.format(x & alpha,'b'))])
                sx_arr = np.array([int(i) for i in # sx . beta
                        list('{:04b}'.format(sx & beta,'b'))])
                if reduce(xor,x_arr) == reduce(xor,sx_arr):
                    lat_dict[beta] += 1
        
        lst2 = [str(int((j/16-0.5)*16)) for i,j in 
        lat_dict.items()] # eps = p - 1/2
        lst2 = list(map(lambda b:b.replace('0','.'),lst2))
        
        # formatting table
        frmt = "{:>3}"*len(lst2)
        print(str(format(alpha,'x')+'  |').rjust(7),
              frmt.format(*lst2))

lat(sbox)
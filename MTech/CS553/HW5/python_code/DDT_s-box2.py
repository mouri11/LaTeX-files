from collections import Counter

sbox1 = {0x0: 0x8, 0x1: 0x6, 0x2: 0x7, 0x3: 0x9, 0x4: 0x3, 
        0x5: 0xc, 0x6: 0xa, 0x7: 0xf, 0x8: 0xd, 0x9: 0x1, 
        0xa: 0xe, 0xb: 0x4, 0xc: 0x0, 0xd: 0xb, 0xe: 0x5, 
        0xf: 0x2} # S-Box produced earlier

sbox2 = {0x0: 0xc, 0x1: 0x6, 0x2: 0x7, 0x3: 0x9, 0x4: 0x4, 
        0x5: 0x8, 0x6: 0xa, 0x7: 0xf, 0x8: 0x5, 0x9: 0x1, 
        0xa: 0xe, 0xb: 0x3, 0xc: 0x0, 0xd: 0xb, 0xe: 0xd, 
        0xf: 0x2}

# sbox3 = {0x0: 0xc, 0x1: 0x6, 0x2: 0x7, 0x3: 0x9, 0x4: 0x3, 
#         0x5: 0x8, 0x6: 0xa, 0x7: 0xf, 0x8: 0x5, 0x9: 0x1, 
#         0xa: 0xe, 0xb: 0x4, 0xc: 0x0, 0xd: 0xb, 0xe: 0xd, 
#         0xf: 0x2}

# sbox1 = {0x0: 0x6, 0x1: 0x4, 0x2: 0xc, 0x3: 0x5, 0x4: 0x0, 
#         0x5: 0x7, 0x6: 0x2, 0x7: 0xe, 0x8: 0x1, 0x9: 0xf, 
#         0xa: 0x3, 0xb: 0xd, 0xc: 0x8, 0xd: 0xa, 0xe: 0x9, 
#         0xf: 0xb}

def ddt(sbox):
    lst1 = [format(i,'x') for i,j in sbox.items()]
    print("in\\out|", ("{:>3} &"*len(lst1)).format(*lst1)) 
    print('-'*56)
    countlist = {}
    for diff in sbox:
        u1 = [hex(i^diff) for i in sbox]
        S_u0 = [hex(j) for i,j in sbox.items()] # S[u0]
        S_u1 = [hex(sbox[(int(i,0))]) for i in u1] # S[u1]
        S_u0_x_S_u1 = [hex(int(i,0)^int(j,0)) for i,j 
        in zip(S_u0,S_u1)] # S[u0] xor S[u1]
        # counting occurences and replacing 0 with '-'
        count = {hex(i):'-' if S_u0_x_S_u1.count(hex(i)) 
        == 0 else S_u0_x_S_u1.count(hex(i)) for i in sbox}        
        # format output as a table
        lst = [str(i) for j,i in count.items()]
        frmt = "{:>3} &"*len(lst)
        print(str(format(diff,'x')+' & ').rjust(7),frmt.
              format(*lst))

        for i,j in Counter(lst).items():
            if i != '-':
                if i not in countlist:
                    countlist[i] = j
                else:
                    countlist[i] += j
    print(countlist)

ddt(sbox1)
ddt(sbox2)
# ddt(sbox3)
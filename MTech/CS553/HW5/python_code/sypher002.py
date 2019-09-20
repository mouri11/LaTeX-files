sbox1 = {0x0: 0x6, 0x1: 0x4, 0x2: 0xc, 0x3: 0x5, 0x4: 0x0, 
        0x5: 0x7, 0x6: 0x2, 0x7: 0xe, 0x8: 0x1, 0x9: 0xf, 
        0xa: 0x3, 0xb: 0xd, 0xc: 0x8, 0xd: 0xa, 0xe: 0x9, 
        0xf: 0xb}

k0 = 0x4
k1 = 0xe
k2 = 0x6

def sbox(p):
    if p not in [format(i,'x') for i in sbox1]:
        exit("Invalid literal")
    return sbox1[int(p,16)]

def sbox_inv(c):
    for i,j in sbox1.items():
        if c == j:
            return format(i,'x')

def sypher002(p):
    return sbox1[sbox1[p^k0]^k1]^k2

def diff_crypt():
    k2_list = []
    for i in range(8):
        c0 = sypher002(i)
        c1 = sypher002(i^int('f',16))
        # print(c0,c1)
        temp = []
        for k2_ in sbox1:
            x0 = c0^k2_
            x1 = c1^k2_
            w0 = sbox_inv(x0)
            w1 = sbox_inv(x1)
            temp.append(1 if format(int(w0,16)^int(w1,16),'x') == 'd' else 0)
        k2_list.append(temp)
        print(temp)    
    
    return k2_list

#p = input("Enter plaintext:")
#print(format(sbox(input("Enter plaintext:")),'x'))
#print(sypher002('f'))
#print(sbox_inv(p))
k = diff_crypt()

lst = [0] * 16
for i in k:
    for j in range(len(i)):
        lst[j] += i[j]

print(lst)
# print(type(p))
# for i in sbox1:
#     print(hex(i))
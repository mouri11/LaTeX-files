# messages taken as input from input.txt
import numpy as np
import sys

# orig_stdout = sys.stdout
# f = open('output_cnfrm.txt','w')
# sys.stdout = f

sbox1 ={0x0: 0x6, 0x1: 0x4, 0x2: 0xc, 0x3: 0x5, 0x4: 0x0, 
        0x5: 0x7, 0x6: 0x2, 0x7: 0xe, 0x8: 0x1, 0x9: 0xf, 
        0xa: 0x3, 0xb: 0xd, 0xc: 0x8, 0xd: 0xa, 0xe: 0x9, 
        0xf: 0xb}

def sbox_4x(msg, bits): # 4-input sbox
    if len(msg) != int(bits,0):# check for message length 
        exit("Plaintext size should be of " + bits + " bits")
    subs = []
    for m in msg: # check for invalid literal
        if m not in [format(i,'x') for i in sbox1]:
            exit("Invalid literal")
        subs.append(format(sbox1[int(m,16)],'x'))
    return subs

def pbox(sbox_out,bits):
    if len(sbox_out) != int(bits,0):
        exit("Too small sbox output!!")
    perm = [b for a in sbox_out # changing hex to binary
            for b in list("{0:04b}".format(int(a,16)))]
    # pbox = sbox output in numpy array and transposing
    perm = np.asarray(perm)
    perm = np.reshape(perm,(4,4)).transpose()
    return "".join([format(int("".join(a),2),'x') 
                   for a in perm])

def sypher004(msg, bits): 
    # uncomment below lines for more verbose output
    # keys = ['c253','0466','affe','645e','0509','fff2'] # keys
    keys = ['340b','3ffc','edfd','8c7d','0696','ffff']
    if len(msg) != int(bits,0):
        exit("Plaintext size should be of " 
             + bits + " bits")
    #print("Round 0:",msg)
    msg = "{:04x}".format(int(msg,16) ^ int(keys[0],16),'x')
    #print("Round 0 (XOR) :","{0:016b}".format(int(msg,16)))

    for i in range(1,len(keys) - 1):
        msg = "".join(sbox_4x(msg,bits))
        # print("Round",str(i),"(Sbox):","{0:016b}"
        # .format(int(msg,16)))
        msg = pbox(msg,bits)
        # print("Round",str(i),"(Perm):","{0:016b}"
        # .format(int(msg,16)))
        msg = "{:04x}".format(int(msg,16)^int(keys[i],16),'x')
        # print("Round",str(i)," (XOR):","{0:016b}"
        # .format(int(msg,16)))
    return msg

def conform_pairs():
    print(" m0 "," m1 "," c0 "," c1 ",)
    print("-"*19)
    count = 0
    with open("./input.txt") as file:
        for line in file:
            m0,m1 = line.strip().split(" ")
            c0 = sypher004(m0,"4")
            c1 = sypher004(m1,"4")
            if int(c0,16)^int(c1,16) == int('8000',16):
                print(m0,m1,c0,c1)
                count += 1
    # sys.stdout = orig_stdout
    # f.close()
    print("There are",count,"conforming message pairs.")

conform_pairs()
# print(sypher004('0001','4'))
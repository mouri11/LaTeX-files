import numpy as np

sbox1 ={0x0: 0x6, 0x1: 0x4, 0x2: 0xc, 0x3: 0x5, 0x4: 0x0, 
        0x5: 0x7, 0x6: 0x2, 0x7: 0xe, 0x8: 0x1, 0x9: 0xf, 
        0xa: 0x3, 0xb: 0xd, 0xc: 0x8, 0xd: 0xa, 0xe: 0x9, 
        0xf: 0xb}

def sbox_4x(msg, bits): # 4-input sbox
    if len(msg) != bits:# check for message length 
        exit("Input size should be of " + format(4*bits) + " bits")
    subs = []
    for m in msg: # check for invalid literal
        if m not in [format(i,'x') for i in sbox1]:
            exit("Invalid literal")
        subs.append(format(sbox1[int(m,16)],'x'))
    return subs

def sbox_4x_inv(cipher, bits):
    if len(cipher) != bits:# check for message length 
        exit("Input size should be of " + format(4*bits) + " bits")
    subs = []
    for c in cipher:
        if c not in [format(i,'x') for i in sbox1.values()]:
            exit("Invalid literal")
        for _c,m in sbox1.items():
            if c == format(m,'x'):
                subs.append(format(_c,'x'))
    return subs

def pbox(sbox_out,bits):
    if len(sbox_out) != bits:
        exit("Too small sbox output!!")
    perm = [b for a in sbox_out # changing hex to binary
            for b in list("{0:04b}".format(int(a,16)))]
    # pbox = sbox output in numpy array and transposing
    perm = np.asarray(perm)
    perm = np.reshape(perm,(4,4)).transpose()
    return "".join([format(int("".join(a),2),'x') 
                   for a in perm])

def sypher004(msg, bits):
    if len(msg) != bits:# check for message length 
        exit("Plaintext size should be of " + format(4*bits) + " bits")

    keys = ['340b','3ffc','edfd','8c7d','0696','ffff']
    msg = "{:04x}".format(int(msg,16) ^ int(keys[0],16),'x')

    for i in range(1,len(keys) - 1):
        msg = "".join(sbox_4x(msg,bits))
        msg = pbox(msg,bits)

        msg = "{:04x}".format(int(msg,16)^int(keys[i],16),'x')

    msg = "".join(sbox_4x(msg,bits))
    msg = "{:04x}".format(int(msg,16)^int(keys[5],16),'x')

    return msg

def sypher004_inv(cipher, bits): # decryption of Sypher004
    if len(cipher) != bits:# check for message length 
        exit("Ciphertext size should be of " + format(4*bits) + " bits")

    keys = ['340b','3ffc','edfd','8c7d','0696','ffff']
    cipher = "{:04x}".format(int(cipher,16) ^ int(keys[len(keys) - 1],16)
                             ,'x')
    cipher = "".join(sbox_4x_inv(cipher,bits))

    for i in range(len(keys) - 2,0,-1):
        cipher = "{:04x}".format(int(cipher,16)^int(keys[i],16),'x')
        cipher = pbox(cipher,bits)
        cipher = "".join(sbox_4x_inv(cipher,bits))

    cipher = "{:04x}".format(int(cipher,16)^int(keys[0],16),'x')

    return cipher

def cfb_enc(msg,IV,t,sypher004):
    x = IV
    cipher = []
    for m in msg:
        c = int(m,16) ^ int(bin(int(sypher004(x,4),16))[:t],2) # msb from x
        cipher.append(format(c,'x'))
        x = "{:04x}".format(((int(x,16) << t) | c) & 255,'x')
    return "".join(cipher)

def cfb_dec(cipher,IV,t,sypher004):
    x = IV
    msg = []
    for c in cipher:
        m = int(c,16) ^ int(bin(int(sypher004(x,4),16))[:t],2) # msb from x
        msg.append(format(m,'x'))
        x = "{:04x}".format(((int(x,16) << t) ^ int(c,16)) % 255,'x')
    return "".join(msg)

# For OFB, encryption is same as decryption, since keystream xor m = c.
def ofb_enc(msg,IV,t,sypher004):
    x = IV
    cipher = []
    for m in msg:
        x = sypher004(x,4)
        c = int(m,16) ^ int(bin(int(x,16))[:t],2) # msb from x
        cipher.append(format(c,'x'))
    return "".join(cipher)

def cipher_mode(IV,msg,mode_enc,mode_dec,mode,sypher004):
    c1 = mode_enc(msg,IV,4,sypher004)
    print("IV used:",IV)
    print("Encryption of msg:",msg,", using Sypher004 -",mode,":", c1)
    print("".join("{:04b}".format(int(c,16)) for c in c1))
    print("Flipping 6th bit from the right:")
    c1 = format(int(c1,16) ^ 32,'x')
    print("".join("{:04b}".format(int(c,16)) for c in c1))
    print("Decryption of modified cipher: ")
    c1 = mode_dec(c1,IV,4,sypher004)
    print("".join("{:04b}".format(int(c,16)) for c in c1),"<-",c1)
    print("".join("{:04b}".format(int(m,16)) for m in msg),"<- Original message")
    print()

IV = input("Enter IV: ")
if len(IV) < 4:
    exit("IV should be minimum of 16 bits")
elif len(IV) > 4:
    IV = IV[-4:]

msg = input("Enter message (multiple of 16 bits): ")
if len(msg) % 4 != 0:
    exit("Message length not a multiple of 16 bits!!")

print()
print("Using Sypher004 encryption:")
print("-" * 28)

print("Mode: CFB")
cipher_mode(IV,msg,cfb_enc,cfb_dec,'CFB',sypher004)

print("Mode: OFB")
cipher_mode(IV,msg,ofb_enc,ofb_enc,'OFB',sypher004)

print("Using Sypher004 decryption:")
print("-" * 28)

print("Mode: CFB")
cipher_mode(IV,msg,cfb_enc,cfb_dec,'CFB',sypher004_inv)

print("Mode: OFB")
cipher_mode(IV,msg,ofb_enc,ofb_enc,'OFB',sypher004_inv)
import numpy as np
import AES # imports from AES.py

def makeIntegral(r,c): # creates an integral 3D list
    integral_state = np.arange(16*256,dtype=object).reshape(256,4,4)
    random = np.random.randint(0,256,16)

    for i in range(256):
        l = 0
        for j in range(4):
            for k in range(4):
                if j == r + 1 and k == c + 1:
                    integral_state[i][j - 1][k - 1] = "{:02x}".format(i,'x')
# filling other bytes with random constants, same for all 256 states
                else:
                    integral_state[i][j - 1][k - 1] = "{:02x}".format(random[l],'x')
                    l += 1
    return integral_state

def isAll(a): # prints 2D list with All bytes marked
    isAllList = np.empty([4,4],dtype=str)
    for j in range(4):
        for k in range(4):
            isAllFlag = True
            n = [i for i in range(256)]
            for i in range(256):
                if int(a[i][j][k],16) not in n:
                    isAllFlag = False
                else:
                    n[int(a[i][j][k],16)] = -1
                    isAllFlag = True
            
            if isAllFlag == True:
                isAllList[j][k] = 'A'
            else:
                isAllList[j][k] = ''

    return isAllList

def isConst(a): # prints 2D list with Constant bytes marked
    isConstList = np.empty([4,4],dtype=str)
    for j in range(4):
        for k in range(4):
            isConstFlag = True
            for i in range(256):
                # checks if all bytes are same
                if a[i][j][k] != a[0][j][k]:
                    isConstFlag = False
                else:
                    isConstFlag = True
            
            if isConstFlag == True:
                isConstList[j][k] = 'C'
            else:
                isConstList[j][k] = ''

    return isConstList

def isBalanced(a): # prints 2D list with Balanced bytes marked
    isBalancedList = np.empty([4,4],dtype=str)
    for j in range(4):
        for k in range(4):
            isBalancedFlag = 0
            for i in range(256):
                isBalancedFlag = isBalancedFlag ^ int(a[i][j][k],16)
            
            if isBalancedFlag == 0:
                isBalancedList[j][k] = 'B'
            else:
                isBalancedList[j][k] = ''

    return isBalancedList

r = int(input("Enter row for All byte: "),10)
c = int(input("Enter column for All byte: "),10)

integral_state = makeIntegral(r,c) # choosing which byte to make All
seed = input("Enter key:") # choosing key for key schedule
keyset = AES.keySchedule(seed, 3)
AES_func = [AES.subBytes, AES.shiftRows, AES.mixColumns, AES.addKey]

print("Round 0 AddKey:")
for i in integral_state:
    i = AES_func[3](i, keyset[0])
print(np.core.defchararray.add(isConst(integral_state),isAll(integral_state)))

# 3-round integral distinguisher
for j in range(3):
    print("Round",j + 1,":")
    for k in range(4):
        for i in range(len(integral_state)):
            # print("Round:",i)
            if k == 3:
                integral_state[i] = AES_func[k](integral_state[i], keyset[j + 1])
            else:
                integral_state[i] = AES_func[k](integral_state[i])

        print("After",AES_func[k].__name__,":")
        temp = np.core.defchararray.add(isConst(integral_state),isAll(integral_state))

        if '' in temp:
            print(isBalanced(integral_state))
        else:
            print(temp)
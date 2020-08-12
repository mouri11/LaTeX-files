# please run the code more than once to generate the collision

import string
import random
import hashlib
import os

def random_string(n): # to generate random string having letters and digits
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k = n))

def hash_list(n,t): # to create a list of string and its hash
    ctr = 0
    str_hash = []
    for i in range(2 ** 16):
        str1 = random_string(n)
        hash1 = hashlib.md5(str1.encode()).hexdigest()
        list1 = []
        list1.append(str1)
        list1.append(hash1)
        str_hash.append(list1)
    return str_hash

def find_collision(n,t): # looking for collision in hash_list
    str_hash = hash_list(n,t)

    str_hash.sort(key = lambda x: x[1])

    file1 = open('string1.txt','w')
    file2 = open('string2.txt','w')

    for i in range(len(str_hash) - 1):
        if str_hash[i][1][:4] == str_hash[i + 1][1][:4] and str_hash[i][1][-4:] == str_hash[i + 1][1][-4:]:
            print(str_hash[i][0],str_hash[i][1])
            file1.write(str_hash[i][0])

            print(str_hash[i + 1][0],str_hash[i + 1][1])
            file2.write(str_hash[i + 1][0])
    file1.close()
    file2.close()

find_collision(100,4)
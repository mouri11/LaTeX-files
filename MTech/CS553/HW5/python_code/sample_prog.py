perm = []
for x in range(2 ** 16):
    strx = "{:04x}".format(x,'x')
    # if strx not in perm:
    #     perm.append(strx)
    xored = "{:04x}".format(int(strx,16)^int('8000',16),'x')
        # if xored not in perm:
            #perm.append(xored)
    print(strx,xored)
# print(perm)

# with open("./output_cnfrm.txt") as file:
#     for i,l in enumerate(file):
#         pass
# print(i + 1)
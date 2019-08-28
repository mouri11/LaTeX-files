def E_gcd(a,b): # function to calculate Euclidean GCD
    a,b = (b,a) if a < b else (a,b) # swaps a and b if a < b
    while True:
        r = a % b
        if (r == 0):
            break
        a = b
        b = r
    return b


try: # to allow only integer input
    a,b = [int(i)for i in(input("Enter two integers: ").split(" "))]
except ValueError:
    print("Please enter two integers!")
    exit(0)

print(E_gcd(a,b))
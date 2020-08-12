from time import time

def compare_mac(x, y, n):
    for i in range(n):
        if x[i] != y[i]:
            return False
    return True

def const_compare_mac(x,y,n):
    result = 0
    for i in range(n):
        result |= ord(x[i]) ^ ord(y[i])
    return result

def timing_measure(mac1,mac2,trials,compare_mac):
    # each call checks the whole string 
    print("Using ",compare_mac.__name__,":")
    start = time()
    for i in range(trials):
        compare_mac(mac1,mac1,len(mac1))
    end = time()
    print('For same string: %0.5fs' % (end - start))

    # each call checks only till mismatch appears    
    start = time()
    for i in range(trials):
        compare_mac(mac1,mac2,len(mac1))
    end = time()
    print('For different string: %0.5fs' % (end - start))

timing_measure('0123456789abcdef','01X3456789abcdef',100000,compare_mac)
timing_measure('0123456789abcdef','01X3456789abcdef',100000,const_compare_mac)
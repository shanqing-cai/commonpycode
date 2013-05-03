#!/usr/bin/python

import sys

# if __name__ == "__main__":
def radix_inc(val, base, inc=1):
    # base = int(sys.argv[1])
    # val = [0, 0, 255] # From most significant to least significant
    # inc = 255

    # === Input sanity check ===
    if base < 0:
        raise Exception, "Base must be > 0"

    N = len(val)
    if N == 0:
        raise Exception, "Input number is empty"

    for i0 in range(N):
        if val[i0] >= base or val[i0] < 0:
            raise Exception, "Invalid input"
    
    # === Do the increment ===
    for k in range(inc):
        val[N - 1] += 1
        for i0 in range(N):        
            if val[N - 1 - i0] == base:
                val[N - 1 - i0] = 0
                if i0 < N - 1:
                    val[N - 2 - i0] += 1
            else:
                break

    return val

    # print(val)

    
    

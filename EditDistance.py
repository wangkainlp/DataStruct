#codinf:uft-8
import sys
import numpy as np

def editDistance(str1, str2):
    lenStr1 = len(str1)
    lenStr2 = len(str2)
    if lenStr1 == 0:
        return lenStr2
    if lenStr2 == 0:
        return lenStr1

    M = lenStr1 + 1
    N = lenStr2 + 1
    d = np.zeros((M, N), dtype=int)

    print d.shape

    for i in range(0, N):
        d[0][i] = i
    for i in range(0, M):
        d[i][0] = i
        
    for j in range(1, N):
        for i in range(1, M):
            tmp = 0 if str1[i - 1] == str2[j - 1] else 1
            d[i][j] = min(d[i-1][j] + 1,        # deletion
                          d[i][j-1] + 1,        # insertion
                          d[i-1][j-1] + tmp)    # substitution

    print d
    print 1 - 1.0 * d[M-1][N-1] / max(lenStr1, lenStr2)
    return d[M-1][N-1]


if __name__ == "__main__":

    str1 = "abcdefg"
    str2 = "1"
    # str2 = "1234567"
    
    print editDistance(str1, str2);

# vim : cc=50 :

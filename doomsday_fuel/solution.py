from fractions import Fraction
from fractions import gcd

def num_of_transients(m):
    if len(m) == 0:
        raise Exception("Can't get transient states of empty matrix")

    for r in range(len(m)):
        for c in range(len(m[r])):
            if m[r][c] != 0:
                # this is not an all-zero row, try next one
                break
        else:
            # has just finished looping over an empty row (i.e. w/o `break`)
            return r
    # reached end of table and didn't encounter all-zero row - no absorbing states
    raise Exception("Not a valid AMC matrix: no absorbing (terminal) states")


# decompose input matrix `m` on Q (t-by-t) and R (t-by-r) components
# `t` is the number of transient states
def decompose(m):
    t = num_of_transients(m)
    if t == 0:
        raise Exception("No transient states. At least initial state is needed.")

    Q = []
    for r in range(t):
        qRow = []
        for c in range(t):
            qRow.append(m[r][c])
        Q.append(qRow)
    if Q == []:
        raise Exception("Not a valid AMC matrix: no transient states")

    R = []
    for r in range(t):
        rRow = []
        for c in range(t, len(m[r])):
            rRow.append(m[r][c])
        R.append(rRow)
    if R == []:
        raise Exception("Not a valid AMC matrix: missing absorbing states")
    return Q, R

# return Identity matrix of size `t`
def identity(t):
    m = []
    for i in range(t):
        r = []
        for j in range(t):
            r.append(int(i == j))
        m.append(r)
    return m

# swap i,j rows/columns of a square matrix `m`
def swap(m, i, j):
    n = []
    s = len(m)

    if s != len(m[0]):
        raise Exception("Cannot swap non-square matrix")

    if i == j:
        # no need to swap
        return m

    for r in range(s):
        nRow = []
        tmpRow = m[r]
        if r == i:
            tmpRow = m[j]
        if r == j:
            tmpRow = m[i]
        for c in range(s):
            tmpEl = tmpRow[c]
            if c == i:
                tmpEl = tmpRow[j]
            if c == j:
                tmpEl = tmpRow[i]
            nRow.append(tmpEl)
        n.append(nRow)
    return n

# reorganize matrix so zero-rows go last (preserving zero rows order)
def sort(m):
    size = len(m)

    zero_row = -1
    for r in range(size):
        sum = 0
        for c in range(size):
            sum += m[r][c]
        if sum == 0:
            # we have found all-zero row, remember it
            zero_row = r
        if sum != 0 and zero_row > -1:
            # we have found non-zero row after all-zero row - swap these rows
            n = swap(m, r, zero_row)
            # and repeat from the begining
            return sort(n)
    #nothing to sort, return
    return m

# normalize matrix `m`
def normalize(m, use_fractions=False ):
    n = []
    for r in range(len(m)):
        sum = 0
        cols = len(m[r])
        for c in range(cols):
            sum += m[r][c]

        nRow = []

        if sum == 0:
            # all-zero row
            nRow = m[r]
        else:
            for c in range(cols):
                # FIXME it's strange but python 2.7 does not automatically convert decimals to floats
                if use_fractions:
                    nRow.append(Fraction(m[r][c], sum))
                else:
                    nRow.append(float(m[r][c])/sum)
        n.append(nRow)
    return n

# subtract two matrices
def subtract(i, q):
    if len(i) != len(i[0]) or len(q) != len(q[0]):
        raise Exception("non-square matrices")

    if len(i) != len(q) or len(i[0]) != len(q[0]):
        raise Exception("Cannot subtract matrices of different sizes")

    s = []
    for r in range(len(i)):
        sRow = []
        for c in range(len(i[r])):
            sRow.append(i[r][c] - q[r][c])
        s.append(sRow)
    return s

# multiply two matrices
def multiply(a, b):
    if a == [] or b == []:
        raise Exception("Cannot multiply empty matrices")

    if len(a[0]) != len(b):
        raise Exception("Cannot multiply matrices of incompatible sizes")

    m = []
    rows = len(a)
    cols = len(b[0])
    iters = len(a[0])

    for r in range(rows):
        mRow = []
        for c in range(cols):
            sum = 0
            for i in range(iters):
                sum += a[r][i]*b[i][c]
            mRow.append(sum)
        m.append(mRow)
    return m

# transpose matrix
def transposeMatrix(m):
    t = []
    for r in range(len(m)):
        tRow = []
        for c in range(len(m[r])):
            if c == r:
                tRow.append(m[r][c])
            else:
                tRow.append(m[c][r])
        t.append(tRow)
    return t

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

# matrix determinant
def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    d = 0
    for c in range(len(m)):
        d += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))

    return d

# matrix inversion
def getMatrixInverse(m):
    d = getMatrixDeternminant(m)

    if d == 0:
        raise Exception("Cannot get inverse of matrix with zero determinant")

    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/d, -1*m[0][1]/d],
                [-1*m[1][0]/d, m[0][0]/d]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/d
    return cofactors

# lowest common multiple of list of fractions
def lcm(args):
    args = list(map(lambda x: x.denominator, args))
    lcm = args[0]
    for i in args[1:]:
        lcm = lcm * i / gcd(lcm, i)
    return lcm

def answer(m):
    # B = (I - Q)^-1 * R

    m = sort(m)
    t = num_of_transients(m)
    if t == 0:
        return [1,1]
    m = normalize(m, use_fractions=True)
    Q, R = decompose(m)[0], decompose(m)[1]
    I = identity(t)
    F = getMatrixInverse(subtract(I,Q))
    B = multiply(F, R)
    z = lcm(B[0])

    output = [a.numerator * z / a.denominator for a in B[0]]
    output.append(z)

    return output

# TEST 1
m1 = [
    [0, 2, 1, 0, 0],
    [0, 0, 0, 3, 4],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
#a = [7, 6, 8, 21]
 
# TEST 2
m2 = [
    [0, 1, 0, 0, 0, 1],
    [4, 0, 0, 3, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]
#a = [0, 3, 2, 9, 14]
 
# TEST 3
m3 = [
    [1, 2, 3, 0, 0, 0],
    [4, 5, 6, 0, 0, 0],
    [7, 8, 9, 1, 0, 0],
    [0, 0, 0, 0, 1, 2],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]
#a = [1, 2, 3]
 
#TEST 4
m4 = [[0]]
#a = [1, 1]
 
# TEST 5
m5 = [
    [0, 0, 12, 0, 15, 0, 0, 0, 1, 8],
    [0, 0, 60, 0, 0, 7, 13, 0, 0, 0],
    [0, 15, 0, 8, 7, 0, 0, 1, 9, 0],
    [23, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [37, 35, 0, 0, 0, 0, 3, 21, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
#a = [1, 2, 3, 4, 5, 15]
 
# TEST 6
m6 = [
    [ 0,  7,  0, 17,  0,  1,  0,  5,  0,  2],
    [ 0,  0, 29,  0, 28,  0,  3,  0, 16,  0],
    [ 0,  3,  0,  0,  0,  1,  0,  0,  0,  0],
    [48,  0,  3,  0,  0,  0, 17,  0,  0,  0],
    [ 0,  6,  0,  0,  0,  1,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
]
#a = [4, 5, 5, 4, 2, 20]
 
# TEST 7
m7 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
#a = [1, 1, 1, 1, 1, 5]
 
# TEST 8
m8 = [
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
#a = [2, 1, 1, 1, 1, 6]
 
# TEST 9
m9 = [
    [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
    [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
    [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
#a = [6, 44, 4, 11, 22, 13, 100]
 
# TEST 10
m10 = [
    [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
    [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
    [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
    [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
#a = [1, 1, 1, 2, 5]

# print answer(m1)
# print answer(m2)
# print answer(m3)
# print answer(m4)
# print answer(m5)
# print answer(m6)
# print answer(m7)
# print answer(m8)
# print answer(m9)
# print answer(m10)

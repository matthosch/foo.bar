def answer(n):
    n = int(n)

    # define lookup table
    lookup_table = { 1: 0, 2: 1 }

    def calculate_steps(n):
        # return memoized value in lookup table
        if n in lookup_table:
            return lookup_table[n]

        # handle safety control limitations (optimized)
        if n & 1:
            # odd numbers have an extra operation due to constraint
            lookup_table[n] = min(calculate_steps((n + 1) >> 1) + 2,
                                  calculate_steps((n - 1) >> 1) + 2)
        else:
            # even numbers add a single operation
            lookup_table[n] = calculate_steps(n >> 1) + 1

        return lookup_table[n]

    # calculate number of steps
    return calculate_steps(n)

def test_case_1():
    n = '4'
    assert answer(n) == 2

def test_case_2():
    n = '15'
    assert answer(n) == 5


##############################################################

from operator import add, sub

def min_operations(n): 
    n = int(n)
    def operation(n, count, operator):
        # Use temp list to store passed in n, count values
        temp = [operator(n, 1), count]
        # Increment count value while n is even
        while temp[0] % 2 == 0:
            temp[0] = temp[0] // 2
            temp[1] += 1
        return temp

    count = 0
    while (n > 1) :
        # If n is even, divide by 2
        if (n % 2 == 0): 
            n //= 2 
        else:
            # Comparing the output of each operation, we want
            # to return temp list based on minimum n value
            n, count = min(
                operation(n, count, sub),
                operation(n, count, add)
            )
        count += 1

    return count 
  
def test_case_3():
    n = '4'
    assert min_operations(n) == 2

def test_case_4():
    n = '15'
    assert min_operations(n) == 5
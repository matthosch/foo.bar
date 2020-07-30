def answer(l, t):
    # Store key values in dictionary with sum:index
    dict = {}
    # Initialize with 0: -1 in case sublist starts from index 0
    dict[0] = -1
    sum = 0
    # traverse the given list
    for i in range(len(l)):
        # sum of elements so far
        sum += l[i]
        # If the sum hasn't been recorded, add to dict
        if sum not in dict:
            dict[sum] = i
        # If sum - t exists in dict, we've found a valid solution
        if sum - t in dict:
            # Subtract index of sum - t
            length = i - dict[sum - t]
            return [i - length + 1, i]
    # No valid values found
    return [-1, -1]

def test_case_1():
    assert answer([4, 3, 5, 7, 8], 12) == [0, 2]

def test_case_2():
    assert answer([4, 3, 10, 2, 8], 12) == [2, 3]

def test_case_3():
    assert answer([1, 2, 3, 4], 15) == [-1, -1] 
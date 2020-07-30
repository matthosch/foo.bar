def answer(data, n):
	return list(filter(lambda x: data.count(x) <= n, data))
	
def test_case_1():
    assert answer([1, 2, 3], 0) == []

def test_case_2():
    assert answer([1, 2, 2, 3, 3, 3, 4, 5, 5], 1) == [1, 4]

def test_case_3():
    assert answer([1, 2, 3], 6) == [1, 2, 3]
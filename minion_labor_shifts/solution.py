def answer(data, n):
	return list(filter(lambda x: data.count(x) <= n, data))
	
print(answer([5, 10, 15, 10, 7], 1))
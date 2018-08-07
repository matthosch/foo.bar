def answer(l, t):
	output = [-1, -1]
	for x in range(len(l)):
		for y in range(len(l)):
			if sum(l[x:y+1]) == t:
				return [x, y]
			#print(x, y, sum(l[x:y+1]))
	return output
	
print answer([4, 3, 5, 7, 8], 12) #expect [0, 2]
print answer([4, 3, 10, 2, 8], 12) #expect [2, 3]
print answer([1, 2, 3, 4], 15) #expect [-1, -1]


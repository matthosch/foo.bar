class Solution:
	def __init__(self, n, b):
		self.n = n
		self.b = b
		self.c = []

	def conver(self, num, base):
			a = 0
			i = 0
			while num:
				num,r = divmod(num, base)
				a += 10**i * r
				i += 1
			return a

	def repeated(self, input_list):
			return len([item for item in list(set(input_list)) if input_list.count(item) > 1])

	def answer(self, c = []):
		k = len(self.n)
		x = int("".join(sorted(self.n, reverse=True)), self.b)
		y = int("".join(sorted(self.n)), self.b)
		z = str(self.conver(x - y, self.b)).zfill(k)
		self.c.append(z)
		if len(self.c) < 50:
			self.n = z
			self.answer(self.c)
		return self.repeated(self.c)

def answer(n, b):
	return Solution(n, b).answer()
	

print answer("1211", 10)
print answer("210022", 3)
print answer("252525", 7)


# Test 1: 1
# Test 2: 3
# Test 3: 6
# Test 4: 4
# Test 5: 14
# Test 6: 1
# Test 7: 5
# Test 8: 3
# Test 9: 1
# Test 10: 2
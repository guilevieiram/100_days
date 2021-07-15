def add(nums):
	return sum(nums)

def multiply(nums):
	result = 1
	for num in nums:
		result *= num
	return result

class Calculator():
	def __init__(self, *args, **kwargs):
		self.__dict__.update(kwargs)
		self.numbers = args

	def calculate(self):
		return self.operation(self.numbers)

c = Calculator(1, 2 ,  27,5 , operation=multiply)
print(c.calculate())
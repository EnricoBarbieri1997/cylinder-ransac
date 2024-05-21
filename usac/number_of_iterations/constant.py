from usac.number_of_iterations.strategy import NumberOfIterationsStrategy


class ConstantNumberOfIterations(NumberOfIterationsStrategy):
	def __init__(self, number_of_iterations = 1000):
		self._number_of_iterations = number_of_iterations
	def number_of_iterations(self, data):
		return self._number_of_iterations
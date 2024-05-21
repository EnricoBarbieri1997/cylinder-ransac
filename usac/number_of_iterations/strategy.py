from abc import ABC, abstractmethod

class NumberOfIterationsStrategy(ABC):
	@abstractmethod
	def number_of_iterations(self, data):
		pass
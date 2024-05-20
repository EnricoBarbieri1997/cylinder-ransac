from abc import ABC, abstractmethod

class SamplingStrategy(ABC):
	@abstractmethod
	def sampling(self, data):
		pass
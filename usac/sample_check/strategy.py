from abc import ABC, abstractmethod

class SampleCheckStrategy(ABC):
	@abstractmethod
	def sample_check(self, sample):
		pass
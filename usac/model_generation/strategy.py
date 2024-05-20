from abc import ABC, abstractmethod

class ModelGenerationStrategy(ABC):
	@abstractmethod
	def model_generation(self, sample):
		pass
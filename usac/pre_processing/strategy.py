from abc import ABC, abstractmethod

class PreProcessingStrategy(ABC):
	@abstractmethod
	def pre_process(self, data):
		pass
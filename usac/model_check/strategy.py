from abc import ABC, abstractmethod

class ModelCheckStrategy(ABC):
	@abstractmethod
	def model_check(self, model):
		pass
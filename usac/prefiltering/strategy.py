from abc import ABC, abstractmethod

class PrefilteringStrategy(ABC):
	@abstractmethod
	def prefiltering(self, data):
		pass
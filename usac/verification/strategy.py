from abc import ABC, abstractmethod

class VerificationStrategy(ABC):
	@abstractmethod
	def verification(self, model, data):
		pass
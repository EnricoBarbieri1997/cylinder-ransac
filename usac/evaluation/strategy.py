from abc import ABC, abstractmethod

class EvaluationStrategy(ABC):
	@abstractmethod
	def evaluate_model(self, model, inliers):
		pass
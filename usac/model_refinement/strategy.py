from abc import ABC, abstractmethod

class ModelRefinementStrategy(ABC):
	@abstractmethod
	def model_refinement(self, model, inliers):
		pass
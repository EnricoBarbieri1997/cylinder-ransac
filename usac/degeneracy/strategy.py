from abc import ABC, abstractmethod

class DegeneracyStrategy(ABC):
	@abstractmethod
	def degeneracy(self, inliers):
		pass
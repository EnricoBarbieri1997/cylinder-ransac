
from usac.degeneracy.strategy import DegeneracyStrategy

class AllPassDegeneracy(DegeneracyStrategy):
	def degeneracy(self, inliers):
		return False
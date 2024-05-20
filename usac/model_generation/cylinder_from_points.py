import numpy as np
from usac.model_generation.strategy import ModelGenerationStrategy

class CylinderFromPointsModelGeneration(ModelGenerationStrategy):
	def model_generation(self, sample):
		coefficients_matrix = []
		for point in sample:
			x, y, z = point
			coefficients_matrix.append([x^2, y^2, z^2, x*y, x*z, y*z, x, y, z, 1])
		coefficients_matrix = np.array(coefficients_matrix)
		known_terms = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])

		return np.linalg.solve(coefficients_matrix, known_terms)
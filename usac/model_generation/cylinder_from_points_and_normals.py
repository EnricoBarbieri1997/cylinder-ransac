import numpy as np
from usac.model_generation.strategy import ModelGenerationStrategy
from utils.geometry import cylinder_from_center_radius_axis, rotation_between

# https://github.com/CloudCompare/CloudCompare/issues/1237
class CylinderFromPointsWithNormalsModelGeneration(ModelGenerationStrategy):
	def model_generation(self, sample):
		x1, y1, z1, a1, b1, c1 = sample[0]
		p1 = [x1, y1, z1]
		n1 = [a1, b1, c1]
		x2, y2, z2, a2, b2, c2 = sample[1]
		p2 = [x2, y2, z2]
		n2 = [a2, b2, c2]

		orthogonal_direction = np.cross(n1, n2)
		# projection_plane = np.array([orthogonal_direction[0], orthogonal_direction[1], orthogonal_direction[3], np.dot(orthogonal_direction, [0, 0, 0])])
		
		projected_position_1 = p1 - (np.dot(p1, orthogonal_direction)) * orthogonal_direction
		projected_normal_1 = n1 - (np.dot(n1, orthogonal_direction)) * orthogonal_direction
		projected_position_2 = p2 - (np.dot(p2, orthogonal_direction)) * orthogonal_direction
		projected_normal_2 = n2 - (np.dot(n2, orthogonal_direction)) * orthogonal_direction

		# plane1 = np.array([a1, b1, c1, np.dot([a1, b1, c1], [x1, y1, z1])])
		# plane2 = np.array([a2, b2, c2, np.dot([a2, b2, c2], [x2, y2, z2])])

		# alpha * n1x - betha * n2x = p2x - p1x
		# alpha * n1y - betha * n2y= p2y - py1

		coefficients_matrix = [
			[projected_normal_1[0], -projected_normal_2[0]],
			[projected_normal_1[1], -projected_normal_2[1]]
		]
		coefficients_matrix = np.array(coefficients_matrix)
		known_terms = np.array([
			projected_position_2[0] - projected_position_1[0],
			projected_position_2[1] - projected_position_1[1]
		])

		alpha, betha = np.linalg.solve(coefficients_matrix, known_terms)
		center = projected_position_1 + alpha * projected_normal_1
		radius = np.linalg.norm(projected_position_1 - center)

		return cylinder_from_center_radius_axis(center, radius, orthogonal_direction)
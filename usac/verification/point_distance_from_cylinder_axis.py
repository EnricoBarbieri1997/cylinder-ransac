import numpy as np

class PointDistanceFromCylinderAxisVerification():
	def verification(self, model, data):
		center, radius, axis = model
		inliers = []
		for point in data:
			dist_pt = np.cross(axis, (center - point))
			dist_pt = np.linalg.norm(dist_pt)
			if abs(dist_pt - radius) < 0.1:
				inliers.append(point)
		return inliers
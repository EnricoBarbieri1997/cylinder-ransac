import numpy as np

from utils.geometry import point_to_line_distance

class PointDistanceFromCylinderAxisVerification():
	def verification(self, model, data):
		center, radius, axis = model
		inliers = []
		for point in data:
			dist_pt = point_to_line_distance(point, center, axis)
			if abs(dist_pt - radius) < 0.1:
				inliers.append(point)
		return inliers
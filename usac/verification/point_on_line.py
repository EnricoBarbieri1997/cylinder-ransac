class PointOnLineVerification():
	def verification(self, model, data):
		m, q = model
		inliers = []
		for point in data:
			x, y = point
			if abs(m * x + q - y) < 1e-1:
				inliers.append(point)
		return inliers
class PointOnCylinderVerification():
	def verification(self, model, data):
		A, B, C, D, E, F, G, H, I = model
		inliers = []
		for point in data:
			x, y, z = point
			if abs(
				A * x**2 + B * y**2 + C * z**2 + D * x * y + E * x * z + F * y * z + G * x + H * y + I * z + 1
			) < 1e-1:
				inliers.append(point)
		return inliers
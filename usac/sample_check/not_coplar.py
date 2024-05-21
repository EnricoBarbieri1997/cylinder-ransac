import numpy as np
from usac.sample_check.strategy import SampleCheckStrategy

class NotCoplanarSampleCheck(SampleCheckStrategy):
	def __init__(self, threshold=1e-2, accepted_coplanar_points=0):
		self.threshold = threshold
		self.accepted_coplanar_points = accepted_coplanar_points
	def sample_check(self, sample):
		if len(sample) < 4:
			return True
		p1, p2, p3 = sample[:3]
		normal = np.cross(p2 - p1, p3 - p1)
		coplanar_points = 0
		for i in range(3, len(sample)):
			if np.abs(np.dot(normal, sample[i] - p1)) < self.threshold:
				coplanar_points += 1

		return coplanar_points <= self.accepted_coplanar_points
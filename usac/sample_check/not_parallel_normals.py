import numpy as np
from usac.sample_check.strategy import SampleCheckStrategy

class NotParallelNormalsSampleCheck(SampleCheckStrategy):
	def __init__(self, threshold=1e-2):
		self.threshold = threshold
	def sample_check(self, sample):
		if len(sample) < 2:
			return True
		normals_starting_index = len(sample[0]) // 2

		for i in range(len(sample)):
			for j in range(i + 1, len(sample)):
				p1, p2 = sample[i], sample[j]
				n1 = p1[normals_starting_index:]
				n1 = n1 / np.linalg.norm(n1)
				n2 = p2[normals_starting_index:]
				n2 = n2 / np.linalg.norm(n2)
				if np.abs(np.dot(n1, n2)) > self.threshold:
					return False

		return True
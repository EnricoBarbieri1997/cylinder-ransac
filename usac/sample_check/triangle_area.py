import numpy as np
from usac.sample_check.strategy import SampleCheckStrategy

class TriangleAreaSampleCheck(SampleCheckStrategy):
	def __init__(self, threshold=10e-14):
		self.threshold = threshold
	def sample_check(self, sample):
		p1 = sample[0]
		p2 = sample[1]
		p3 = sample[2]
		# triangle "edges"
		t = p2-p1
		u = p3-p1
		v = p3-p2

		# triangle normal
		w = np.cross(t, u)
		wsl = np.dot(w, w)
		if (wsl<self.threshold):
			return False
		return True
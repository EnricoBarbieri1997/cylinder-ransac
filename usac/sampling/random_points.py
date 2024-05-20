import numpy as np
from usac.sampling.strategy import SamplingStrategy

class RandomPointsSampling(SamplingStrategy):
	def __init__(self, number_of_points = 2):
		self.number_of_points = number_of_points
	def sampling(self, data):
		return data[np.random.choice(len(data), size=self.number_of_points, replace=False)]
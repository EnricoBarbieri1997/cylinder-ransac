import numpy as np
from usac.pre_processing.strategy import PreProcessingStrategy

class NormalizePointCoordinatesPreProcessing(PreProcessingStrategy):
	def pre_process(self, data):
		max_distance = max(np.linalg.norm(data, axis=1))
		return data / max_distance, max_distance
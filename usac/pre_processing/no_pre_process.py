from usac.pre_processing.strategy import PreProcessingStrategy

class NoPreProcessingPreprocessing(PreProcessingStrategy):
	def pre_process(self, data):
		return data, None
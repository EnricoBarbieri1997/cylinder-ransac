from usac.post_processing.strategy import PostProcessingStrategy

class NoPostProcessingPreprocessing(PostProcessingStrategy):
	def post_process(self, model, inliers, pre_process_output):
		return model, inliers
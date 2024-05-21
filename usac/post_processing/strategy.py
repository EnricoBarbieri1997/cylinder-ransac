from abc import ABC, abstractmethod

class PostProcessingStrategy(ABC):
	@abstractmethod
	def post_process(self, model, inliers, pre_process_output):
		pass
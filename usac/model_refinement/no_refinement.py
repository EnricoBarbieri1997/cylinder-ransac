from usac.model_refinement.strategy import ModelRefinementStrategy

class NoRefinementModelRefinement(ModelRefinementStrategy):
	def model_refinement(self, model, inliers):
		return model
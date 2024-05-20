from usac.model_check.strategy import ModelCheckStrategy

class AllPassModelCheck(ModelCheckStrategy):
	def model_check(self, model):
		return True
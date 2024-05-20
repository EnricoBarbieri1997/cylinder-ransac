from usac.prefiltering.strategy import PrefilteringStrategy


class AllPassPrefiltering(PrefilteringStrategy):
	def prefiltering(self, data):
		return data
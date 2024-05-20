from usac.sample_check.strategy import SampleCheckStrategy

class AllPassSampleCheck(SampleCheckStrategy):
	def sample_check(self, sample):
		return True
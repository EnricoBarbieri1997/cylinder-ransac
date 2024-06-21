from usac.model_generation.strategy import ModelGenerationStrategy

class LineFromPointsModelGeneration(ModelGenerationStrategy):
	def model_generation(self, sample):
		x1, y1 = sample[0]
		x2, y2 = sample[1]
		slope = (y2 - y1) / (x2 - x1)

		# Calculate the offset
		intercept = y1 - (x1 * slope)

		return [slope, intercept]
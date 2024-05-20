import numpy as np
from typing import TypedDict

from usac.degeneracy.all_pass import AllPassDegeneracy
from usac.degeneracy.strategy import DegeneracyStrategy
from usac.evaluation.count import CountEvaluation
from usac.evaluation.strategy import EvaluationStrategy
from usac.model_check.all_pass import AllPassModelCheck
from usac.model_check.strategy import ModelCheckStrategy
from usac.model_generation.cylinder_from_points import CylinderFromPointsModelGeneration
from usac.model_generation.line_from_points import LineFromPointsModelGeneration
from usac.model_generation.strategy import ModelGenerationStrategy
from usac.model_refinement.no_refinement import NoRefinementModelRefinement
from usac.model_refinement.strategy import ModelRefinementStrategy
from usac.prefiltering.all_pass import AllPassPrefiltering
from usac.prefiltering.strategy import PrefilteringStrategy
from usac.sample_check.all_pass import AllPassSampleCheck
from usac.sample_check.strategy import SampleCheckStrategy
from usac.sampling.random_points import RandomPointsSampling
from usac.sampling.strategy import SamplingStrategy
from usac.verification.point_on_cylinder import PointOnCylinderVerification
from usac.verification.point_on_line import PointOnLineVerification
from usac.verification.strategy import VerificationStrategy

class USACStepsDefinitionRequired(TypedDict):
	sampling_strategy: SamplingStrategy
	model_generation_strategy: ModelGenerationStrategy
	verification_strategy: VerificationStrategy

class USACStepsDefinition(USACStepsDefinitionRequired, total = False):
	prefiltering_strategy: PrefilteringStrategy
	sample_check_strategy: SampleCheckStrategy
	model_check_strategy: ModelCheckStrategy
	degeneracy_strategy: DegeneracyStrategy
	evaluation_strategy: EvaluationStrategy
	model_refinement_strategy: ModelRefinementStrategy
	num_iterations: int

class USAC:
	def __init__(self, steps: USACStepsDefinition):
		self.prefiltering_strategy = steps.get('prefiltering_strategy', AllPassPrefiltering())
		self.sampling_strategy = steps.get('sampling_strategy')
		if (self.sampling_strategy is None):
			raise ValueError('Sampling strategy is required')
		self.sample_check_strategy = steps.get('sample_check_strategy', AllPassSampleCheck())
		self.model_generation_strategy = steps.get('model_generation_strategy')
		if (self.model_generation_strategy is None):
			raise ValueError('Model generation strategy is required')
		self.model_check_strategy = steps.get('model_check_strategy', AllPassModelCheck())
		self.verification_strategy = steps.get('verification_strategy')
		if (self.verification_strategy is None):
			raise ValueError('Verification strategy is required')
		self.degeneracy_strategy = steps.get('degeneracy_strategy', AllPassDegeneracy())
		self.evaluation_strategy = steps.get('evaluation_strategy', CountEvaluation())
		self.model_refinement_strategy = steps.get('model_refinement_strategy', NoRefinementModelRefinement())
		self.num_iterations = steps.get('num_iterations', 1000)

	def run(self, data):
		# Step 1: Prefiltering
		filtered_data = self.prefiltering_strategy.prefiltering(data)
		
		# Initialize variables to track the best model
		best_model = None
		best_inliers = []
		best_score = float('-inf')
		
		for _ in range(self.num_iterations):
			# Step 2: Sampling
			sample = self.sampling_strategy.sampling(filtered_data)
			
			# Step 3: Sample Check
			if not self.sample_check_strategy.sample_check(sample):
				continue
			
			# Step 4: Model Generation
			model = self.model_generation_strategy.model_generation(sample)
			
			# Step 5: Model Check
			if not self.model_check_strategy.model_check(model):
				continue
			
			# Step 6: Verification
			inliers = self.verification_strategy.verification(model, filtered_data)
			score = self.evaluation_strategy.evaluate_model(model, inliers)
			
			# Step 7: Degeneracy
			if self.degeneracy_strategy.degeneracy(inliers):
				continue
			
			# Update the best model if the current one is better
			if score > best_score:
				best_score = score
				best_model = model
				best_inliers = inliers
		
		# Step 8: Model Refinement
		if best_model is not None:
			best_model = self.model_refinement_strategy.model_refinement(best_model, best_inliers)
		
		return best_model, best_inliers

class USACBuilder:
	def __init__(self):
		self.steps: USACStepsDefinition = {}

	def with_prefiltering_strategy(self, prefiltering_strategy: PrefilteringStrategy):
		self.steps['prefiltering_strategy'] = prefiltering_strategy
		return self

	def with_sampling_strategy(self, sampling_strategy: SamplingStrategy):
		self.steps['sampling_strategy'] = sampling_strategy
		return self

	def with_sample_check_strategy(self, sample_check_strategy: SampleCheckStrategy):
		self.steps['sample_check_strategy'] = sample_check_strategy
		return self

	def with_model_generation_strategy(self, model_generation_strategy: ModelGenerationStrategy):
		self.steps['model_generation_strategy'] = model_generation_strategy
		return self

	def with_model_check_strategy(self, model_check_strategy: ModelCheckStrategy):
		self.steps['model_check_strategy'] = model_check_strategy
		return self

	def with_verification_strategy(self, verification_strategy: VerificationStrategy):
		self.steps['verification_strategy'] = verification_strategy
		return self

	def with_degeneracy_strategy(self, degeneracy_strategy: DegeneracyStrategy):
		self.steps['degeneracy_strategy'] = degeneracy_strategy
		return self
	
	def with_evaluation_strategy(self, evaluation_strategy: EvaluationStrategy):
		self.steps['evaluation_strategy'] = evaluation_strategy
		return self

	def with_model_refinement_strategy(self, model_refinement_strategy: ModelRefinementStrategy):
		self.steps['model_refinement_strategy'] = model_refinement_strategy
		return self

	def with_num_iterations(self, num_iterations: int):
		self.steps['num_iterations'] = num_iterations
		return self

	def build(self):
		return USAC(self.steps)

class USACFactory:
	@staticmethod
	def line_simple(num_iterations = 1000):
		return (USACBuilder()
			.with_sampling_strategy(RandomPointsSampling())
			.with_model_generation_strategy(LineFromPointsModelGeneration())
			.with_verification_strategy(PointOnLineVerification())
			.with_num_iterations(num_iterations)
			.build())
	
	@staticmethod
	def cylinder_simple(num_iterations = 20):
		return (USACBuilder()
			.with_sampling_strategy(RandomPointsSampling(9))
			.with_model_generation_strategy(CylinderFromPointsModelGeneration())
			.with_verification_strategy(PointOnCylinderVerification())
			.with_num_iterations(num_iterations)
			.build())
		

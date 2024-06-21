import numpy as np
from typing import TypedDict

from usac.degeneracy.all_pass import AllPassDegeneracy
from usac.degeneracy.strategy import DegeneracyStrategy
from usac.evaluation.count import CountEvaluation
from usac.evaluation.strategy import EvaluationStrategy
from usac.model_check.all_pass import AllPassModelCheck
from usac.model_check.strategy import ModelCheckStrategy
from usac.model_generation.cylinder_from_points import CylinderFromPointsModelGeneration
from usac.model_generation.cylinder_from_points_and_normals import CylinderFromPointsWithNormalsModelGeneration
from usac.model_generation.cylinder_from_points_forming_circle import CylinderFromPointsFormingCircleModelGeneration
from usac.model_generation.line_from_points import LineFromPointsModelGeneration
from usac.model_generation.strategy import ModelGenerationStrategy
from usac.model_refinement.no_refinement import NoRefinementModelRefinement
from usac.model_refinement.strategy import ModelRefinementStrategy
from usac.number_of_iterations.constant import ConstantNumberOfIterations
from usac.number_of_iterations.strategy import NumberOfIterationsStrategy
from usac.post_processing.no_post_process import NoPostProcessingPreprocessing
from usac.post_processing.strategy import PostProcessingStrategy
from usac.pre_processing.no_pre_process import NoPreProcessingPreprocessing
from usac.pre_processing.strategy import PreProcessingStrategy
from usac.prefiltering.all_pass import AllPassPrefiltering
from usac.prefiltering.strategy import PrefilteringStrategy
from usac.sample_check.all_pass import AllPassSampleCheck
from usac.sample_check.not_coplar import NotCoplanarSampleCheck
from usac.sample_check.not_parallel_normals import NotParallelNormalsSampleCheck
from usac.sample_check.strategy import SampleCheckStrategy
from usac.sampling.random_points import RandomPointsSampling
from usac.sampling.strategy import SamplingStrategy
from usac.verification.point_distance_from_cylinder_axis import PointDistanceFromCylinderAxisVerification
from usac.verification.point_on_cylinder import PointOnCylinderVerification
from usac.verification.point_on_line import PointOnLineVerification
from usac.verification.point_with_normals_on_cylinder import PointWithNormalsOnCylinderVerification
from usac.verification.strategy import VerificationStrategy

class USACStepsDefinitionRequired(TypedDict):
	sampling_strategy: SamplingStrategy
	model_generation_strategy: ModelGenerationStrategy
	verification_strategy: VerificationStrategy

class USACStepsDefinition(USACStepsDefinitionRequired, total = False):
	pre_processing_strategy: PreProcessingStrategy
	number_of_iterations_strategy: NumberOfIterationsStrategy
	prefiltering_strategy: PrefilteringStrategy
	sample_check_strategy: SampleCheckStrategy
	model_check_strategy: ModelCheckStrategy
	degeneracy_strategy: DegeneracyStrategy
	evaluation_strategy: EvaluationStrategy
	model_refinement_strategy: ModelRefinementStrategy
	post_processing_strategy: PostProcessingStrategy

class USAC:
	def __init__(self, steps: USACStepsDefinition):
		self.pre_processing_strategy = steps.get('pre_processing_strategy', NoPreProcessingPreprocessing())
		self.number_of_iterations_strategy = steps.get('number_of_iterations_strategy', ConstantNumberOfIterations())
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
		self.post_processing_strategy = steps.get('post_processing_strategy', NoPostProcessingPreprocessing())

	def run(self, data):
		# Step 0: Preprocessing
		pre_processed_data, pre_process_output = self.pre_processing_strategy.pre_process(data)
		# Step 1: Prefiltering
		filtered_data = self.prefiltering_strategy.prefiltering(pre_processed_data)
		
		# Initialize variables to track the best model
		best_model = None
		best_inliers = []
		best_score = float('-inf')

		for _ in range(self.number_of_iterations_strategy.number_of_iterations(filtered_data)):
			# Step 2: Sampling
			sample = self.sampling_strategy.sampling(filtered_data)
			
			# Step 3: Sample Check
			if not self.sample_check_strategy.sample_check(sample):
				continue
			
			# Step 4: Model Generation
			try:
				model = self.model_generation_strategy.model_generation(sample)
			except:
				continue
			
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
		
		if best_model is not None:
			# Step 8: Model Refinement
			best_model = self.model_refinement_strategy.model_refinement(best_model, best_inliers)
			# Step 9: Post Processing
			best_model, best_inliers = self.post_processing_strategy.post_process(best_model, best_inliers, pre_process_output)
		
		return best_model, best_inliers

class USACBuilder:
	def __init__(self):
		self.steps: USACStepsDefinition = {}

	def with_pre_processing_strategy(self, pre_processing_strategy: PreProcessingStrategy):
		self.steps['pre_processing_strategy'] = pre_processing_strategy
		return self

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

	def with_number_of_iterations_strategy(self, number_of_iterations_strategy: NumberOfIterationsStrategy):
		self.steps['number_of_iterations_strategy'] = number_of_iterations_strategy
		return self
	
	def with_post_processing_strategy(self, post_processing_strategy: PostProcessingStrategy):
		self.steps['post_processing_strategy'] = post_processing_strategy
		return self

	def build(self):
		return USAC(self.steps)

class USACFactory:
	@staticmethod
	def line_simple():
		return (USACBuilder()
			.with_sampling_strategy(RandomPointsSampling())
			.with_model_generation_strategy(LineFromPointsModelGeneration())
			.with_verification_strategy(PointOnLineVerification())
			.with_number_of_iterations_strategy(ConstantNumberOfIterations(1000))
			.build())
	
	@staticmethod
	def cylinder_simple():
		return (USACBuilder()
			.with_sampling_strategy(RandomPointsSampling(9))
			.with_sample_check_strategy(NotCoplanarSampleCheck())
			.with_model_generation_strategy(CylinderFromPointsModelGeneration())
			.with_verification_strategy(PointOnCylinderVerification())
			.build())
	
	@staticmethod
	def cylinder_with_normals():
		return (USACBuilder()
			.with_sampling_strategy(RandomPointsSampling(2))
			.with_sample_check_strategy(NotParallelNormalsSampleCheck())
			.with_model_generation_strategy(CylinderFromPointsWithNormalsModelGeneration())
			.with_verification_strategy(PointDistanceFromCylinderAxisVerification())
			.with_number_of_iterations_strategy(ConstantNumberOfIterations(1000))
			.build())
	
	@staticmethod
	def cylinder_from_points_forming_circle():
		return (USACBuilder()
			.with_sampling_strategy(RandomPointsSampling(3))
			.with_model_generation_strategy(CylinderFromPointsFormingCircleModelGeneration())
			.with_verification_strategy(PointDistanceFromCylinderAxisVerification())
			.with_number_of_iterations_strategy(ConstantNumberOfIterations(1000))
			.build())

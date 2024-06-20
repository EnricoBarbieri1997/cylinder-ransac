import utils.geometry as geometry
import numpy as np

def random_rotation_matrix():
	# Generate three random angles
	alpha, beta, gamma = np.random.uniform(0, 2*np.pi, 3)
	return geometry.rotation_matrix_from_angles(alpha, beta, gamma)
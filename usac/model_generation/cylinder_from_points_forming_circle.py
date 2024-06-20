import math
import numpy as np
from usac.model_generation.strategy import ModelGenerationStrategy
from utils.geometry import cylinder_from_center_radius_axis, rotation_between

class CylinderFromPointsFormingCircleModelGeneration(ModelGenerationStrategy):
	def model_generation(self, sample):
		p1 = sample[0]
		p2 = sample[1]
		p3 = sample[2]
		# triangle "edges"
		t = p2-p1
		u = p3-p1
		v = p3-p2

		# triangle normal
		w = np.cross(t, u)
		wsl = np.dot(w, w)

		# helpers
		iwsl2 = 1.0 / (2.0*wsl)
		tt = np.dot(t, t)
		uu = np.dot(u, u)

		# result circle
		center = p1 + (u*tt*np.dot(u, v) - t*uu*np.dot(t,v)) * iwsl2
		radius = math.sqrt(tt * uu * np.dot(v, v) * iwsl2*0.5)
		orthogonal_direction   = w / math.sqrt(wsl)

		return cylinder_from_center_radius_axis(center, radius, orthogonal_direction), [center, radius, orthogonal_direction]
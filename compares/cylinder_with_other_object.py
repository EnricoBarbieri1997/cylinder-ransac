import numpy as np
from compares.evaluate import evaluate_cylinder_over_other_object
from utils.point_clouds import sample_points_on_cube, sample_points_on_cylinder
import matplotlib.pyplot as plt

# Define the parameters of the cylinder
radius = 4.0
height = 10.0
num_points = 200

center = np.random.rand(3) * 10
axis = np.random.rand(3)
# axis = (1, 0, 0)
points = sample_points_on_cylinder(center, axis, radius, height, num_points, True)

cube_center = np.random.rand(3) * 10
cube_side = 4.0
cube_points = sample_points_on_cube(cube_center, cube_side, num_points, True)

evaluate_cylinder_over_other_object(points, [center, axis, radius], cube_points)
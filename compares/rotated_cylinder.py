import numpy as np
from compares.evaluate import evaluate_cylinder_over_noise
from utils.point_clouds import sample_points_on_cylinder
import matplotlib.pyplot as plt

# Define the parameters of the cylinder
radius = 4.0
height = 10.0
num_points = 200

center = (5, 5, 5)
axis = np.random.rand(3)
# axis = (1, 0, 0)
points = sample_points_on_cylinder(center, axis, radius, height, num_points, True)

x = points[:, 0]
y = points[:, 1]
z = points[:, 2]

# Plot the 3D points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))
ax.scatter(x, y, z)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

evaluate_cylinder_over_noise(points, [center, axis, radius])
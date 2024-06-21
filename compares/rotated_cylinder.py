import numpy as np
import pyransac3d
import matplotlib.pyplot as plt
from usac.usac import USACFactory
from utils.geometry import point_to_line_distance
from utils.point_clouds import sample_points_on_cylinder

# Define the parameters of the cylinder
radius = 4.0
height = 10.0
num_points = 200

center = (5, 5, 5)
axis = np.random.rand(3)
# axis = (1, 0, 0)
points = sample_points_on_cylinder(center, axis, radius, height, num_points)

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

min_noise = 0.05
max_noise = 0.4
noise_step = 0.05

noises = [x / 100.0 for x in range(int(min_noise*100), int(max_noise*100), int(noise_step*100))]

errors_pyransac3d = []
errors_our = []

for noise_scale in noises:
    # Add noise to the points position
    points[:, 0] += np.random.normal(0, noise_scale, num_points)
    points[:, 1] += np.random.normal(0, noise_scale, num_points)
    points[:, 2] += np.random.normal(0, noise_scale, num_points)

    center_pyransac3d, axis_pyransac3d, radius_pyransac3d, inliers = pyransac3d.Cylinder().fit(points, thresh=0.2, maxIteration=1000)
    [center_our, radius_our, axis_our], inliers,  = USACFactory.cylinder_from_points_forming_circle().run(points)

    error_pyransac3d = point_to_line_distance(center_pyransac3d, center, axis) + np.linalg.norm(axis_pyransac3d - axis) + np.abs(radius_pyransac3d - radius)
    error_our = point_to_line_distance(center_our, center, axis) + np.linalg.norm(axis_our - axis) + np.abs(radius_our - radius)

    # print(np.linalg.norm(center_pyransac3d - center) - np.linalg.norm(center_our - center))
    # print(np.linalg.norm(axis_pyransac3d - axis) - np.linalg.norm(axis_our - axis))
    # print(np.abs(radius_pyransac3d - radius) - np.abs(radius_our - radius))

    errors_pyransac3d.append(error_pyransac3d)
    errors_our.append(error_our)

# Plot the errors
plt.plot(noises, errors_pyransac3d, label='pyransac3d')
plt.plot(noises, errors_our, label='our')
plt.xlabel('Noise Scale')
plt.ylabel('Error')
plt.legend()
plt.show()

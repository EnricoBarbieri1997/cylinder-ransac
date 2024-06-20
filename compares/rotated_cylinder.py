import numpy as np
import pyransac3d
import open3d as o3d
import matplotlib.pyplot as plt
from usac.usac import USACFactory
from utils.random_extra import random_rotation_matrix

# Define the parameters of the cylinder
radius = 4.0
height = 10.0
num_points = 1000

# Generate random points on the surface of the cylinder
theta = np.random.uniform(0, 2*np.pi, num_points)
z = np.random.uniform(0, height, num_points)
x = radius * np.cos(theta)
y = radius * np.sin(theta)

# Combine the coordinates into a single array
points = np.column_stack((x, y, z))

# Calculate the normal vector pointing from the center to the surface points
normals = np.column_stack((x, y, np.zeros(num_points)))
normals /= np.linalg.norm(normals, axis=1)[:, np.newaxis]

# rotation = random_rotation_matrix()

# # Rotate the points and normals
# points = np.dot(points, rotation.T)
# normals = np.dot(normals, rotation.T)

min_noise = 0.05
max_noise = 0.4
noise_step = 0.05

# Plot the 3D points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

for noise_scale in range(min_noise, max_noise, noise_step):
    # Add noise to the points position
    x += np.random.normal(0, noise_scale, num_points)
    y += np.random.normal(0, noise_scale, num_points)
    z += np.random.normal(0, noise_scale, num_points)

    center, axis, radius, inliers = pyransac3d.Cylinder().fit(points, thresh=0.2, maxIteration=1000)
    data = USACFactory.cylinder_from_points_forming_circle().run(points)

    points_with_normals = np.column_stack((points, normals))

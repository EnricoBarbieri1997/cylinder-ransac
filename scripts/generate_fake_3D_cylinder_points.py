import numpy as np
import os
import matplotlib.pyplot as plt

# Define the parameters of the cylinder
radius = 4.0
height = 10.0
num_points = 1000

# Generate random points on the surface of the cylinder
theta = np.random.uniform(0, 2*np.pi, num_points)
z = np.random.uniform(0, height, num_points)
x = radius * np.cos(theta)
y = radius * np.sin(theta)

# Add noise to the points position
noise_scale = 0.5
x += np.random.normal(0, noise_scale, num_points)
y += np.random.normal(0, noise_scale, num_points)
z += np.random.normal(0, noise_scale, num_points)

# Combine the coordinates into a single array
points = np.column_stack((x, y, z))

# Plot the 3D points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Define the path to save the points file
points_file = os.path.join(script_dir, '../data/points.txt')
# Save the points array to the file
np.savetxt(points_file, points)
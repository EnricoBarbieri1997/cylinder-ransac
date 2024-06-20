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

# Generate random rotation angles
angles = np.random.uniform(0, 2*np.pi, 3)
# mesh_cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=height)
mesh_cylinder = o3d.geometry.TriangleMesh.create_coordinate_frame()
R = mesh_cylinder.get_rotation_matrix_from_xyz((np.pi / 2, 0, np.pi / 4))
mesh_cylinder.rotate(R, center=(0, 0, 0))
pcd_load = mesh_cylinder.sample_points_uniformly(number_of_points=num_points)
# o3d.visualization.draw_geometries([pcd_load])

min_noise = 0.05
max_noise = 0.4
noise_step = 0.05

for noise_scale in range(min_noise, max_noise, noise_step):
    # Add noise to the points position
    pcd_load[:, 0] += np.random.normal(0, noise_scale, num_points)
    pcd_load[:, 1] += np.random.normal(0, noise_scale, num_points)
    pcd_load[:, 2] += np.random.normal(0, noise_scale, num_points)

    # Plot the 3D points
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pcd_load[:, 0], pcd_load[:, 1], pcd_load[:, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

    center_pyransac3d, axis_pyransac3d, radius_pyransac3d, inliers = pyransac3d.Cylinder().fit(pcd_load, thresh=0.2, maxIteration=1000)
    model, inliers, [center, radius, axis] = USACFactory.cylinder_from_points_forming_circle().run(pcd_load)
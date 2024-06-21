import numpy as np

def sample_points_on_cylinder(base_center, axis_direction, radius, height, num_points):
    """
    Samples points on the surface of a cylinder.
    
    Parameters:
    - base_center: tuple (x0, y0, z0) - The center of the base of the cylinder.
    - axis_direction: tuple (ax, ay, az) - The direction vector of the cylinder's axis.
    - radius: float - The radius of the cylinder.
    - height: float - The height of the cylinder.
    - num_points: int - The number of points to sample.
    
    Returns:
    - points: numpy array of shape (num_points, 3) - The sampled points on the cylinder.
    """
    
    # Normalize the axis direction
    axis_direction = np.array(axis_direction)
    axis_direction = axis_direction / np.linalg.norm(axis_direction)
    
    # Create orthogonal vectors to the axis direction
    if axis_direction[0] == 0 and axis_direction[1] == 0:
        ortho_vector1 = np.array([1, 0, 0])
    else:
        ortho_vector1 = np.array([-axis_direction[1], axis_direction[0], 0])
    ortho_vector1 = ortho_vector1 / np.linalg.norm(ortho_vector1)
    ortho_vector2 = np.cross(axis_direction, ortho_vector1)
    
    points = []
    for _ in range(num_points):
        theta = np.random.uniform(0, 2 * np.pi)
        z = np.random.uniform(0, height)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        point_on_base_circle = x * ortho_vector1 + y * ortho_vector2
        point_on_cylinder = base_center + point_on_base_circle + z * axis_direction
        
        points.append(point_on_cylinder)
    
    return np.array(points)
import numpy as np

def sample_points_on_cube(center, side_length, num_points, include_normals=False):
    """
    Samples points on the surface of a cube.
    
    Parameters:
    - center: tuple (x0, y0, z0) - The center of the cube.
    - side_length: float - The side length of the cube.
    - num_points: int - The number of points to sample.
    
    Returns:
    - points: numpy array of shape (num_points, 3) - The sampled points on the cube.
    """
    
    half_side_length = side_length / 2
    points = []
    for _ in range(num_points):
        face = np.random.choice(['front', 'back', 'left', 'right', 'top', 'bottom'])
        x, y, z, normal = 0, 0, 0, [0, 0, 0]
        if face == 'front':
            x = half_side_length
            y = np.random.uniform(-half_side_length, half_side_length)
            z = np.random.uniform(-half_side_length, half_side_length)
            normal = np.array([1, 0, 0])
        elif face == 'back':
            x = -half_side_length
            y = np.random.uniform(-half_side_length, half_side_length)
            z = np.random.uniform(-half_side_length, half_side_length)
            normal = np.array([-1, 0, 0])
        elif face == 'left':
            x = np.random.uniform(-half_side_length, half_side_length)
            y = half_side_length
            z = np.random.uniform(-half_side_length, half_side_length)
            normal = np.array([0, 1, 0])
        elif face == 'right':
            x = np.random.uniform(-half_side_length, half_side_length)
            y = -half_side_length
            z = np.random.uniform(-half_side_length, half_side_length)
            normal = np.array([0, -1, 0])
        elif face == 'top':
            x = np.random.uniform(-half_side_length, half_side_length)
            y = np.random.uniform(-half_side_length, half_side_length)
            z = half_side_length
            normal = np.array([0, 0, 1])
        elif face == 'bottom':
            x = np.random.uniform(-half_side_length, half_side_length)
            y = np.random.uniform(-half_side_length, half_side_length)
            z = -half_side_length
            normal = np.array([0, 0, -1])
        
        if x == half_side_length:
            point = center + np.array([x, y, z])
        elif x == -half_side_length:
            point = center + np.array([x, y, z])
        elif y == half_side_length:
            point = center + np.array([x, y, z])
        elif y == -half_side_length:
            point = center + np.array([x, y, z])
        elif z == half_side_length:
            point = center + np.array([x, y, z])
        elif z == -half_side_length:
            point = center + np.array([x, y, z])
        
        if include_normals:
            point = np.concatenate([point, normal])
        
        points.append(point)
    
    return np.array(points)

def sample_points_on_cylinder(base_center, axis_direction, radius, height, num_points, include_normals=False):
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

        if include_normals:
            normal = point_on_base_circle - base_center
            normal = normal / np.linalg.norm(normal)
            point_on_cylinder = np.concatenate([point_on_cylinder, normal])
        
        points.append(point_on_cylinder)
    
    return np.array(points)
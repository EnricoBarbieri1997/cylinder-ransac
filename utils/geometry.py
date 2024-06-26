import numpy as np

def point_to_line_distance(point, offset, axis):
	return abs(np.linalg.norm(np.cross(axis, point[:3] - offset)) / np.linalg.norm(axis))

def rotation_between(vector_a, vector_b):
	v = np.cross(vector_a, vector_b)
	# s = np.linalg.norm(v)
	c = np.dot(vector_a, vector_b)
	v_skew_matrix = np.array([
		[0, -v[2], v[1]],
		[v[2], 0, -v[0]],
		[-v[1], v[0], 0]
	])

	return np.identity(3) + v_skew_matrix + np.dot(v_skew_matrix, v_skew_matrix) / (1+c)

def cylinder_from_center_radius_axis(center, radius, axis):
	z_up = [0, 0, 1]

	rotation_from_z_up = rotation_between(z_up, axis)
	rotation_matrix = np.identity(4)
	rotation_matrix[0:3, 0:3] = rotation_from_z_up
	translation = np.identity(4)
	translation[0:3, 3] = center
	transformation_matrix = np.dot(translation, rotation_matrix)

	inverse_radius = 1 / (radius**2)
	z_up_cylinder = [
		[inverse_radius, 0, 0, 0],
		[0, inverse_radius, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, -1]
	]

	# (x - c)^2 + (y-c)^2 = r^2
	# x^2 -2cx + c^2 + y^2 - 2cy + c^2 = r^2
	# x^2 -2cx + y^2 -2cy = (r^2 - c^2 - c^2)

	transformed_cylinder = transformation_matrix * z_up_cylinder * np.linalg.matrix_transpose(transformation_matrix)
	transformed_cylinder /= transformed_cylinder[3, 3]
	transformed_cylinder = np.identity(4)
	transformed_cylinder[0:3, 0:3] = np.identity(3) - np.dot(axis, axis)
	
	return [
		transformed_cylinder[0][0], # A
		transformed_cylinder[1][1], # B
		transformed_cylinder[2, 2], # C
		2 * transformed_cylinder[0][1], # D
		2 * transformed_cylinder[0][2], # E
		2 * transformed_cylinder[1][2], # F
		2 * transformed_cylinder[0, 3], # G
		2 * transformed_cylinder[1, 3], # H
		2 * transformed_cylinder[2, 3] # I
	]

def rotation_matrix_from_axis(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def rotation_matrix_from_angles(alpha, beta, gamma):
	# Create three rotation matrices
	rot_matrix1 = rotation_matrix_from_axis([1, 0, 0], alpha)
	rot_matrix2 = rotation_matrix_from_axis([0, 1, 0], beta)
	rot_matrix3 = rotation_matrix_from_axis([0, 0, 1], gamma)

	# Multiply the matrices to get a random 3D rotation matrix
	return np.dot(rot_matrix1, np.dot(rot_matrix2, rot_matrix3))
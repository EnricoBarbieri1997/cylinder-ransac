from matplotlib import pyplot as plt
import numpy as np
import pyransac3d
from usac.usac import USACFactory
from utils.geometry import point_to_line_distance
from multiprocessing import Pool as ThreadPool

def evaluate_multiple_strategies(arguments):
    noise_scale, points, model = arguments
    [center, axis, radius] = model

    points_without_normals = points[:, :3]
    normals = points[:, 3:]
    points_with_noise = points_without_normals + np.random.normal(0, noise_scale, points_without_normals.shape)
    points = np.concatenate([points_with_noise, normals], axis=1)

    center_pyransac3d, axis_pyransac3d, radius_pyransac3d, inliers = pyransac3d.Cylinder().fit(points_without_normals, thresh=0.2, maxIteration=1000)
    [center_circle, radius_circle, axis_circle], inliers  = USACFactory.cylinder_from_points_forming_circle().run(points_without_normals)
    [center_with_normals, radius_with_normals, axis_with_normals], inliers  = USACFactory.cylinder_with_normals().run(points)

    error_pyransac3d = point_to_line_distance(center_pyransac3d, center, axis) + np.linalg.norm(axis_pyransac3d - axis) + np.abs(radius_pyransac3d - radius)
    error_circle = point_to_line_distance(center_circle, center, axis) + np.linalg.norm(axis_circle - axis) + np.abs(radius_circle - radius)
    error_with_normals = point_to_line_distance(center_with_normals, center, axis) + np.linalg.norm(axis_with_normals - axis) + np.abs(radius_with_normals - radius)

    return error_pyransac3d, error_circle, error_with_normals

def print_errors(abscissa, errors, label):
    errors_pyransac3d = [error[0] for error in errors]
    errors_circle = [error[1] for error in errors]
    errors_with_normals = [error[2] for error in errors]

    # Plot the errors
    plt.plot(abscissa, errors_pyransac3d, label='pyransac3d')
    plt.plot(abscissa, errors_circle, label='circle method')
    plt.plot(abscissa, errors_with_normals, label='normals method')
    plt.xlabel(label)
    plt.ylabel('Error')
    plt.legend()
    plt.show()

def evaluate_cylinder_over_noise(points, model):
    min_noise = 0.05
    max_noise = 0.4
    noise_step = 0.05

    noises = [x / 100.0 for x in range(int(min_noise*100), int(max_noise*100), int(noise_step*100))]
    noises_with_parameters = [[noise, points, model] for noise in noises]

    pool = ThreadPool(8)
    errors = pool.map(evaluate_multiple_strategies, noises_with_parameters)

    print_errors(noises, errors, 'Noise Scale')

def evaluate_cylinder_over_other_object(points, model, outliers):
    min_outlier_percentage = 0.1
    max_outlier_percentage = 1.0
    outlier_percentage_step = 0.1

    max_outliers = len(outliers)

    outliers_counts = [int(x / 100.0 * max_outliers) for x in range(int(min_outlier_percentage*100), int(max_outlier_percentage*100), int(outlier_percentage_step*100))]
    parameters = []
    for outliers_count in outliers_counts:
        points_with_outliers = np.concatenate([
            points,
            outliers[np.random.choice(max_outliers, outliers_count, replace=False)]
        ])
        np.random.shuffle(points_with_outliers)
        parameters.append([
        0,
        points_with_outliers,
        model
    ])

    pool = ThreadPool(8)
    errors = pool.map(evaluate_multiple_strategies, parameters)
    outliers_percentages = [outliers_count / (len(points) + outliers_count) for outliers_count in outliers_counts]
    print_errors(outliers_percentages, errors, 'Outliers Percentage')
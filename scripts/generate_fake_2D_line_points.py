import numpy as np
import os

# Define the line parameters
slope = 2.0
intercept = 1.0

# Generate x values
x = np.linspace(0, 10, 100)

# Generate y values with some noise
noise = np.random.normal(0, 0.5, len(x))
y = slope * x + intercept + noise

# Create the numpy array of 2D points
points = np.array(list(zip(x, y)))

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to save the points file
points_file = os.path.join(script_dir, '../data/points.txt')

# Save the points array to the file
np.savetxt(points_file, points)
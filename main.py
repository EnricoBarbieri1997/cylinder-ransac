import argparse

import numpy as np

from usac.usac import USACFactory

# Create an argument parser
parser = argparse.ArgumentParser(description='Read named parameters')

# Add the required arguments
parser.add_argument('--file', type=str, help='Path to the file containing 3D points')
parser.add_argument('--points', nargs='+', type=float, help='List of 3D points')

# Parse the command line arguments
args = parser.parse_args()

# Check if either file or points is specified
if args.file is None and args.points is None:
	print('Error: Either --file or --points must be specified.')
	exit(1)

points = None

if args.file:
	points = np.loadtxt(args.file)
else:
	points = np.array([])

line_fitting = USACFactory.line_simple(10)
model, inliers = line_fitting.run(points)
print(model)
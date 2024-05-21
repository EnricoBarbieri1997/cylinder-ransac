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

cylinder_fitting = USACFactory.cylinder_from_points_forming_circle()
model, inliers = cylinder_fitting.run(points)
print(model)
print(f"{model[0]}x^2 + {model[1]}y^2 + {model[2]}z^2 + {model[3]}xy + {model[4]}xz + {model[5]}yz + {model[6]}x + {model[7]}y + {model[8]}z + 1 = 0")

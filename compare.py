import argparse

parser = argparse.ArgumentParser(description='Read named parameters')
parser.add_argument('--type', type=str, help='name of comparison')

args = parser.parse_args()

if args.type == None:
    print('Error: --type must be specified.')
    exit(1)

if args.type == 'rotated_cylinder':
    from compares.rotated_cylinder import *

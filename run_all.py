import argparse
import subprocess as sub

parser = argparse.ArgumentParser('Run all variants of an algorithm')
parser.add_argument('-a', choices=[ 'astar', 'ga', 'gsa', 'mct', 'minmin', 'olb', 'tabu' ], required=True)

args = parser.parse_args()

variants = []
for x in ['c', 'i', 's']:
	for y in ['l', 'h']:
		for z in ['l', 'h']:
			var = x + '-' + y + '-' + z
			variants.append(var)

for variant in variants:
	cmd = 'python runner.py -a ' + args.a + ' -v ' + variant
	print cmd

	sub.call(cmd, shell=True)

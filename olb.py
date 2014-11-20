import model
import argparse
import numpy
import sys

parser = argparse.ArgumentParser('OLB')
parser.add_argument('-f', '--data-file', dest='data_file', required=True)
args = parser.parse_args()

M = model.Model(args.data_file)

def avail_times(map):
	return [ map.etc(m) for m in range(M.nmachines) ]

mapping = model.Mapping(M)
for t in range(M.ntasks):
	next_available_machine = numpy.argmin(avail_times(mapping))
	mapping.assign(t, next_available_machine)

print(mapping.makespan())
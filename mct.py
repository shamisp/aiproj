import model
import argparse
import numpy
import sys

parser = argparse.ArgumentParser('Min-Min')
parser.add_argument('-f', '--data-file', dest='data_file', required=True)
args = parser.parse_args()

M = model.Model(args.data_file)
def completion_time(mapping, t, m):
	''' the completion time should task t be assigned to m '''
	global M
	return mapping.etc(m) + M.etc(t, m)

def mct(mapping, t):
	''' returns the machine that task t would achieve it's MCT on '''
	global M
	cts = [ completion_time(mapping, t, m) for m in range(M.nmachines) ]
	m = numpy.argmin(cts)

	#print cts
	#print 'min: ', m, cts[m]
	return (t, m, cts[m])

mapping = model.Mapping(M)
for t in range(M.ntasks):
	m = mct(mapping, t)[1]
	mapping.assign(t, m)

print(mapping.makespan())
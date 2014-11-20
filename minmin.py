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
unassigned = [t for t in range(M.ntasks)]
while len(unassigned) > 0:
	mcts = [ mct(mapping, t) for t in unassigned ]
	min_index = numpy.argmin(map(lambda x: x[2], mcts))
	
	(t, m, CT) = mcts[min_index]

	mapping.assign(t, m)
	unassigned.remove(t)
	#print len(unassigned)

print(mapping.makespan())
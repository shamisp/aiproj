import model
import argparse
import numpy
import sys

def run(data):
	def completion_time(mapping, t, m):
		''' the completion time should task t be assigned to m '''
		return mapping.etc(m) + data.etc(t, m)

	def mct(mapping, t):
		''' returns the machine that task t would achieve it's MCT on '''
		cts = [ completion_time(mapping, t, m) for m in range(data.nmachines) ]
		m = numpy.argmin(cts)
		return (t, m, cts[m])

	mapping = model.Mapping(data)
	unassigned = [t for t in range(data.ntasks)]
	while len(unassigned) > 0:
		mcts = [ mct(mapping, t) for t in unassigned ]
		min_index = numpy.argmin(map(lambda x: x[2], mcts))
		
		(t, m, CT) = mcts[min_index]

		mapping.assign(t, m)
		unassigned.remove(t)

	return mapping

if __name__ == '__main__':
	parser = argparse.ArgumentParser('Min-Min')
	parser.add_argument('-f', '--data-file', dest='data_file', required=True)
	args = parser.parse_args()

	data = model.Model(args.data_file)
	mapping = run(data)
	print(mapping.makespan())
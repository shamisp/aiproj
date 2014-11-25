import glob
import numpy

def makespan(f):
	f = open(f, 'r')

	last_line = ''
	for l in f:
		last_line = l

	return float(last_line)

def makespans(algo, variant):
	return sorted([
			makespan(f)
			for f
			in glob.glob('./out/' + variant + '/' + algo + '.*') ])

def box_and_whisker_data(l):
	if len(l) % 2 == 0:
		lower_half = l[:len(l) / 2]
		upper_half = l[len(l) / 2:]
	else:
		lower_half = l[:len(l) / 2]
		upper_half = l[len(l) / 2 + 1:]

	q1 = numpy.median(lower_half)
	q2 = numpy.median(l)
	q3 = numpy.median(upper_half)

	return (min(l), q1, q2, q3, max(l))

def confidence_interval(l, confidence=0.95):
	#
	# http://stackoverflow.com/questions/15033511/compute-a-confidence-interval-from-sample-data
	#

	if len(l) == 0:
		return 0, 0, 0

	import numpy as np
	import scipy as sp
	import scipy.stats

	a = 1.0 * np.array(l)
	n = len(a)
	m, se = np.mean(a), scipy.stats.sem(a)
	h = se * sp.stats.t._ppf((1 + confidence) / 2., n - 1)
	return m, h

if __name__ == '__main__':
	import argparse

	variants = []
	for x in ['c', 'i', 's']:
		for y in ['l', 'h']:
			for z in ['l', 'h']:
				var = x + '-' + y + '-' + z
				variants.append(var)

	parser = argparse.ArgumentParser('Data Collector')
	parser.add_argument('-a', choices=[ 'astar', 'mct', 'minmin', 'olb', 'tabu' ], dest='algo', help='The algorithm to run', required=True)
	parser.add_argument('-v', choices=variants, dest='variant', help='The variant of the data file to run', default='i-l-l')
	args = parser.parse_args()
	# print ','.join(map(
	# 			lambda x: str(x),
	# 			box_and_whisker_data(makespans)
	# 		))

	print ','.join(map(lambda x: str(x), confidence_interval(makespans(args.algo, args.variant))))

import argparse

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plot
import numpy
import algo_stat
import os

def _mkdir(s):
	try:
		os.mkdir(s)
	except:
		pass

_mkdir('./plots/')

def variant_to_string(v):
	def sub(s):
		return s.upper() \
			.replace('C', 'Consistent') \
			.replace('I', 'Inconsistent') \
			.replace('S', 'Semi-Consistent') \
			.replace('L', 'Low') \
			.replace('H', 'High')
	parts = map(lambda x: sub(x), v.split('-'))
	return parts[0] + '/' + parts[1] + '-' + parts[2]

variants = []
for x in ['c', 'i', 's']:
	for y in ['l', 'h']:
		for z in ['l', 'h']:
			var = x + '-' + y + '-' + z
			variants.append(var)

parser = argparse.ArgumentParser('Plotter')
parser.add_argument('-v', choices=variants, dest='variant', help='The variant to plot', required=True)
args = parser.parse_args()
VARIANT = args.variant

algorithms = {}
algorithms['astar'] = 'A*'
algorithms['mct'] = 'MCT'
algorithms['minmin'] = 'Min-Min'
algorithms['olb'] = 'OLB'
algorithms['tabu'] = 'Tabu'

data = {}
for algo in algorithms.keys():
	data[algo] = algo_stat.confidence_interval(algo_stat.makespans(algo, VARIANT))

labels = [ algorithms[algo] for algo in algorithms.keys() ]
means = [ data[algo][0] for algo in algorithms.keys() ]
error = [ data[algo][1] for algo in algorithms.keys() ]

plot.bar(
	numpy.arange(len(algorithms)),
	means,
	yerr=error,
	align='center',
	alpha=0.4
)
plot.xticks(numpy.arange(len(algorithms)), labels)
plot.ylabel('Makespan')
plot.title(variant_to_string(VARIANT))
plot.savefig('./plots/' + VARIANT + '.png')

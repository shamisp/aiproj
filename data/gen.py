import numpy as n
import numpy.random as r
import argparse as ap
import os
import os.path

def fix_matrix(m, type):
	''' ensures the matrix is consistent, inconsistent, or semi-consistent, based on the argument 'type' '''
	t = m.shape[0]
	
	if type == 'c':
		# make consistent (sort the rows)
		for r in range(t):
			m[r].sort()
	elif type == 'i':
		pass # nothing to do
	elif type == 's':
		# make semi-consistent (sort the even columns)
		for r in range(t):
			row = m[r]
			even = row[::2]
			odd = row[1::2]
			
			even.sort()
			zipped = zip(even, odd) # list of tuples with even/odd elements staggered
			flattened = [i for sub in zipped for i in sub] # tuples removed
			
			m[r] = flattened
	return m

def gen_matrix(args):
	''' generates a matrix '''
	
	# create a t by m empty matrix
	rows = n.empty((args.tasks, args.machines), int)
	
	# generate the rows
	for i in range(args.tasks):
		# phi_b (from the paper)
		tmax = 100 if args.t_var == 'LOW' else 3000
		row = r.random_integers(1, tmax - 1, args.machines)
		
		# phi_r (from the paper)
		mmax = 10 if args.m_var == 'LOW' else 1000
		row_multiplier = r.random_integers(1, mmax - 1, args.machines)
		
		row *= row_multiplier
		
		rows[i] = row
	return fix_matrix(rows, args.type)

# get command-line arguments
parser = ap.ArgumentParser('ETC generator')
parser.add_argument('--inconsistent', action='store_const', dest='type', const='i', help="Generate inconsistent matrices")
parser.add_argument('--consistent', action='store_const', dest='type', const='c', help="Generate consistent matrices")
parser.add_argument('--semi', action='store_const', dest='type', const='s', help="Generate semi-consistent matrices")
parser.add_argument('-t', '--tasks', dest='tasks', action='store', default=512, type=int, help='The number of tasks')
parser.add_argument('-m', '--machines', action='store', default=16, type=int, help='The number of machines')
parser.add_argument('-tv', '--task-variance', dest='t_var', choices=[ 'LOW', 'HIGH' ], default='LOW', help='The task heterogeneity')
parser.add_argument('-mv', '--machine-variance', dest='m_var', choices=[ 'LOW', 'HIGH' ], default='LOW', help='The machine heterogeneity')
parser.add_argument('-n', action='store', default=50, type=int, help='The number of matrices to generate')
parser.add_argument('-d', '--dest', dest='dir', action='store', default='.' + os.path.sep, type=str, help='The destination directory')
args = parser.parse_args() # ex. Namespace(m_var='HIGH', machines=16, n=1, t_var='LOW', tasks=512, type='c')

if args.type == None:
	args.type = 'c' # default is consistent

# check for directory
if not os.path.isdir(args.dir):
	os.mkdir(args.dir)

header = str(vars(args))
for i in range(args.n):
	etc_matrix = gen_matrix(args)

	fname = args.dir + os.path.sep + str(i + 1) + '.csv'
	#print fname
	n.savetxt(fname, etc_matrix, fmt='%d', delimiter=',', header=header)

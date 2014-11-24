import argparse
import ssh
import os

variants = []
for x in ['c', 'i', 's']:
	for y in ['l', 'h']:
		for z in ['l', 'h']:
			variants.append(x + '-' + y + '-' + z)

parser = argparse.ArgumentParser('Simulation Runner')
parser.add_argument('-a', choices=[ 'astar', 'mct', 'minmin', 'olb', 'tabu' ], dest='algo', help='The algorithm to run', required=True)
parser.add_argument('-n', type=int, help='The number of trials to run', default=5)
parser.add_argument('-v', choices=variants, dest='variant', help='The variant of the data file to run', default='i-l-l')
args = parser.parse_args()

print('Running ' + args.algo.upper())

cwd = os.getcwd()

print('Fetching machine list...')
machs = ssh.get_least_cpu_utilized(max_cpu=50)

print('Starting' + str(args.n) + ' runs...')
for i in range(args.n):
	mach = machs[i % len(machs)]

	cmd = 'python '
	cmd += '\'' + cwd + '/' + args.algo + '.py\' ' # the algorithm script file (ex.: minmin.py)
	cmd += '-f \'' + cwd + '/data/' + args.variant + '/' + str(i) + '.csv\'' # the data file to run off of (ex.: .../i-l-l/1.csv)
	cmd += '> \'' + cwd + '/out/' + args.variant + '/' + args.algo + '.out\'' # pipe output to a file in the ./data/ directory
	cmd += ' &' # run in the background

	print cmd
	ssh.single_ssh_cmd(cmd, mach)

print('Done')

#threads = ssh_cmd('cat /etc/hostname', ['peanut', 'bananas'])
#print ssh.get_least_cpu_utilized()
#print get_machines()

#threads = ssh.ssh_cmd('sleep 10 && echo "hey"', ssh.get_machines(), 1)
#out = [ t.out for t in threads ]
#print out

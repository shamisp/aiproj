import argparse
import ssh

variants = []
for x in ['c', 'i', 's']:
	for y in ['l', 'h']:
		for z in ['l', 'h']:
			var = x + '-' + y + '-' + z
			variants.append(var)

parser = argparse.ArgumentParser('Simulation Runner')
parser.add_argument('-a', choices=[ 'astar', 'ga', 'gsa', 'mct', 'minmin', 'olb', 'tabu' ], dest='algo', help='The algorithm to run', required=True)
parser.add_argument('-v', choices=variants, dest='variant', help='The variant of the data file to run', default='i-l-l')
parser.add_argument('--kill', dest='kill', action='store_true', default=False, help='If present, kills the processes found')
args = parser.parse_args()

# print 'Querying machines...'

machs = ssh.get_machines()
cmd = 'ps -ef | grep ' + args.algo + ' | grep \'' + args.variant + '\' | grep -v \'grep\' | grep -v \'kill.py\' | awk \'{print $2}\''
# print cmd
threads = ssh.ssh_cmd(cmd, machs)

# iterate over the machines
for t in threads:
	if t.out == None:
		continue

	# get the PID's running on the current machine
	for pid in t.out.split():
		try:
			pid = int(pid)
			print 'Found', pid, 'on', t.mach, '(killed)' if args.kill else ''

			if args.kill == True:
				cmd = 'kill ' + str(pid)
				ssh.single_ssh_cmd(cmd, t.mach)
			else:
				print ssh.single_ssh_cmd('ps -p ' + pid, t.mach)
		except:
			# NaN
			continue

# print('Done')

import subprocess as sub
import threading

def single_ssh_cmd(cmd, machine='peanut', connectionTimeout=5):
	'''
	Executes a single SSH command on the given machine
	'''
	c = 'ssh -o StrictHostKeyChecking=no'
	if connectionTimeout != None:
		c += ' -o ConnectTimeout=' + str(connectionTimeout)
	c +=  ' ' + machine + '.cs.colostate.edu ' + cmd

	p = sub.Popen(c, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
	(out, err) = p.communicate()
	if err.strip() != '':
		return None
	else:
		return out

def ssh_cmd(cmd, machines=[], timeout=None):
	'''
	Executes an SSH command in parallel on a set of machines

	Returns a list of objects that contain a property 'out' that
	is the STDOUT of the command executed.
	'''
	class SingleSshCmd(threading.Thread):
		def __init__(self, cmd, mach):
			self.cmd = cmd
			self.mach = mach
			self.out = None
			threading.Thread.__init__(self)

		def run(self):
			self.out = single_ssh_cmd(self.cmd, self.mach)

	threads = [ SingleSshCmd(cmd, mach) for mach in machines ]
	for t in threads:
		t.start()

	for t in threads:
		if timeout != None:
			t.join(timeout)
		else:
			t.join()

	return threads

def get_machines():
	'''
	Gets a list of CS machines designated for general use
	'''
	machs = single_ssh_cmd("cat ~info/machines | grep 'Linux(Fedora)' | grep 'general' | awk '{print $1}' | grep '^[a-z|\-]*$'")
	return machs.split()

def get_least_cpu_utilized(machines=None, max_cpu=100):
	'''
	Returns a list machines sorted from low to high
	based on the cpu utilization of that machine
	'''
	if machines == None:
		machines = get_machines()

	cmd = "sar -u 3 1 | tail -n 1 | awk '{print $5}'" # prints a number such as 8.45 (the CPU usage)
	threads = ssh_cmd(cmd, machines, 10) # run the command on "all the things"
	
	# now filter the results based on commands that actually returned a number
	# and that are less than max_cpu
	def _isfloat(s):
		try:
			float(s)
			return True
		except:
			return False
	cpu = [ (t.mach, float(t.out)) for t in
				filter(lambda x: _isfloat(x.out) and float(x.out) < max_cpu,
						threads) ]

	# sort the results on increading CPU usage
	def _comparator(x, y):
		diff = x[1] - y[1]
		return -1 if diff < 0 else 1 if diff > 0 else 0

	# now strip out the CPU usage numbers and just return the machines, in sorted order of course
	return [ x[0] for x in sorted(cpu, cmp=_comparator) ]

from subprocess import call
import os.path

TASKS = '512'#'75'
MACHS = '16'#'4'

# generate the 12 different cases:
for consistency, switch in { 'c': '--consistent', 'i': '--inconsistent', 's': '--semi' }.iteritems():
	for t_var in [ 'LOW', 'HIGH' ]:
		t_prefix = t_var[0].lower()
		for m_var in [ 'LOW', 'HIGH' ]:
			m_prefix = m_var[0].lower()

			dirname = '.' + os.path.sep + consistency + '-' + t_prefix + '-' + m_prefix
			cmd = [ 'python',  'gen.py', switch, '-t', TASKS, '-m', MACHS, '-tv', t_var, '-mv', m_var, '-n', '50', '-d', dirname ]
			print cmd
			call(cmd)
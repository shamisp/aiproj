import numpy

class Model:
	def __init__(self, fname):
		self._etc = numpy.loadtxt(fname, delimiter=',', skiprows=1)
		self.ntasks = self._etc.shape[0]
		self.nmachines = self._etc.shape[1]

	def etc(self, t, m):
		return self._etc[t, m]

class Mapping:
	def __init__(self, model):
		self._model = model
		self._machine_tasks = [ [] for i in range(model.nmachines) ]
		self._task_machines = [ None for i in range(model.ntasks) ]
		self._etcs = [ 0 for i in range(model.nmachines) ]

	def assign(self, t, m):
		assert(not t in self._machine_tasks[m])
		assert(self._task_machines[t] == None)

		self._machine_tasks[m].append(t)
		self._task_machines[t] = m
		self._etcs[m] += self._model.etc(t, m)

	def unassign(self, t):
		m = self._task_machines[t]
		self._task_machines[t] = None
		self._machine_tasks[m].remove(t)
		self._etcs[m] -= self._model.etc(t, m)

	def etc(self, m):
		return self._etcs[m]

	def makespan(self):
		return max(self._etcs)

	def machine(self, t):
		''' returns the machine t is assigned to '''
		return self._task_machines[t]

	def similar(self, otherMapping):
		''' returns the # of task-to-machine assignments that are shared between these two mappings '''
		return numpy.array_equal(self._task_machines, otherMapping._task_machines)

	def __str__(self):
		return str(self._machine_tasks)

if __name__ == '__main__':
	model = Model('./data/c-l-l/1.csv')
	mapping = Mapping(model)

	etc1 = model.etc(0, 0)

	mapping.assign(0, 0)
	etc2 = mapping.etc(0)

	assert etc1 == etc2
	assert mapping.makespan() == etc1

	mapping.unassign(0)
	assert mapping.etc(0) == 0

	print 'Tests complete'

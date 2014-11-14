import numpy

class Model:
	def __init__(self, fname):
		self._etc = numpy.loadtxt(fname, delimiter=',', skiprows=1)
		self.ntasks = self._etc.shape[0]
		self.nmachines = self._etc.shape[1]

	def etc(self, t, m):
		return self._etc[t, m]

class Mapping:
	def __init__(self, model, reversable = True):
		'''
		reversable: denotes whether this object should keep track of which task is assigned to which machine.
			This is useful for the A* algorithm, as it doesn't need for this class to keep track of queues, etc.
		'''
		self._model = model

		if reversable:
			self._machine_tasks = [ [] for i in range(model.nmachines) ]
			self._task_machines = [ None for i in range(model.ntasks) ]
		
		self._etcs = [ 0 for i in range(model.nmachines) ]
		self._reversable = reversable

	def assign(self, t, m):
		if self._reversable:
			assert(not t in self._machine_tasks[m])
			assert(self._task_machines[t] == None)
			self._machine_tasks[m].append(t)
			self._task_machines[t] = m

		self._etcs[m] += self._model.etc(t, m)

	def unassign(self, t):
		assert(self._reversable)

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
		assert(self._reversable)
		return self._task_machines[t]

	def similar(self, otherMapping):
		''' returns the # of task-to-machine assignments that are shared between these two mappings '''
		assert(self._reversable)
		return numpy.array_equal(self._task_machines, otherMapping._task_machines)

	def __str__(self):
		assert(self._reversable)
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

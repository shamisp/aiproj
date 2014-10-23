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
		self._machines_queues = [ [] for i in range(model.nmachines)]

	def assign(self, t, m):
		assert(not t in self._machines_queues[m])
		self._machines_queues[m].append(t)

	def unassign(self, t):
		for queue in self._machines_queues:
			if t in queue:
				queue.remove(t)

	def etc(self, m):
		return reduce(
			lambda etc, t: etc + self._model.etc(t, m),
			self._machines_queues[m],
			0)

	def makespan(self):
		etcs = [ self.etc(m) for m in range(self._model.nmachines) ]
		return max(etcs)

	def __str__(self):
		return str(self._machines_queues)

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

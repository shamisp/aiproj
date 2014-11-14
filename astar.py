import model
import sys

MAX_NODES = 64

class Node:
	''' An A* node '''
	def __init__(self, t, m, model, parent = None):
		self.t = t
		self.m = m
		self.model = model
		self.parent = parent

		if parent == None:
			self.depth = 0
		else:
			self.depth = parent.depth + 1

		self._mapping = None

	def mapping(self):
		if self._mapping != None:
			return self._mapping

		self._mapping = model.Mapping(self.model, reversable = False)
		n = self
		while n != None:
			self._mapping.assign(n.t, n.m)
			n = n.parent
		return self._mapping

	def g(self):
		# TODO: innefficient?
		return self.mapping().makespan()

	def is_leaf(self):
		return (self.depth + 1) == self.model.ntasks

def astar_next_level(data, parent):
	t = 0 if parent == None else (parent.depth + 1)
	#print t

	next = []
	for m in range(data.nmachines):
		next.append(Node(t, m, data, parent))
	return next

def astar_search(data, H):
	''' Implement A* search '''
	def _f(n):
		return n.g() + H(n)

	def _sort_and_truncate(l):
		def _cmp(n1, n2):
			c = _f(n1) - _f(n2)
			if c < 0:
				return -1
			elif c > 0:
				return 1
			else:
				# if the two nodes' _f(n) is the same, break ties based on depth,
				# prioritizing nodes that are deaper (highest depth to lowest)
				return n2.depth - n1.depth
		l.sort(cmp = _cmp)
		while len(l) > MAX_NODES:
			l.pop(MAX_NODES)

	unexplored = astar_next_level(data, None)
	_sort_and_truncate(unexplored)
	while True:
		fs = [ _f(n) for n in unexplored ]
		print fs[0:10], len(fs)

		top = unexplored.pop(0)
		print 'Exploring task', top.depth, _f(top), len(unexplored)
		if top.is_leaf():
			return top.mapping()

		unexplored.extend(astar_next_level(data, top))
		_sort_and_truncate(unexplored)

def mct_time(n, t):
	_mct = sys.maxint
	for j in range(n.model.nmachines):
		ct = n.mapping().etc(j) + n.model.etc(t, j)
		if ct < _mct:
			_mct = ct
	return _mct

def h1(n):
	#def mct_machines():
	def mmct(n):
		_max = 0
		for i in range(n.model.ntasks):
			_mct = mct_time(n, i)
			if _mct > _max:
				_max = _mct
		return _max

	return max(0, mmct(n) - n.g())

def h2(n):
	def sdma(n):
		_sum = 0
		mkspn = n.mapping().makespan()
		for m in range(n.model.nmachines):
			_sum += mkspn - n.mapping().etc(m)
		return _sum

	def smet(n):
		_totMct = 0
		for i in range(n.t + 1, n.model.ntasks):
			_totMct += mct_time(n, i)
		return _totMct

	return max(0, float(smet(n) - sdma(n)) / float(n.model.nmachines))

# def h(n):
# 	return max(h1(n), h2(n))

data = model.Model('./data/i-h-h/1.csv')
solution = astar_search(data, lambda n: max(h1(n), h2(n)))

print solution.makespan()


import argparse
import bisect
import model
import sys

MAX_NODES = 1024 #64

parser = argparse.ArgumentParser('Min-Min')
parser.add_argument('-f', '--data-file', dest='data_file', required=True)
args = parser.parse_args()

class Node:
	''' An A* node '''
	def __init__(self, t, m, _model, parent = None):
		self.t = t
		self.m = m
		self.model = _model
		self.parent = parent
		self.mapping = parent.mapping.copy() if parent != None else model.Mapping(_model, reversable = False)
		self.mapping.assign(t, m)
		self.mcts = {}
		self._f = None
		self._g = None
		self._h = None

		if parent == None:
			self.depth = 0
		else:
			self.depth = parent.depth + 1

	def is_leaf(self):
		return (self.depth + 1) == self.model.ntasks

	def mct_time(self, t):
		if not t in self.mcts:
			self.mcts[t] = min([ self.mapping.etc(j) + self.model.etc(t, j) for j in range(self.model.nmachines) ])
		return self.mcts[t]

	def f(self):
		if self._f == None:
			self._f = self.g() + self.h()
		return self._f

	def g(self):
		if self._g == None:
			self._g = self.mapping.makespan()
		return self._g

	def h(self):
		if self._h != None:
			return self._h

		def _h1():
			def mmct():
				return max([ self.mct_time(i) for i in range(self.model.ntasks) ])
			return max(0, mmct() - self.g())

		def _h2():
			def sdma():
				mkspn = self.mapping.makespan()
				return sum([ mkspn - self.mapping.etc(m) for m in range(self.model.nmachines) ])

			def smet():
				return sum([ self.mct_time(i) for i in range(self.t + 1, self.model.ntasks) ])

			return max(0, float(smet() - sdma()) / float(self.model.nmachines))

		self._h = max(_h1(), _h2())
		return self._h

	def __cmp__(self, other):
		if other == None:
			return 1

		c = self.f() - other.f()
		if c == 0:
			# if the two nodes' f() is the same, break ties based on depth,
			# prioritizing nodes that are deaper (highest depth to lowest)
			c = other.depth - self.depth
		
		if c < 0:
			return -1
		elif c > 0:
			return 1
		else:
			return 0

	def __str__(self):
		return str(self.f())

	def __repr__(self):
		return self.__str__()

def astar_next_level(data, parent):
	t = 0 if parent == None else (parent.depth + 1)
	#print t

	next = []
	for m in range(data.nmachines):
		next.append(Node(t, m, data, parent))
	return next

def astar_search(data):
	''' Implement A* search '''
	unexplored = []
	def _extend_from(parent):
		for n_next in astar_next_level(data, parent):
			bisect.insort_left(unexplored, n_next)
		while len(unexplored) > MAX_NODES:
	 		unexplored.pop(MAX_NODES)

	_extend_from(None)
	#unexplored = sorted(unexplored)
	last_task = 0
	while True:
		fs = [ n.f() for n in unexplored[0:10] ]
		# print fs, len(unexplored)

		top = unexplored.pop(0)
		# print 'Exploring task', top.depth, top.f(), len(unexplored)
		if top.depth > last_task:
			last_task = top.depth
			print 'Exploring task', last_task
		
		if top.is_leaf():
			return top.mapping

		_extend_from(top)

data = model.Model(args.data_file)
solution = astar_search(data) #lambda n: max(h1(n), h2(n)))

print solution.makespan()


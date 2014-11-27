import model
import random
import itertools

class Chromosome:
    def __init__(self, m, tabu_list=None, empty=False):
        ''' generate random chromosome from the model '''
        self.model=m
        self.regenerate(empty)
        
    def regenerate(self, empty=False):
        self.map = model.Mapping(self.model)
        if (not empty):
            for i in range(self.model.ntasks):
                self.map.assign(i, random.randint(0, self.model.nmachines - 1))
    
    def permutations(self):
        ''' generate permutation of task exchanges '''
        return itertools.combinations(range(self.model.ntasks),2)
    
    def value(self):
        ''' calculate makespan for the chromosome '''
        return self.map.makespan()
    
    def apply_permutation(self, perm):
        ''' apply permutation to the chromosome '''
        t1, t2 = perm
        m1, m2 = self.map.machine(t1), self.map.machine(t2)

        self.map.unassign(t1)
        self.map.unassign(t2)

        self.map.assign(t1, m2)
        self.map.assign(t2, m1)
    
    def unapply_permutation(self, perm):
        ''' unapply permutation '''
        self.apply_permutation(perm)
    
    def above_50(self, ch):
        return self.map.similar(ch.map) / self.model.ntasks >= 0.5
    
    def apply_mutatation(self):
        rand_task = random.randint(0, self.model.ntasks-1)
        # Making sure that the value is actually changed
        while True:
            curr_m = self.map.machine(rand_task)
            new_m = random.randint(0, self.model.nmachines - 1)
            if new_m != curr_m:
                break
        self.map.unassign(rand_task)
        self.map.assign(rand_task, new_m)
    
    def __repr__(self):
        return str(self.map._task_machines)
    
    def __str__(self):
        return str(self.map._task_machines)

def crossover(M, a, b):
    assert a.model.ntasks ==  b.model.ntasks
    assert a.model.nmachines ==  b.model.nmachines
    assert M.nmachines ==  a.model.nmachines
    assert M.ntasks ==  a.model.ntasks
    
    new = Chromosome(M, tabu_list=None, empty=True)
    intersec = random.randint(0, M.ntasks-1)
    
    for t in range(intersec):
        new.map.assign(t, a.map.machine(t))
    
    for t in range(intersec,M.ntasks):
        new.map.assign(t, b.map.machine(t))
        
    return new
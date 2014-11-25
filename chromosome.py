import model
import random
import itertools

class Chromosome:
    def __init__(self, m, tabu_list=None):
        ''' generate random chromosome from the model '''
        self.model=m
        self.regenerate()
        
    def regenerate(self):
        self.map = model.Mapping(self.model)
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

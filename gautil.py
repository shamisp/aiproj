import model
import itertools
import numpy
import random
import bisect
import minmin
from chromosome import Chromosome , crossover

P_SIZE=200          # population size
CROSSOVER_PRB=0.6   # crossover probability 
MUTATION_PRB=0.4    # mutation probability
DEBUG = False

# Generate initial population. We seed it with one min-min value
def generate_new_population(M):
    chrs=[]
    for _ in itertools.repeat(None, P_SIZE-1):
        chrs.append(Chromosome(M))
    # Seed min-min
    ch = Chromosome(M, tabu_list=None, empty=True)
    mapping = minmin.run(M)
    if DEBUG: print mapping, mapping.makespan()
    
    for t in range(mapping._model.ntasks):
        ch.map.assign(t, mapping.machine(t))
    chrs.append(ch)    
    return chrs
'''
def calc_probability(chrs):
    total = 0
    result=[]
    for ch in chrs:
        total+=ch.value()
    for ch in chrs:
        # lowest value should have higher probability
        # this normalization is broken
        result.append(ch.value()/total)
    
    assert len(result) == len(chrs)    
    return result
'''

def calc_probability(chrs):
    total = 0
    rtotal = 0
    result=[]
    
    for ch in chrs:
        total+=ch.value()
    
    for ch in chrs:
        # lowest value should have higher probability
        # this normalization is broken
        result.append(total/ch.value())
        rtotal+=total/ch.value()
    
    for i in range(len(result)):
        result[i] = result[i]/rtotal

    assert len(result) == len(chrs)    
    
    return result

def find_elite_index(prb):
    return numpy.argmax(numpy.array(prb))

def find_elite_ch(chrs, prb):
    assert len(prb) == len(chrs)
    return (chrs[find_elite_index(prb)], 
            find_elite_index(prb)) 

def select_with_probability(num, prb, chrs):
    assert len(prb) == len(chrs)
    acc_prb = [None]*len(prb)
    acc_prb[0] = prb[0]
    for i in range(1,len(prb)):
        acc_prb[i]=acc_prb[i-1] + prb[i]
    
    # the rest of the selection code is based on 
    # http://stackoverflow.com/questions/4113307/pythonic-way-to-select-list-elements-with-different-probability
    result=[]
    for _ in range(num):
        x = random.random()
        index = bisect.bisect(acc_prb, x)
        result.append(chrs[index])
    
    return result

def select_for_crossover(chrs):
    # Select even number of chromosome for crossover
    result = []
    for ch in chrs:
        if random.random() <= CROSSOVER_PRB:
            result.append(ch)
    if (len(result)/2):
        result.pop()
    return result

def mutate_chromosome(ch):
    if random.random() <= MUTATION_PRB:
        ch.apply_mutatation()
        if DEBUG: print "M: ", ch  

''' Not used
def mutate_population(chrs):
    for ch in len(chrs):
        if random.random() <= MUTATION_PRB:
            ch.apply_mutatation()  
'''
            
def crossover_population(M, chrs):
    c_ppl = select_for_crossover(chrs)
    for _ in c_ppl:
        a = c_ppl.pop()
        b = c_ppl.pop()
        c = crossover(M, a, b)
        if DEBUG: print "A: ", a
        if DEBUG: print "B: ", b
        if DEBUG: print "C: ", c
        mutate_chromosome(c)
        chrs.append(c)

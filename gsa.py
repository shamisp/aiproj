import model
import argparse
from gautil import *

parser = argparse.ArgumentParser('GSA')
parser.add_argument('-f', '--data-file', dest='data_file', required=True)
args = parser.parse_args()

TOTAL_ITER=1000     # total iterations
MAX_NO_CHANGE=150   # no change in elite chromosome
REG_CYCLES=4
SEEDED_CYCLES=4

def gsa(M, seed):
    elite_count = 0
    elite_value = -1
    ppl = generate_new_population(M, seed)
    temp = calc_temp(ppl)
    if DEBUG: print"Initial temperature: ", temp
    
    for i in range(TOTAL_ITER):
        if DEBUG: print "Iteration ", i
        assert(len(ppl) == P_SIZE)
        
        # select elite and do the checks        
        elite, index = find_elite_ch(ppl,prb=None)
        
        if(elite.value() == elite_value):
            elite_count += 1
            if DEBUG: print "No change in elite ", elite_value
        else:
            if elite.value() > elite_value and -1 != elite_value:
                print "Bug ! new elite > old elite", elite.value, elite_value
            elite_value = elite.value()
            elite_count = 0
            
        if elite_count == MAX_NO_CHANGE:
            return elite
        
        ppl.pop(index)            
        
        # selection is done
        gsacrossover_population(M, ppl, temp)
        ppl.append(elite)
        temp = adjust_temp(temp)
        if DEBUG: print"Adjusted temperature: ", temp    
    return elite
        
M = model.Model(args.data_file)
total_cycles=0
best_c=None

for i in range(REG_CYCLES):
    print "Cycle number (not seeded):", total_cycles
    res = gsa(M, seed=False)
    print ">> Mapping: ", res.map
    print ">> Value: ", res.value()
    if i == 0 or res.value() < best_c.value():
        best_c = res
    total_cycles+=1

for _ in range(SEEDED_CYCLES):
    print "Cycle number (seeded):", total_cycles
    res = gsa(M, seed=True)
    print ">> Mapping: ", res.map
    print ">> Value: ", res.value()
    if res.value() < best_c.value():
        best_c = res
    total_cycles+=1

print "Mapping: ", best_c.map
print "Value: ", best_c.value()
import model
import argparse
from gautil import *

parser = argparse.ArgumentParser('GSA')
parser.add_argument('-f', '--data-file', dest='data_file', required=True)
args = parser.parse_args()

TOTAL_ITER=1000     # total iterations
MAX_NO_CHANGE=150   # no change in elite chromosome

def gsa(M):
    elite_count = 0
    elite_value = -1
    ppl = generate_new_population(M)
    temp = calc_temp(ppl)
    if DEBUG: print"Initial temperature: ", temp
    
    for i in range(TOTAL_ITER):
        print "Iteration ", i
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
best_c = gsa(M)

print "Mapping: ", best_c.map
print "Value: ", best_c.value()
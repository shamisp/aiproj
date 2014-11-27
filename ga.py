import model
import argparse
from gautil import *

parser = argparse.ArgumentParser('GA')
parser.add_argument('-f', '--data-file', dest='data_file', required=True)
args = parser.parse_args()

TOTAL_ITER=1000     # total iterations
MAX_NO_CHANGE=150   # no change in elite chromosome

def ga(M):
    elite_count = 0
    elite_value = -1
    ppl = generate_new_population(M)
    
    for i in range(TOTAL_ITER):
        print "Iteration ", i
        
        pb = calc_probability(ppl)
        
        # select elite and do the checks        
        elite, index = find_elite_ch(ppl,pb)
        
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
        selection = select_with_probability(P_SIZE-1, 
                                            calc_probability(ppl), 
                                            ppl)
        selection.append(elite)
        # selection is done
        crossover_population(M, selection)
        ppl = selection
    
    return elite
        
M = model.Model(args.data_file)
best_c = ga(M)

print "Mapping: ", best_c.map
print "Value: ", best_c.value()
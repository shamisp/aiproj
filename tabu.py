import model
import argparse
import chromosome

parser = argparse.ArgumentParser('Tabu')
parser.add_argument('-f', '--data-file', dest='data_file', required=True)
args = parser.parse_args()

M = model.Model(args.data_file)
mapping = model.Mapping(M)

MAX_LONG_HOPS=1200
MAX_SHORT_HOPS=1200

num_short_hops=0
num_long_hops=0
tabu_list=[]
best_c = None

def tabu_check(c, tabu_list):
    again = True
    ntry  = 0
    max_try = (c.model.nmachines**c.model.ntasks)/2
    
    while(ntry < max_try and again):
        again = False
        # check if we have similar (50% or more) chromosomes in the tabu list
        for ch in tabu_list:
            if c.above_50(ch):
                c.generate()
                again = True
                ntry += 1
                break
    return again

while num_long_hops + num_short_hops < MAX_LONG_HOPS:
    print num_long_hops + num_short_hops, MAX_LONG_HOPS
    c = chromosome.Chromosome(M, tabu_list)
    
    if (tabu_check(c, tabu_list)):
        break
    
    short_best_etc = c.value()
    num_short_hops = 0
    while num_short_hops < MAX_SHORT_HOPS:           
        print '\t', num_short_hops, MAX_SHORT_HOPS
        perm_found=False
        for perm in c.permutations():
            #print perm
            c.apply_permutation(perm)
            c_v = c.value()
            if (c_v < short_best_etc):
                short_best_etc = c_v
                perm_found = True
                break
            else:
                c.unapply_permutation(perm)
        if(False == perm_found):
            break
        else:
            num_short_hops+=1
    # We done with short hops
    # append new value to the tupple list
    tabu_list.append(c)
    num_long_hops+=1
    
# Find optimal mapping from the tabu list

best_c = tabu_list[0]
for element in tabu_list:
    if(element.value() < best_c.value()):
        best_c = element
 
print "Mapping: ", best_c.map
print "Value: ", best_c.value()
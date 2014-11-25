import model
import argparse
import itertools
from chromosome import Chromosome 

parser = argparse.ArgumentParser('GA')
parser.add_argument('-f', '--data-file', dest='data_file', required=True)
args = parser.parse_args()

M = model.Model(args.data_file)
mapping = model.Mapping(M)

P_SIZE=200 # population size
TOTAL_ITER=1000 # total iterations
MAX_NO_CHANGE=150 # no change in elite chromosome

# Generate initial population. We seed it with one min-min value
chrs=[]
for _ in itertools.repeat(None, P_SIZE):
    chrs.append(Chromosome(M))
# Todo: Update the code to seed one entry from min-min

chrs[0].value()
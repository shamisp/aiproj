aiproj
======

AI project for CS440

*note: most runnable Python files use the argument parser library, and so help messages can often be displayed with `python [file.py] -h`.*

# Setup

Data sets for the algorithms must be generated before the algorithms can be run:

`$ cd data; python gen_all.py`

This generates twelve sub-directories in `data/`, whose name is of the form: `(c|i|s)-(l|h)-(l|h)`, where **C** stands for **consistent** matrix, *I* stands for **inconsistent**, and **S** stands for **semi-consistent**. The next two groups are for task- and machine- heterogeneity (**L**ow, or **H**igh), respectively.

# Supporting Files

There are a few supporting files that provide model-abstraction APIs to the algorithms:

* `chromosome.py` - used by GA, GSA, and Tabu
* `gautil.py` - used by GA and GSA
* `model.py` - used by the rest of the algorithms

The rest of the files that are not the algorithm implementations (see below) are utility scripts for running, gathering, and plotting the results.

# Running the Algorithms

There are seven algorithms in this project: Opportunistic Load Balancing (OLB), Minimum Completion Time (MCT), Min-Min, Genetic Algorithm (GA), Genetic Simulated Annealing (GSA), Tabu, and A*. They reside in the following files:

* OLB: `olb.py`
* MCT: `mct.py`
* Min-Min: `minmin.py`
* GA: `ga.py`
* GSA: `gsa.py`
* Tabu: `tabu.py`
* A*: `astar.py`

To run MCT (for example) against the first data file for a consistent-low-task-heterogeneity-low-machine-heterogeneity, run:

`python mct.py -f data/c-l-l/1.csv`

Help messages for each of the algorithms can be displayed on any of the algorithm files with the `-h` switch.  For example:

`python mct.py -h`

# Automated tools:

## `runner.py`

Use this script to run a set of algorithms on the Computer Science (CS) machines:

Login to a CS machine and run:

`python runner.py -a astar -v c-l-l -n 50`

This will start fifty runs of the A* algorithm, running the variant 'c-l-l' (loads the datasets that are *c*onsistent/*low*/*low* [as described in the paper])

## `kill.py`

Use this script to kill runs started on the CS machines.

`python kill.py -a astar -v c-l-l` just lists out processes that are still running.  To force the script to kill the processes it finds, introduce the switch `--kill`.

## `plot.py`

Plot a variant as a PNG file:

`python plot.py -v c-l-l` generates the file `c-l-l.png`.

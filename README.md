aiproj
======

AI project for CS440

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

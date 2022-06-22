# Overlapping community detection evaluation
This Python project is created for comparing algorithms that detect networks with overlapping communities. 
This means a node is not only restricted to being member of one network.

data-sets:
https://github.com/danison2/C-MLC/blob/f7927b6194f5f8d4e228974065f5afe99406eca1/data/ground_truth/com-facebook.txt

## Dependencies:

Linux (sorry): I tried for a long time to keep it windows only. However, many of the algorithms and measures did not work since they were written for linux.
I even tried resolving dependencies and adapting the C++ code for the Windows compiler. That could have made it all work on Windows. 
However, there were many issues including stack corruption that I do not have enough knowledge for to fix.

Python 3.9 (Only tested version, There are at least some features that require 3.8)

Python packages listed in `requirements.txt`

GUI for matplotlib by `sudo apt-get install python-tk`

## Project structure

* **external/weighted_weak_communities.py:** Contains files for WNW algorithm, referenced in paper as O-HAMUHI
* **real_networks:** contains all the real-life networks used to run the experiment on
* **synthetic_networks:** starts empty, is filled by the LFR-benchmark with synthetic network files.
* **requirements.txt:** Contains all the python package dependencies
* **src:** Contains the python files that run
  * **algorithm.py:** All algorithms that have been compared can be called in this file
  * **benchmark.py:** API with the LFR benchmark project. To generate the synthetic networks and to convert such a file to a networkx graph
  * **debug.py:** A debug print function
  * **main.py:** Entry of the program, running this file creates everything for the paper
  * **measure.py:** Implements all the measures used to verify the quality of the results: NMI, Omega Index, NF1
  * **results.py:** Collects all the results created by measures and combines them to 
  * **utils.py:** Contains utility functions, mostly for reading/writing to files and converting formats
  * **visualize.py:** Converts the results to plots using matplotlib
* **(synthetic|real)_results.dat:** File containing all the results of the networks, gathers all output information in this file.

## Running

After following the steps in the readme and installing all the requirements with pip running should be done by running main.py from its own level

The first time the plots will be empty. The plots are created from the information gathered by the previous run.
So if you want to see the plots then let it run for a few minutes and run it again.
Stopping the algorithm from running will **NOT** result in lost data from computations. The information is all stored in the output files.
So the program will automatically continue from where it left off.

**_Warning:_** Doing a full run will take a few hours, this is because the Omega Index computation takes exponentially long the larger the network gets.

### Output of the program
The output is not inside the terminal, the majority that prints to it is OSLOM, however we could not find a way to surpress this

The folders real_networks and synthetic_networks will get changed.
Each subdirectory in this folder is a network. You will find that the names in synthetic_networks are named according to the parameters with which it is ran.
Also, it is prefixed with UW if it is unweighted, otherwise it is called W
After running the algorithms you can re-run, and then it will produce the results.dat file that contains the results, in addition it will visualize the data in plots.


The folder structure after running is the following:
* **(synthetic|real)_networks/\*\*/:** path to the network folder
  * **community.dat:** The unprocessed file containing information about the communities
  * **network.dat:** All the edges with optionally their weight as third value on the line
  * _SYNTHETIC ONLY:_
    * **statistics.dat:** Statistics about the generated network 
    * **time_seed.dat:** The seed with which LRF ran, it is a non-deterministic algorithm

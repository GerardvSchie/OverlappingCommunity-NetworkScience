# Research comparing overlapping communities

This repository is used to compare algorithms that can detect overlapping communities.
It contains the data used and the algorithms that are compared.
The code that controls the algorithms can be found in the PyAlgorithms folder. This is a Python project that calls the external buildfiles using subprocesses.

Note: This entire repository depends on linux. I have tried to make it work for Windows but without any luck.

I think it does not depend on java anymore.

**TODO: Link all the source code locations**

## Generating synthetic networks

LFR-Benchmark can create synthetic networks given some parameters.

### Building
This project needs to get built so the Python code can access it.

* Install cmake on your system
* cd into `src_refactor_cpp`
* `mkdir build`
* `cd build`
* `cmake ..`

### Verify build
In the README.md file of LFR-benchmark project examples can be found 

## Detecting overlapping communities
There are several algorithms implemented that can run to produce a community structure of the given network with (weighted) edges.

### Demon

This is a python library, listed in `requirements.txt` of the python project. It runs an algorithm that builds bottom to top by combining small networks.

### O-HAMUHI

Is situated in a python file in directory external of the python project. The source code has not been changed.

### OSLOM
It is a separate directory that contains the code. It is a c++ project that needs to get built seperately. The instructions are listed below. Oslom 2 is chosen since it is a faster version than the original Oslom, and it does give similar results.

#### Building OSLOM
Directory: Algo_Oslom2

run `sh ./compile_all.sh` and this produces all the files necessary.

Again, in the readme of the project are examples that can be ran to verify success of the build.

## Verifying quality of the results

### NMI score

This is a c++ package that needs to get compiled. 

#### Build instructions

`cd ./Measure_NMI`
`make`

To make sure it works you can run an example listed in the ReadMe.txt

### Omega-Index

Package form PyPi to compute the omega index.
Same API as: https://github.com/isaranto/omega_index

### Average F1-score

Computes the average f1 score and the deviation.
IMPORTANT: Does not seem to work correctly.

The source code of the python package is here:
https://github.com/GiulioRossetti/f1-communities

## Running Python project

After also following the instructions listed in PyAlgorithms/Readme.md it should now be possible to run the python code. I myself used PyCharm to run the `main.py` file. If you run into any issues please contact us so you can also run it.

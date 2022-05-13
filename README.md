# Research comparing overlapping communities

This repository is used to compare algorithms that can detect overlapping communities.
It will contain the data used and the algorithms that are compared.

## Generating synthetic networks
LFR-Benchmark can create synthetic networks given some parameters
For now it looks like it cannot create the resulting files in subdirectories.
So only give a file name using `-name` argument.

Compiling is done by compiling the benchm.cpp file. This is done by running the solution
Or by calling from the Visual Studio command line `cl ./Source/benchm.cpp`

It is extended so arguments can be given in the command line.
For example the following command can be put in the console window.

```
./benchmark -N 1000 -k 15 -maxk 50 -muw 0.1 -minc 20 -maxc 50 -cnl 1 -name case1K15
```

This wil create 3 files with the name `case1K15`.

## Python code

Contains small karate club example using the Demon package.
CFinder, DEMON, and OSLOM package should be able to be called from python code itself.
Sofar it is only a `main.py` that can be ran. requirements.txt should contain the packages that are necessary.

### DEMON algorithm

Link to the package repo. The README there should give sufficient instructions to run the python code.
https://github.com/GiulioRossetti/DEMON

### OSLOM algorithm

Still work in progress. The c++ code compiles and example can be ran (executable needs to be environment variables somewhere so python package can find it).
This is not yet configured

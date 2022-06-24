#!/bin/bash
# e: exit if fails, x: trace
set -e

# shellcheck disable=SC2154
# echo an error message before exiting
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

# Set the current directory
REPO_DIR=$(pwd)

# Build oslom
cd Algo_Oslom2
echo "at $(pwd)"
echo "sh compile_all.sh"
# sh compile_all.sh
cd "${REPO_DIR}"

# Build LFR benchmark
cd Benchmark_LFR/2009-LFR-Benchmark/src_refactor_cpp
mkdir -p build
cd build
echo "at $(pwd)"
echo "cmake .."
# cmake ..
cd "${REPO_DIR}"

# Build NMI
cd Measure_NMI
echo "at $(pwd)"
echo "make ."
# make .
cd "${REPO_DIR}"

# Python requirements
cd PyAlgorithms
python3 -m pip install -r requirements.txt
cd "${REPO_DIR}"

echo "everything is built, now you can run main.py"

# Remove trap
trap - EXIT

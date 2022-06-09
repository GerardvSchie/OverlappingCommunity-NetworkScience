# Examples of LFR parameters:
# https://www.researchgate.net/publication/277659058_A_Stochastic_Model_for_Detecting_Overlapping_and_Hierarchical_Community_Structure
# https://www.ijsr.net/archive/v3i8/MDIwMTU2MTY=.pdf

import os
import subprocess
import shutil
import networkx as nx

import utils

LFR_BIN = os.path.abspath("../../Benchmark_LFR/lfrbench_udwov")


# Create the graph using LFR-benchmark
# k=20, kmax 50, cmin 20, cmax 100, tow1 -2, tow2 = -1, mixing = 0.4 Om=2, nr overlapping nodes = On/n
# n = 1000-10000 dn=1000 Om=1-8 dOm=1 On/n 0.1-0.6 dOn/n=0.1
def create_graph(N:int, k:int, maxk:int, mixing_topology:float, mixing_weights:float, tow1:float, tow2:float, minc:int, maxc:int, on:int, om:int, name:str, result_dir:str):
    filename = os.path.join("..", "networks", str(name), str(name))
    seed_path = os.path.join("..", "seed.txt")
    command = [
        LFR_BIN,
        "-N", str(N),
        "-k", str(k),
        "-maxk", str(maxk),
        "-mut", str(mixing_topology),
        "-muw", str(mixing_weights),
        "-t1", str(tow1),
        "-t2", str(tow2),
        "-minc", str(minc),
        "-maxc", str(maxc),
        "-on", str(on),
        "-om", str(om),
        "-cnl", "1",
        # Put file in networks folder and use fixed seed
        "-name", filename,
        "-seed", seed_path
    ]
    subprocess.run(command, shell=True, check=True)

    # Copy over communities and edges file
    shutil.copyfile(filename + ".cnl", os.path.join(result_dir, "communities.dat"))
    utils.copy_without_comments(os.path.abspath(filename) + ".nse", os.path.join(result_dir, "edges.dat"))


def read_graph(edges_path, weighted=False):
    '''
    Reads the input network in networkx.
    '''
    edges = utils.read_file(edges_path)
    if weighted:
        G = nx.parse_edgelist(edges, nodetype=int, data=(("weight", float),), delimiter='\t', create_using=nx.Graph())
    else:
        G = nx.parse_edgelist(edges, nodetype=int, delimiter='\t', create_using=nx.Graph())

    # Quick check to see if the parsing worked
    # print(G.edges(data = True))
    return G

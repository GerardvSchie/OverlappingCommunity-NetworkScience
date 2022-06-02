import os
import subprocess
import shutil
import networkx as nx

import utils

LFR_BIN = os.path.abspath("../../Benchmark_LFR/x64/Debug")


# Create the graph using LFR-benchmark
def create_graph(N:int, k:int, maxk:int, muw:float, minc:int, maxc:int, name:str, result_dir:str):
    filename = os.path.join("../networks", str(name))
    command = [
        os.path.join(LFR_BIN, "LFR-Benchmark.exe"),
        "-N", str(N),
        "-k", str(k),
        "-maxk", str(maxk),
        "-muw", str(muw),
        "-minc", str(minc),
        "-maxc", str(maxc),
        "-cnl", "1",
        # Put file in networks folder
        "-name", filename
    ]
    subprocess.run(command, shell=True, check=True)

    # Copy over communities and edges file
    shutil.copyfile(filename + ".cnl", os.path.join(result_dir, "communities.dat"))
    utils.copy_without_comments(os.path.join(result_dir, "edges.dat"), os.path.abspath(filename) + ".nse")


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

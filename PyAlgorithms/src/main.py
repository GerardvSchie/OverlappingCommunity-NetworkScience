import networkx as nx
import subprocess
import os
import demon as d
import oslom
import matplotlib.pyplot as plt
from argparse import Namespace

LFR_BIN = os.path.abspath("../../LFR-Benchmark_UndirWeightOvp/x64/Debug")
OSLOM_BIN = os.path.abspath("../../Oslom_visual_1_5_8/x64/Debug")

def run_demon(G):
    dm = d.Demon(graph=G, epsilon=0.25, min_community_size=3)
    coms = dm.execute()
    return coms


def visual_graph(G):
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


# Create the graph using LFR-benchmark
def create_graph(N:int, k:int, maxk:int, muw:float, minc:int, maxc:int, name:str):
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
        "-name", os.path.join("../networks", str(name))
    ]
    subprocess.run(command, shell=True, check=True)


# Reads the file content and returns it
def read_file(file_path) -> [str]:
    lines = []
    with open(file_path, "r") as file:
        while line := file.readline().rstrip():
            lines.append(line)
    return lines


def read_graph(edges_path, weighted=False):
    '''
    Reads the input network in networkx.
    '''
    edges = read_file(edges_path)
    if weighted:
        G = nx.parse_edgelist(edges, nodetype=int, data=(("weight", float),), delimiter='\t', create_using=nx.Graph())
    else:
        G = nx.parse_edgelist(edges, nodetype=int, delimiter='\t', create_using=nx.Graph())

    # Quick check to see if the parsing worked
    # print(G.edges(data = True))
    return G


def run_oslom(path, weighted=False):
    weightedArg = None
    if weighted:
        weightedArg = "-w"
    else:
        weightedArg = "-uw"

    # OSLOM -f example.dat -uw -time 0.005 -infomap 3 -copra 2 -louvain 1
    command = [
        os.path.join(OSLOM_BIN, "OSLOM.exe"),
        "-f", path,
        weightedArg,
        "-t", "0.005",
        "-infomap", "3",
        "-copra", "2",
        "-louvain", "1"
    ]
    subprocess.run(command, shell=True, check=True)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Generate graph using LFR benchmark executable
    graph_name = "test100_15"
    # create_graph(100, 5, 20, 0.1, 7, 20, graph_name)

    # Read the graph from the generated edge (*.nse) file into nx graph
    path = os.path.join("../networks", graph_name + ".nse")
    # G = read_graph(path, weighted=True)

    run_oslom(path)

    # Sanity check that it has been read
    # print("Degree distribution:")
    # print(nx.degree_histogram(G))
    #
    # # Detect communities on karate club network
    # KarateGraph = nx.karate_club_graph()
    # demon_communities = run_demon(G)
    # print(demon_communities)
    #
    # # Visualize the network
    # visual_graph(G)

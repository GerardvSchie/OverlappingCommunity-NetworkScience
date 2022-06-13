# Examples of LFR parameters:
# https://www.researchgate.net/publication/277659058_A_Stochastic_Model_for_Detecting_Overlapping_and_Hierarchical_Community_Structure
# https://www.ijsr.net/archive/v3i8/MDIwMTU2MTY=.pdf

import os
import subprocess
import shutil
import networkx as nx
import debug

import utils

LFR_BUILD_DIR = os.path.abspath(os.path.join("..", "..", "Benchmark_LFR", "2009-LFR-Benchmark", "src_refactor_cpp", "build"))
LFR_UW_BIN = os.path.join(LFR_BUILD_DIR, "undirected_graph", "lfr_undir_net")
LFR_W_BIN = os.path.join(LFR_BUILD_DIR, "weighted_graph", "lfr_weighted_net")


# Create the graph using LFR-benchmark
# k=20, kmax 50, cmin 20, cmax 100, tow1 -2, tow2 = -1, mixing = 0.4 Om=2, nr overlapping nodes = On/n
# n = 1000-10000 dn=1000 Om=1-8 dOm=1 On/n 0.1-0.6 dOn/n=0.1
def create_graph(weighted:bool, N:int, k:int, maxk:int, mixing_topology:float, mixing_weights:float, tow1:float, tow2:float, minc:int, maxc:int, on:int, om:int, graph_dir:str):
    debug.print_msg("LFR running")

    # Command that runs weighted network
    if weighted:
        command = [
            LFR_W_BIN,
            "-N", str(N),
            "-k", str(k),
            "-maxk", str(maxk),
            # "-mu", str(mixing_topology),
            "-muw", str(mixing_weights),
            "-t1", str(tow1),
            "-t2", str(tow2),
            "-minc", str(minc),
            "-maxc", str(maxc),
            "-on", str(on),
            "-om", str(om),
        ]

    # Command that creates unweighted network
    else:
        command = [
            LFR_UW_BIN,
            "-N", str(N),
            "-k", str(k),
            "-maxk", str(maxk),
            "-mu", str(mixing_topology),
            "-t1", str(tow1),
            "-t2", str(tow2),
            "-minc", str(minc),
            "-maxc", str(maxc),
            "-on", str(on),
            "-om", str(om),
        ]
    # Create the network
    subprocess.run(command, check=False)

    # Copy all files to the networks directory
    for file_name in ["network.dat", "community.dat", "statistics.dat", "time_seed.dat"]:
        shutil.move(file_name, os.path.join(graph_dir, file_name))


def community_to_nmi_file(graph_dir: str):
    # Dict that for each community will contain a list of all members
    communities = dict()

    # Collect the communities for each node,
    with open(os.path.join(graph_dir, "community.dat"), "r") as file:
        # Example line: "200   1 4 5" where node 200 is member of community 1 4 5
        for line in file.readlines():
            # Split on tab, which is after node number
            node_nr, community_nrs = line.strip().split('\t')
            community_nrs = community_nrs.split()
            node_nr, community_nrs = int(node_nr), [int(nr) for nr in community_nrs]

            # Add node to each community in dict
            for nr in community_nrs:
                # Community number doesn't yet exist in dictionary
                if nr not in communities:
                    communities[nr] = []
                communities[nr].append(node_nr)

    # Write the communities in file so each line has a line for each community
    nmi_output_file = os.path.join(graph_dir, "results", "community.dat")
    with open(nmi_output_file, "w") as file:
        # Write all members of the community per line
        for community in communities:
            for member in communities[community]:
                file.write(str(member) + " ")
            file.write("\n")


def read_graph(weighted: bool, edges_path: str):
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

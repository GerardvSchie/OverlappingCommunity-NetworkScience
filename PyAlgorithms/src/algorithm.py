# Paper: https://cs.paperswithcode.com/paper/high-quality-disjoint-and-overlapping
# Source: https://github.com/velicast/WMW

import os
import subprocess
import demon as d
import networkx as nx
import networkx.algorithms as nxa
import shutil
import external.weighted_weak_communities
import debug

CFINDER_BIN = os.path.abspath("../../Algo_CFinder")
OSLOM2_BIN = os.path.abspath(os.path.join("..", "..", "Algo_Oslom2", "oslom_undir"))


def run_demon(G):
    debug.print_msg("Run demon")
    dm = d.Demon(graph=G, epsilon=0.25, min_community_size=3)
    coms = dm.execute()
    return coms


def run_oslom2(path: str, weighted):
    debug.print_msg("Run oslom2")
    if weighted:
        weighted_flag = "-w"
    else:
        weighted_flag = "-uw"

    assert os.path.exists(path)

    # OSLOM -f example.dat -uw -time 0.005 -infomap 3 -copra 2 -louvain 1
    command = [
        OSLOM2_BIN,
        "-f", path,
        weighted_flag,
        "-t", "0.005",
        "-infomap", "3",
        "-copra", "2",
        "-louvain", "1",
        "-fast"
    ]

    # print(command)

    # subprocess.run(command, shell=True, check=True)

    # Somehow does not work with subprocess.run
    command_line = " ".join(command)
    os.system(command_line)



def run_wnw(G, weighted):
    debug.print_msg("Run WNW")
    if nx.is_directed(G):
        return None
    elif weighted:
        comms_sets = external.weighted_weak_communities.weighted_weak_communities(G, weight='weight')
    else:
        comms_sets = external.weighted_weak_communities.weighted_weak_communities(G)

    # Convert to lists
    communities = []
    for comm in comms_sets:
        communities.append(list(comm))
    return communities

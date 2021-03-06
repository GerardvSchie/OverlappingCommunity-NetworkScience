# Paper: https://cs.paperswithcode.com/paper/high-quality-disjoint-and-overlapping
# Source: https://github.com/velicast/WMW

import os
import demon as d
import networkx as nx
import external.WMW.weighted_weak_communities as WMW
import external.LinkCommunity.link_clustering as LinkCommunity
import debug

OSLOM2_BIN = os.path.abspath(os.path.join("..", "..", "Algo_Oslom2", "oslom_undir"))
ALGOS = ["Demon", "Oslom", "O-HAMUHI", "ground-truth"]


def run_demon(G):
    debug.print_msg("Run demon")
    dm = d.Demon(graph=G, epsilon=0.25, min_community_size=3)
    coms = dm.execute()
    return coms


def run_oslom2(path: str, weighted):
    debug.print_msg("Run Oslom")
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
        "-fast"
    ]

    # Somehow does not work with subprocess.run
    command_line = " ".join(command)
    os.system(command_line)


def run_wnw(G, weighted):
    debug.print_msg("O-HAMUHI")
    if nx.is_directed(G):
        return None
    elif weighted:
        comms_sets = WMW.weighted_weak_communities(G, weight='weight')
    else:
        comms_sets = WMW.weighted_weak_communities(G)

    # Convert to lists
    communities = []
    for comm in comms_sets:
        communities.append(list(comm))
    return communities


def run_link(edges_path: str, result_dir: str, weighted: bool):
    LinkCommunity.detect_communities(None, weighted, None, result_dir, edges_path)

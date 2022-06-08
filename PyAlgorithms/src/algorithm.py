import os
import subprocess
import demon as d
import networkx as nx
import external.weighted_weak_communities

OSLOM_BIN = os.path.abspath("../../Algo_Oslom/x64/Debug")
CFINDER_BIN = os.path.abspath("../../Algo_CFinder")


def run_demon(G):
    dm = d.Demon(graph=G, epsilon=0.25, min_community_size=3)
    coms = dm.execute()
    return coms


def run_oslom(path: str, weighted=False):
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


def run_cfinder(path):
    command = [
        os.path.join(CFINDER_BIN, "CFinder_commandline.exe"),
        "-i", path,
        "-l", os.path.join(CFINDER_BIN, "licence.txt")
    ]
    subprocess.run(command, shell=True, check=True)


def run_wnw(G):
    if nx.is_directed(G):
        return None
    else:
        comms_sets = external.weighted_weak_communities.weighted_weak_communities(G)

    # Convert to lists
    communities = []
    for comm in comms_sets:
        communities.append(list(comm))
    return communities

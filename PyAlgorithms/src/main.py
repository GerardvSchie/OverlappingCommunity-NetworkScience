import networkx as nx
import demon as d
import oslom
import matplotlib.pyplot as plt
from argparse import Namespace

def run_demon():
    g = nx.karate_club_graph()
    dm = d.Demon(graph=g, epsilon=0.25, min_community_size=3)
    coms = dm.execute()
    return coms

def visual_graph():
    G = nx.karate_club_graph()
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(run_demon())
    visual_graph()

# # run OSLOM with files already on disk
# args = Namespace()
# args.edges = "/path/to/input_edges.tsv"
# args.output_clusters = "/path/to/output_clusters.json"
# args.oslom_output = "/path/to/oslom_aux_files"
# args.min_cluster_size = oslom.DEF_MIN_CLUSTER_SIZE
# args.oslom_exec = oslom.DEF_OSLOM_EXEC
# args.oslom_args = oslom.DEF_OSLOM_ARGS
# oslom.run(args)

# run OSLOM with data in Python objects
args = Namespace()
args.min_cluster_size = 0
args.oslom_exec = oslom.DEF_OSLOM_EXEC
args.oslom_args = oslom.DEF_OSLOM_ARGS

# edges is an iterable of tuples (source, target, weight)
# in the same format as the command-line version
edges = [(0, 1, 1.0), (1, 2, 1), (2, 0, 1)]
clusters = oslom.run_in_memory(args, edges)
print(clusters)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

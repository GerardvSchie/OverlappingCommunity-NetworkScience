import os
import benchmark
import algorithm
import measure
import results
import utils
import numpy as np
import shutil


def create_graph(weighted:bool, N:int, Om:int, On:int) -> (str, str):
    # Create a synthetic network with given name
    # Generate graph using LFR benchmark
    graph_name = f"N{N}_Om{Om}_On{On}"
    if weighted:
        graph_name = "W_" + graph_name
    else:
        graph_name = "UW_" + graph_name

    graph_path = os.path.join("..", "networks", graph_name)
    result_dir = os.path.abspath(os.path.join(graph_path, "results"))

    # Create directories
    utils.create_dir(os.path.join("..", "networks"))
    utils.create_dir(graph_path)
    utils.create_dir(result_dir)

    # Graph already exists
    if not (os.path.exists(os.path.join(graph_path, "community.dat")) and os.path.exists(os.path.join(graph_path, "network.dat")) and os.path.exists(os.path.join(graph_path, f"statistics.dat"))):
        # k=20, kmax 50, cmin 20, cmax 100, tow1 -2, tow2 = -1, mixing = 0.4 Om=2, nr overlapping nodes = On/n
        # n = 1000-10000 dn=1000 Om=1-8 dOm=1 On/n 0.1-0.6 dOn/n=0.1
        benchmark.create_graph(
            weighted=weighted,
            N=N,
            k=23, #k=20
            maxk=30, #maxk=50
            mixing_topology=0.4,
            mixing_weights=0.1,
            tow1=-2,
            tow2=-1,
            minc=20,
            maxc=100,
            on=On,
            om=Om,
            graph_dir=graph_path
        )

    # Copy over communities and network file
    if not os.path.exists(os.path.join(result_dir, "community.dat")) or not os.path.exists(os.path.join(result_dir, "network.dat")):
        # Convert community file to NMI format
        benchmark.community_to_nmi_file(graph_path)
        utils.copy_edge_file(graph_path)

    return graph_name, result_dir


# Test method
def test_graph(weighted: bool, result_dir: str) -> None:
    # Read the graph from the generated edge file into nx graph
    edges_path = os.path.join(result_dir, "network.dat")
    G = benchmark.read_graph(weighted, edges_path)
    # print(G.edges(data=True))

    # WNW
    # if not os.path.exists(os.path.join(result_dir, "wnw.dat")):
    wnw_communities = algorithm.run_wnw(G, weighted='weighted')
    utils.communities_to_file(result_dir, wnw_communities, "wnw")

    # DEMON
    # if not os.path.exists(os.path.join(result_dir, "demon.dat")):
    # demon_communities = algorithm.run_demon(G)
    # utils.communities_to_file(result_dir, demon_communities, "demon")

    # OSLOM2
    # if not os.path.exists(os.path.join(result_dir, "oslom2.dat")):
    # algorithm.run_oslom2(edges_path, weighted)
    # utils.copy_without_comments(os.path.join(result_dir, "network.dat_oslo_files", "tp"),
    #                             os.path.join(result_dir, "oslom2.dat"))

    # # Visualize the network
    # visual_graph(G)


# Get the 3 measurements of the algorithms
def get_scores(result_dir, graph_name):
    algos = ["demon", "oslom2", "wnw"]
    result_file = os.path.join(result_dir, "result.dat")
    prev_algorithms_results = []

    # Read which results are already available
    if os.path.exists(result_file):
        with open(result_file, "r") as file:
            prev_algorithms_results = [line.split(",")[0] for line in file.readlines()]

    # Don't get results that are already present
    for element in prev_algorithms_results:
        if element in algos:
            algos.remove(element)
    if not algos:
        return

    with open(result_file, "a") as file:
        file.write("algo, nmi, omega, nf1\n")
        for algo in algos:
            if os.path.exists(os.path.join(result_dir, algo + ".dat")):
                nmi_score = measure.get_nmi_score(graph_name, algo)
                omega_index = measure.get_omega_score(result_dir, algo)
                avg_f1 = measure.get_average_f1_score(result_dir, algo)
                # Write these results in the file
                file.write(f"{algo},{nmi_score},{omega_index},{avg_f1}\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # results.collect_results()

    weighted = True
    graph_name, result_dir = create_graph(weighted, N=200, Om=0, On=0)
    test_graph(weighted, result_dir)
    get_scores(result_dir, graph_name)
    raise Exception("Fast stop")

    default_n = 3000
    default_Om = 3
    default_On_frac = 0.3

    # Change the n parameter
    for n in np.arange(1000, 11000, 1000):
        # print("n:" + str(n))
        On = int(default_On_frac * n)
        graph_name, result_dir = create_graph(True, N=n, Om=default_Om, On=On)
        test_graph(True, result_dir)
        get_scores(result_dir, graph_name)
        raise Exception("Fast stop")

    # for Om in np.arange(1, 9, 1):
    for Om in np.arange(1, 7, 1):
        On = int(default_On_frac * default_n)
        graph_name, result_dir = create_graph(True, N=default_n, Om=Om, On=On)
        test_graph(True, result_dir)
        get_scores(result_dir, graph_name)
        # print("Om:" + str(Om))

    for on_frac in np.arange(0.1, 0.7, 0.1):
        On = int(default_n * on_frac)
        # print("On" + str(On))
        graph_name, result_dir = create_graph(True, N=default_n, Om=default_Om, On=On)
        test_graph(True, result_dir)
        get_scores(result_dir, graph_name)

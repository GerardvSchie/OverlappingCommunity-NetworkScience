import os
import benchmark
import algorithm
import measure
import visualize
import results
import utils
import numpy as np


def create_graph(weighted:bool, N:int, Om:int, On:int) -> (str, str):
    # Create a synthetic network with given name
    # Generate graph using LFR benchmark
    graph_name = f"N{N}_Om{Om}_On{On}"
    if weighted:
        graph_name = "W_" + graph_name
    else:
        graph_name = "UW_" + graph_name

    graph_path = os.path.join("..", "synthetic_networks", graph_name)
    result_dir = os.path.join(graph_path, "results")

    # Create directories
    utils.create_dir(os.path.join("..", "synthetic_networks"))
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

    if weighted:
        weighted_flag = 'weight'
    else:
        weighted_flag = None

    # WNW
    if not os.path.exists(os.path.join(result_dir, "wnw.dat")):
        wnw_communities = algorithm.run_wnw(G, weighted=weighted_flag)
        utils.communities_to_file(result_dir, wnw_communities, "wnw")

    # DEMON
    if not os.path.exists(os.path.join(result_dir, "demon.dat")):
        demon_communities = algorithm.run_demon(G)
        utils.communities_to_file(result_dir, demon_communities, "demon")

    # OSLOM2
    if not os.path.exists(os.path.join(result_dir, "oslom2.dat")):
        algorithm.run_oslom2(edges_path, weighted)
        utils.copy_without_comments(os.path.join(result_dir, "network.dat_oslo_files", "tp"),
                                    os.path.join(result_dir, "oslom2.dat"))

    # # Visualize the network
    # visual_graph(G)


# Get the 3 measurements of the algorithms
def get_scores(synthetic: bool, result_dir: str, graph_name: str):
    algos = ["demon", "oslom2", "wnw", "ground_truth"]
    result_file = os.path.join(result_dir, "result.dat")
    computed_results_name = []

    result_existed = False
    # Read which results are already available
    if os.path.exists(result_file):
        with open(result_file, "r") as file:
            result_existed = True
            computed_results_name = [line.split(",")[0] for line in file.readlines()]

    # Don't get results that are already present
    for element in computed_results_name:
        if element in algos:
            algos.remove(element)
    if not algos:
        return

    # Append the results to the results.dat file
    with open(result_file, "a") as file:
        if not result_existed:
            file.write("algo, nmi, omega, nf1, nr_communities\n")
        for algo in algos:
            # For ground truth only the number of communities needs to get measured
            if algo == "ground_truth":
                nr_communities = measure.get_number_communities(result_dir, "community")
                file.write(f"{algo},{nr_communities}\n")
            # For all other algorithms, all measures have to be taken
            elif os.path.exists(os.path.join(result_dir, algo + ".dat")):
                nmi_score = measure.get_nmi_score(synthetic, graph_name, algo)
                omega_index = measure.get_omega_score(result_dir, algo)
                avg_f1 = measure.get_average_f1_score(result_dir, algo)
                nr_communities = measure.get_number_communities(result_dir, algo)
                # Write these results in the file
                file.write(f"{algo},{nmi_score},{omega_index},{avg_f1},{nr_communities}\n")


# Runs synthetic networks, weighted parameter denotes whether the syntehtic networks should have weighted edges
def run_synthetic_networks(weighted: bool):
    results.collect_synthetic_results()
    # visualize.plot_results(weighted, "synthetic")

    # Base parameters
    default_n = 3000
    default_Om = 3
    default_On_frac = 0.3

    # Change the n parameter
    for n in np.arange(1000, 7000, 1000):
        On = int(default_On_frac * n)
        graph_name, result_dir = create_graph(weighted, N=n, Om=default_Om, On=On)
        test_graph(weighted, result_dir)
        get_scores(True, result_dir, graph_name)
        raise Exception("Fast stop")

    for Om in np.arange(1, 7, 1):
        On = int(default_On_frac * default_n)
        graph_name, result_dir = create_graph(weighted, N=default_n, Om=Om, On=On)
        test_graph(weighted, result_dir)
        get_scores(True, result_dir, graph_name)

    for on_frac in np.arange(0.1, 0.7, 0.1):
        On = int(default_n * on_frac)
        graph_name, result_dir = create_graph(weighted, N=default_n, Om=default_Om, On=On)
        test_graph(weighted, result_dir)
        get_scores(True, result_dir, graph_name)

    # Algorithm is done running, collect the latest results and write it to the file
    results.collect_synthetic_results()


def run_real_networks():
    for name in ["PPI-D1", "PPI-D2"]:
        # Create directories
        graph_path = os.path.join("..", "real_networks", name)
        result_dir = os.path.join(graph_path, "results")
        utils.create_dir(result_dir)

        mapping = utils.get_node_mapping(graph_path)
        # Move files to result folder
        utils.copy_communities_with_mapping(graph_path, mapping)
        utils.copy_edge_file(graph_path, mapping)

        # Test the graph
        test_graph(True, result_dir)
        get_scores(False, result_dir, name)

    # Such a short run, no need to collect results from last run
    results.collect_real_results()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # run_real_networks()
    run_synthetic_networks(weighted=False)
    # run_synthetic_networks(weighted=True)

import os
import benchmark
import algorithm
import measure
import visualize
import results
import utils
import numpy as np

expected_fields = [
    "demon_nmi", "demon_omega-index", "demon_number-communities",
    "oslom2_nmi", "oslom2_omega-index", "oslom2_number-communities",
    "O-HAMUHI_nmi", "O-HAMUHI_omega-index", "O-HAMUHI_number-communities",
    "ground-truth_number-communities"
]


def create_graph(nr_run: int, weighted: bool, N: int, Om: int, On: int) -> (str, str):
    # Create a synthetic network with given name
    # Generate graph using LFR benchmark
    graph_name = f"N{N}_Om{Om}_On{On}_{nr_run}"
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
            k=6, #k=20
            maxk=35, #maxk=50
            mixing_topology=0.4,
            mixing_weights=0.1,
            tow1=-2,
            tow2=-1,
            minc=4,
            maxc=100,
            on=On,
            om=Om,
            graph_dir=graph_path
        )

    # Copy over communities and network file
    if not os.path.exists(os.path.join(result_dir, "ground-truth.dat")) or not os.path.exists(os.path.join(result_dir, "network.dat")):
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

    # LinkCommunities
    if not os.path.exists(os.path.join(result_dir, "link.dat")):
        algorithm.run_link(edges_path, result_dir, weighted)

    # # Visualize the network
    # visual_graph(G)


# Get the 3 measurements of the algorithms
def get_scores(synthetic: bool, result_dir: str, graph_name: str):
    fields_to_compute = expected_fields
    result_file = os.path.join(result_dir, "result.dat")

    # Read which results are already computed
    if os.path.exists(result_file):
        with open(result_file, "r") as file:
            for line in file.readlines():
                if not line:
                    continue

                fields_to_compute.remove(line.strip().split(",")[0])

    # Everything had already been computed
    if len(fields_to_compute) == 0:
        return

    # Compute and append the to-be-computed fields to the results.dat file
    with open(result_file, "a") as file:
        for field in fields_to_compute:
            algo, measure = field.split("_")[:1]

            # For each measure that still need to be computed do so
            if measure == "number-communities":
                nr_communities = measure.get_number_communities(result_dir, algo)
                file.write(f"{algo}_{measure},{nr_communities}")
            elif measure == "nmi":
                nmi_score = measure.get_nmi_score(synthetic, graph_name, algo)
                file.write(f"{algo}_{measure},{nmi_score}")
            elif measure == "omega-index":
                omega_index = measure.get_omega_score(result_dir, algo)
                file.write(f"{algo}_{measure},{omega_index}")
            else:
                raise NotImplementedError("Measure not implemented")

# Runs synthetic networks, weighted parameter denotes whether the syntehtic networks should have weighted edges
def run_synthetic_networks(weighted: bool):
    results.collect_synthetic_results()
    # visualize.plot_results(weighted, "synthetic")

    # Base parameters
    default_n = 800
    default_Om = 2
    default_On_frac = 0.20

    # Run experiment set 5 times
    for nr_run in np.arange(1, 6, 1):
        # Change the n parameter
        for n in np.arange(100, 2000, 200):
            On = int(default_On_frac * n)
            graph_name, result_dir = create_graph(nr_run, weighted, N=n, Om=default_Om, On=On)
            test_graph(weighted, result_dir)
            get_scores(True, result_dir, graph_name)
            raise Exception("Fast stop")

        for Om in np.arange(1, 6, 1):
            On = int(default_On_frac * default_n)
            graph_name, result_dir = create_graph(nr_run, weighted, N=default_n, Om=Om, On=On)
            test_graph(weighted, result_dir)
            get_scores(True, result_dir, graph_name)

        for on_frac in np.arange(0.1, 0.6, 0.1):
            On = int(default_n * on_frac)
            graph_name, result_dir = create_graph(nr_run, weighted, N=default_n, Om=default_Om, On=On)
            test_graph(weighted, result_dir)
            get_scores(True, result_dir, graph_name)

    # Algorithm is done running, collect the latest results and write it to the file
    results.collect_synthetic_results()


def run_real_networks():
    for name, weighted in [("PPI-D1", True), ("PPI-D2", True), ("Facebook-ego", False)]:
        # Create directories
        graph_path = os.path.join("..", "real_networks", name)
        result_dir = os.path.join(graph_path, "results")
        utils.create_dir(result_dir)

        mapping = utils.get_node_mapping(graph_path, weighted)
        # Move files to result folder
        utils.copy_communities_with_mapping(graph_path, mapping)
        utils.copy_edge_file(graph_path, mapping)

        # Test the graph
        test_graph(weighted, result_dir)
        get_scores(False, result_dir, name)

    # Such a short run, no need to collect results from last run
    results.collect_real_results()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_real_networks()
    # run_synthetic_networks(weighted=False)
    # run_synthetic_networks(weighted=True)

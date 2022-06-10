import os
import benchmark
import algorithm
import measure
import results
import utils
import numpy as np
import shutil


def create_graph(N:int, Om:int, On:int) -> (str, str):
    # Create a synthetic network with given name
    # Generate graph using LFR benchmark executable
    graph_name = f"N{N}_Om{Om}_On{On}"
    graph_path = os.path.join("..", "networks", graph_name)
    utils.create_dir(graph_path)
    result_dir = os.path.abspath(os.path.join(graph_path, "results"))
    utils.create_dir(result_dir)

    # Graph already exists
    if not (os.path.exists(os.path.join(graph_path, f"{graph_name}.cnl")) and os.path.exists(os.path.join(graph_path, f"{graph_name}.nse")) and os.path.exists(os.path.join(graph_path, f"{graph_name}.nst"))):
        # k=20, kmax 50, cmin 20, cmax 100, tow1 -2, tow2 = -1, mixing = 0.4 Om=2, nr overlapping nodes = On/n
        # n = 1000-10000 dn=1000 Om=1-8 dOm=1 On/n 0.1-0.6 dOn/n=0.1
        benchmark.create_graph(
            N=N,
            k=17, #k=20
            maxk=30, #maxk=50
            mixing_topology=0.4,
            mixing_weights=0,
            tow1=-2,
            tow2=-1,
            minc=20,
            maxc=100,
            on=On,
            om=Om,
            name=graph_name,
            result_dir=result_dir
        )

    # Copy over communities and edges file
    filename = os.path.join("..", "networks", str(graph_name), str(graph_name))
    if not os.path.exists(os.path.join(result_dir, "communities.dat")) or not os.path.exists(os.path.join(result_dir, "edges.dat")):
        shutil.copyfile(filename + ".cnl", os.path.join(result_dir, "communities.dat"))
        utils.copy_without_comments(os.path.abspath(filename) + ".nse", os.path.join(result_dir, "edges.dat"))

    return graph_name, result_dir


# Test method
def test_graph(graph_name, result_dir) -> None:
    # Read the graph from the generated edge file into nx graph
    edges_path = os.path.join("..", "networks", str(graph_name), "results", "edges.dat")
    G = benchmark.read_graph(edges_path, weighted=True)

    # WNW
    if not os.path.exists(os.path.join(result_dir, "wnw.dat")):
        wnw_communities = algorithm.run_wnw(G)
        utils.communities_to_file(result_dir, wnw_communities, "wnw")

    # DEMON
    if not os.path.exists(os.path.join(result_dir, "demon.dat")):
        demon_communities = algorithm.run_demon(G)
        utils.communities_to_file(result_dir, demon_communities, "demon")

    # OSLOM2
    if not os.path.exists(os.path.join(result_dir, "oslom2.dat")):
        algorithm.run_oslom2(edges_path, True)
        utils.copy_without_comments(os.path.join("..", "networks", graph_name, "results", "edges.dat_oslo_files", "tp"),
                                    os.path.join(result_dir, "oslom2.dat"))

    # if not os.path.exists(os.path.join(result_dir, "cfinder.dat")):
    #     algorithm.run_native_cfinder(G)
    #     algorithm.run_cfinder(graph_name, edges_path)
    #     utils.copy_without_comments(os.path.join("../networks", graph_name, "cfinder_run", "k=3", "communities"),
    #                                 os.path.join(result_dir, "cfinder.dat"))
    #     get_scores(result_dir, graph_name, "cfinder")

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
    results.collect_results()

    for n in np.arange(1000, 11000, 1000):
        # print("n:" + str(n))
        # for Om in np.arange(1, 9, 1):
        for Om in np.arange(1, 7, 1):
            # print("Om:" + str(Om))
            for on_frac in np.arange(0.1, 0.7, 0.1):
                On = int(n * on_frac)
                # print("On" + str(On))
                graph_name, result_dir = create_graph(N=n, Om=Om, On=On)
                test_graph(graph_name, result_dir)
                get_scores(result_dir, graph_name)

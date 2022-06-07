import os
import benchmark
import algorithm
import measure
import utils


# Test method
def test_method(result_dir, name) -> None:
    # Create a synthetic network with given name
    # Generate graph using LFR benchmark executable
    # create_graph(100, 5, 20, 0.1, 7, 20, graph_name, result_dir)

    # Read the graph from the generated edge file into nx graph
    path = os.path.join(result_dir, "edges.dat")
    G = benchmark.read_graph(path, weighted=True)
    algorithm.run_wnw(G, None)
    # DEMON
    # demon_communities = algorithm.run_demon(G)
    # utils.communities_to_file(result_dir, demon_communities, "demon")
    get_scores(result_dir, name, "demon")

    # OSLOM
    # algorithm.run_oslom(path)
    # utils.copy_without_comments(os.path.join(f"../networks", f"{name}.nse_oslo_files", "tp"),
    #                             os.path.join(result_dir, "oslom.dat"))
    get_scores(result_dir, name, "oslom")

    # Visualize the network
    # visual_graph(G)


# Get the 3 measurements of the algorithms
def get_scores(result_dir, graph_name, algo_name):
    print(f"NMI({algo_name}):" + str(measure.get_nmi_score(graph_name, algo_name)))
    print(f"Omega({algo_name}):" + str(measure.get_omega_score(result_dir, algo_name)))
    print(f"Avg F1({algo_name}): " + str(measure.get_average_f1_score(result_dir, algo_name)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    graph_name = "test100_15"
    result_dir = os.path.abspath(os.path.join("../networks", graph_name + "_results"))
    test_method(result_dir, graph_name)

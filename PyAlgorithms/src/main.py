import os
import benchmark
import algorithm
import measure
import utils


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Generate graph using LFR benchmark executable
    graph_name = "test100_15"
    result_dir = os.path.abspath(os.path.join("../networks", graph_name + "_results"))
    # utils.create_results_dir(result_dir)

    # create_graph(100, 5, 20, 0.1, 7, 20, graph_name, result_dir)

    # Read the graph from the generated edge file into nx graph
    path = os.path.join(result_dir, "edges.dat")
    G = benchmark.read_graph(path, weighted=True)

    # run_oslom(path)

    # Sanity check that it has been read
    # print("Degree distribution:")
    # print(nx.degree_histogram(G))
    #
    # # Detect communities on karate club network
    # KarateGraph = nx.karate_club_graph()
    demon_communities = algorithm.run_demon(G)
    utils.communities_to_file(result_dir, demon_communities, "demon")

    # NMI score
    # nmi_score = measure.get_nmi_score(graph_name, "demon.dat", "communities.dat")
    # print("NMI score demon and GT: " + str(nmi_score))

    measure.get_omega_score(result_dir, "demon")
    measure.get_average_f1_score(result_dir, "demon")
    #
    # # Visualize the network
    # visual_graph(G)

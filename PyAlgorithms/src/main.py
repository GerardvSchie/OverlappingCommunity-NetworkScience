import os
import benchmark
import algorithm
import measure
import utils


def create_graph() -> (str, str):
    # Create a synthetic network with given name
    # Generate graph using LFR benchmark executable
    graph_name = "N1000_k20_kmax50"
    graph_path = os.path.join("../networks", graph_name)
    utils.create_dir(graph_path)
    result_dir = os.path.abspath(os.path.join(graph_path, "results"))
    utils.create_dir(result_dir)

    # Graph already exists
    if os.path.exists(os.path.join(graph_path, f"{graph_name}.cnl")) and os.path.exists(os.path.join(graph_path, f"{graph_name}.nse")) and os.path.exists(os.path.join(graph_path, f"{graph_name}.nst")):
        return graph_name, result_dir

    # k=20, kmax 50, cmin 20, cmax 100, tow1 -2, tow2 = -1, mixing = 0.4 Om=2, nr overlapping nodes = On/n
    # n = 1000-10000 dn=1000 Om=1-8 dOm=1 On/n 0.1-0.6 dOn/n=0.1
    benchmark.create_graph(
        N=1000,
        k=17,
        maxk=30,
        mixing_topology=0.4,
        mixing_weights=0,
        tow1=-2,
        tow2=-1,
        minc=20,
        maxc=100,
        on=200,
        om=2,
        name=graph_name,
        result_dir=result_dir
    )

    # benchmark.create_graph(N=100, k=5, maxk=20, mixing_topology=0.1, minc=7, maxc=20, name=graph_name, result_dir=result_dir)

    # N: int, k: int, maxk: int, muw: float, minc: int, maxc: int, name: str
    return graph_name, result_dir


# Test method
def test_graph(graph_name, result_dir) -> None:
    # Read the graph from the generated edge file into nx graph
    edges_path = os.path.join(result_dir, "edges.dat")
    G = benchmark.read_graph(edges_path, weighted=True)

    # WNW
    if not os.path.exists(os.path.join(result_dir, "wnw.dat")):
        wnw_communities = algorithm.run_wnw(G)
        utils.communities_to_file(result_dir, wnw_communities, "wnw")
        # get_scores(result_dir, graph_name, "wnw")

    # DEMON
    if not os.path.exists(os.path.join(result_dir, "demon.dat")):
        demon_communities = algorithm.run_demon(G)
        utils.communities_to_file(result_dir, demon_communities, "demon")
        # get_scores(result_dir, graph_name, "demon")

    # OSLOM
    # algorithm.run_oslom(path, True)
    # utils.copy_without_comments(os.path.join("../networks", graph_name + ".nse_oslo_files", "tp"),
    #                             os.path.join(result_dir, "oslom.dat"))

    if not os.path.exists(os.path.join(result_dir, "oslom2.dat")):
        algorithm.run_oslom2(edges_path, True)
        utils.copy_without_comments(os.path.join("../networks", graph_name + ".nse_oslo_files", "tp"),
                                    os.path.join(result_dir, "oslom2.dat"))

    if not os.path.exists(os.path.join(result_dir, "cfinder.dat")):
        algorithm.run_native_cfinder(G)
        # algorithm.run_cfinder(graph_name, edges_path)
        # utils.copy_without_comments(os.path.join("../networks", graph_name, "cfinder_run", "k=3", "communities"),
        #                             os.path.join(result_dir, "cfinder.dat"))
        # get_scores(result_dir, graph_name, "cfinder")

    # # Visualize the network
    # visual_graph(G)


# Get the 3 measurements of the algorithms
def get_scores(result_dir, graph_name):
    algos = ["demon", "wnw"]
    for algo in algos:
        if os.path.exists(os.path.join(result_dir, algo + ".dat")):
            print(f"NMI({graph_name}{algo}):" + str(measure.get_nmi_score(graph_name, algo)))
            print(f"Omega({graph_name}{algo}):" + str(measure.get_omega_score(result_dir, algo)))
            print(f"Avg F1({graph_name}{algo}): " + str(measure.get_average_f1_score(result_dir, algo)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    graph_name, result_dir = create_graph()
    test_graph(graph_name, result_dir)
    get_scores(result_dir, graph_name)

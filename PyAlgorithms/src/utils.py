import os
import networkx as nx
import matplotlib.pyplot as plt


def copy_without_comments(in_path: str, res_path: str):
    # Input file does not exist
    if not os.path.exists(in_path):
        return

    with open(res_path, "w") as res_file:
        with open(in_path, "r") as file:
            for line in file:
                # Comment
                if line.startswith('#'):
                    continue
                res_file.write(line)


def create_dir(dir_path: str):
    exists = os.path.exists(dir_path)
    if not exists:
        os.makedirs(dir_path)


# Reads the file content and returns it
def read_file(file_path: str) -> [str]:
    with open(file_path, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return lines


def visual_graph(G):
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


def communities_to_file(result_dir: str, communities: [int], name: str) -> None:
    result_file = os.path.join(result_dir, name + ".dat")
    with open(result_file, "w") as file:
        for community in communities:
            for node in community:
                file.write(str(node) + " ")
            file.write("\n")


def communities_from_file(result_dir: str, name: str) -> dict[[str]]:
    # Get file and init resulting dict
    result_file = os.path.join(result_dir, name + ".dat")
    communities = dict()
    index = 1

    # Read the file
    with open(result_file, "r") as file:
        for line in file.readlines():
            if line == "":
                continue
            communities["Community" + str(index)] = line.split()
            index += 1

    # print(communities)
    return communities


def copy_edge_file(graph_path: str, mapping=None):
    with open(os.path.join(graph_path, "network.dat"), "r") as created_file:
        with open(os.path.join(graph_path, "results", "network.dat"), "w") as result_file:
            for line in created_file.readlines():
                line = line.strip()
                vals = line.split('\t')
                if mapping:
                    vals[0] = mapping[vals[0]]
                    vals[1] = mapping[vals[1]]

                if len(vals) == 2:
                    result_line = line
                elif vals[2] == '0':
                    continue
                elif 'e' in vals[2].lower():
                    result_line = f'{vals[0]}\t{vals[1]}\t{str(float(vals[2]))}'
                else:
                    result_line = line

                result_file.write(result_line + '\n')


def get_node_mapping(graph_path: str):
    mapping = dict()
    iterator = 1

    with open(os.path.join(graph_path, "network.dat"), "r") as file:
        for line in file.readlines():
            line = line.strip()
            node1, node2, _ = line.split('\t')
            if node1 not in mapping:
                mapping[node1] = str(iterator)
                iterator += 1
            if node2 not in mapping:
                mapping[node2] = str(iterator)
                iterator += 1

    with open(os.path.join(graph_path, "community.dat"), "r") as file:
        for line in file.readlines():
            line = line.strip()
            for node in line.split():
                if node not in mapping:
                    mapping[node] = str(iterator)
                    iterator += 1

    return mapping


def copy_communities_with_mapping(graph_path, mapping):
    with open(os.path.join(graph_path, "community.dat"), 'r') as in_file:
        with open(os.path.join(graph_path, "results", "community.dat"), 'w') as out_file:
            for line in in_file.readlines():
                line = line.strip()
                nodes = line.split()
                for node in nodes:
                    out_file.write(mapping[node] + ' ')
                out_file.write('\n')

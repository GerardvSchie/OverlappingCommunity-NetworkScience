import os
import networkx as nx
import matplotlib.pyplot as plt


def copy_without_comments(in_path: str, res_path: str):
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

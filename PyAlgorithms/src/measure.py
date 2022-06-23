import os
import subprocess
import utils
import omega_index_py3
from nf1 import NF1
import debug

NMI_BIN = os.path.abspath(os.path.join("..", "..", "Measure_NMI", "mutual"))
# MEASURES = ["nf1", "nmi", "omega-index", "number-communities"]
MEASURES = ["nmi", "omega-index", "number-communities"]

# Compute the NMI score
# https://sites.google.com/site/andrealancichinetti/mutual
def get_nmi_score(synthetic: bool, graph_name: str, output_name: str) -> float:
    debug.print_msg("Run NMI")
    assert os.path.exists(NMI_BIN)
    if synthetic:
        folder_name = "synthetic_networks"
    else:
        folder_name = "real_networks"

    command = [
        NMI_BIN,
        f"../{folder_name}/{graph_name}/results/ground-truth.dat",
        f"../{folder_name}/{graph_name}/results/{output_name}.dat"
    ]

    # Run the program that gets the NMI score
    process_result = subprocess.run(command, shell=False, capture_output=True, check=True)
    result_string = process_result.stdout.decode()

    # Retrieve it from the string and give it
    return float(result_string.strip().split("\t")[1])


# Compares omega score with the ground truth
def get_omega_score(results_dir: str, algo_output_name: str) -> float:
    debug.print_msg("Run Omega")
    ground_truth = utils.communities_from_file(results_dir, "ground-truth")
    output = utils.communities_from_file(results_dir, algo_output_name)

    o = omega_index_py3.Omega(output, ground_truth)
    return o.omega_score


# Computing the NF1 scores and statistics
def get_average_f1_score(results_dir: str, algo_output_name: str) -> float:
    debug.print_msg("Run NF1")
    ground_truth = utils.communities_from_file(results_dir, "ground-truth")
    output = utils.communities_from_file(results_dir, algo_output_name)

    nf = NF1(output, ground_truth)
    results = nf.summary()

    nf1 = results['details']['F1 mean'][0]
    return nf1

    # Visualising the Precision-Recall density scatter-plot
    # nf.plot()


def get_number_communities(results_dir: str, algo_output_name: str) -> int:
    nr_communities = 0

    # Count number of communities
    with open(os.path.join(results_dir, algo_output_name + ".dat"), "r") as file:
        for line in file.readlines():
            line = line.strip()
            if line:
                nr_communities += 1

    return nr_communities
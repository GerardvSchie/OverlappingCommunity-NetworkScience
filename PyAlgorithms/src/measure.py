import os
import subprocess
import utils
import omega_index_py3
from nf1 import NF1

NMI_BIN = os.path.abspath("../../Measure_NMI/x64/Debug")


# # Create the graph using LFR-benchmark
# def get_nmi_score(graph_name, file1: str, file2: str) -> float:
#     command = [
#         os.path.join(NMI_BIN, "NMI_Measure.exe"),
#         "../networks/test100_15_results/communities.dat",
#         "../networks/test100_15_results/demon.dat"
#     ]
#     # process_result = subprocess.run(command, shell=True, check=False)
#     process_result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
#     result_string = process_result.stdout.decode()
#     print("string: " + result_string)
#     result = float(result_string.strip().split("\t")[1])
#     print("NMI score: " + str(result))
#     return result


# Create the graph using LFR-benchmark
def get_nmi_score(graph_name, file1: str, file2: str) -> float:
    command = [
        os.path.join(NMI_BIN, "NMI_Measure.exe"),
        f"../networks/{graph_name}_results/{file1}",
        f"../networks/{graph_name}_results/{file1}"
    ]

    # Run the program that gets the NMI score
    process_result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
    result_string = process_result.stdout.decode()

    # Retrieve it from the string and give it
    return float(result_string.strip().split("\t")[1])


# Compares omega score with the ground truth
def get_omega_score(results_dir:str, algo_output_name):
    ground_truth = utils.communities_from_file(results_dir, "communities")
    output = utils.communities_from_file(results_dir, algo_output_name)

    o = omega_index_py3.Omega(output, ground_truth)
    omega = o.omega_score
    print("Omega: " + str(omega))
    return omega


def get_average_f1_score(results_dir:str, algo_output_name):
    # Computing the NF1 scores and statistics
    ground_truth = utils.communities_from_file(results_dir, "communities")
    output = utils.communities_from_file(results_dir, algo_output_name)

    nf = NF1(output, ground_truth)
    results = nf.summary()

    # print(results['scores'])
    details = results['details']
    print(details)
    nf1 = results['details']['F1 mean'][0]
    print("NF1 score: " + str(nf1))
    return nf1

    # Visualising the Precision-Recall density scatter-plot
    # nf.plot()

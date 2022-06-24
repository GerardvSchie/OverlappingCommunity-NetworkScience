import os
import utils


def collect_synthetic_results():
    collect_results("synthetic")


def collect_real_results():
    collect_results("real")


def collect_results(dir_name):
    data_path = os.path.join("..", dir_name + "_results.dat")

    # Open file where the results will be written into
    with open(data_path, "w") as dat_file:
        network_dir = os.path.join("..", dir_name + "_networks")

        # Create dir if it's not yet present
        utils.create_dir(network_dir)

        network_names = [name for name in os.listdir(network_dir) if os.path.isdir(os.path.join(network_dir, name))]

        # Each network name
        for name in network_names:
            results_file_path = os.path.join(network_dir, name, "results", "result.dat")

            # Results file does not exist
            if not os.path.exists(results_file_path):
                continue

            # Read the results from each individual algorithm
            with open(results_file_path, "r") as file:
                for line in file.readlines():
                    dat_file.write(name + "," + line)

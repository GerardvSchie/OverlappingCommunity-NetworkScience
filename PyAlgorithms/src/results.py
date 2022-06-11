import os

results_path = os.path.join("..", "results.dat")


def collect_results():
    data_path = os.path.join("..", "results.dat")
    missing_names = []

    # Open file where the results will be written into
    with open(data_path, "w") as dat_file:
        network_dir = os.path.join("..", "networks")
        network_names = [name for name in os.listdir(network_dir) if os.path.isdir(os.path.join(network_dir, name))]

        # Each network name
        for name in network_names:
            results_file_path = os.path.join(network_dir, name, "results", "result.dat")

            # Results file does not exist
            if not os.path.exists(results_file_path):
                missing_names.append(name)
                continue

            # Read the results from each individual
            with open(results_file_path, "r") as file:
                lines = file.readlines()[1:]
                lines = [line.strip().split(",") for line in lines]
                lines = sorted(lines, key=lambda x: x[0])
                lines = [line[1:] for line in lines]
                concat_list = ",".join([j for i in lines for j in i])
                dat_file.write(name + "," + concat_list + "\n")

    # Print all the directories that did not have results
    print(f"missing result files: {missing_names}")

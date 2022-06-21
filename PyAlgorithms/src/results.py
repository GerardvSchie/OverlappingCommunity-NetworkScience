import os


def collect_synthetic_results():
    collect_results("synthetic")


def collect_real_results():
    collect_results("real")


def collect_results(dir_name):
    missing_names = []
    data_path = os.path.join("..", dir_name + "_results.dat")

    # Open file where the results will be written into
    with open(data_path, "w") as dat_file:
        dat_file.write("config_name, demon_nmi, demon_omega, demon_nf1, demon_nr_comms, gt_nr_comms, oslom_nmi, oslom_omega, oslom_nf1, oslom_nr_comms, wnw_nmi, wnw_omega, wnw_nf1, demon_nr_comms\n")

        network_dir = os.path.join("..", dir_name + "_networks")
        network_names = [name for name in os.listdir(network_dir) if os.path.isdir(os.path.join(network_dir, name))]

        # Each network name
        for name in network_names:
            results_file_path = os.path.join(network_dir, name, "results", "result.dat")

            # Results file does not exist
            if not os.path.exists(results_file_path):
                missing_names.append(name)
                continue

            # Read the results from each individual algorithm
            with open(results_file_path, "r") as file:
                lines = file.readlines()[1:]
                lines = [line.strip().split(",") for line in lines]
                lines = sorted(lines, key=lambda x: x[0])
                lines = [line[1:] for line in lines]
                concat_list = ",".join([j for i in lines for j in i])
                dat_file.write(name + "," + concat_list + "\n")

    # Print all the directories that did not have results
    print(f"missing result files: {missing_names}")

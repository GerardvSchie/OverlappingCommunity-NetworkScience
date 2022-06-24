import os
import re
import utils
import numpy as np
import matplotlib.pyplot as plt
import measure
import algorithm

configuration = r'^((U?)W_N(\d+)_Om(\d+)_On(\d+))_(\d+)'


# Collects results into dictionaries
def collect_bins(weighted: bool, prefix: str):
    # Skip column names of file since those are column names
    results_file = os.path.join("..", prefix + "_results.dat")
    if not results_file:
        print("There are no results yet, it will first generate them")
        return None, None, None

    lines = utils.read_file(results_file)

    N_runs = dict()
    Om_runs = dict()
    On_runs = dict()

    for line in lines:
        # Read the configuration values
        match = re.match(configuration, line)
        name, uw, n, om, on, nr_run = match[1], match[2], int(match[3]), int(match[4]), int(match[5]), int(match[6])

        # Only consider the weighted results when we are trying to plot them
        if uw and weighted:
            continue
        elif not uw and not weighted:
            continue

        # Configuration name as first and all the values after to floats
        _, parameter, value = line.split(",")[:3]
        value = float(value)

        on_frac = on / n

        # Put the results in each figure
        if n != 700:
            add_value(N_runs, parameter, n, value)
        elif om != 3:
            add_value(Om_runs, parameter, om, value)
        elif on_frac != 0.2:
            add_value(On_runs, parameter, on, value)
        # The default values for parameters go in each plot
        else:
            # Add list if it didnt exist yet
            add_value(N_runs, parameter, n, value)
            add_value(Om_runs, parameter, om, value)
            add_value(On_runs, parameter, on, value)

    return N_runs, On_runs, Om_runs


def add_value(data_dict, parameter, x, value):
    if not (parameter, x) in data_dict:
        data_dict[(parameter, x)] = []
    data_dict[(parameter, x)].append(value)


def plot_results(weighted: bool, prefix: str):
    N_runs, On_runs, Om_runs = collect_bins(weighted, prefix)

    plot_dir = os.path.join("..", "plots")
    utils.create_dir(plot_dir)

    # Plot title
    if weighted:
        title_prefix = "Weighted network "
    else:
        title_prefix = "Unweighted network "

    for measure_name in measure.MEASURES:
        fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 3))
        fig.suptitle(title_prefix + measure_name.replace("-", " "))

        # Plot information for each variable
        plot_data(axs[0], "Variable community size", "N", measure_name, N_runs)
        plot_data(axs[1], "Variable number of overlapping nodes", "On", measure_name, On_runs)
        plot_data(axs[2], "Variable number of communities", "Om", measure_name, Om_runs)

        # Put legend right of the figure
        box = axs[-1].get_position()
        axs[-1].set_position([box.x0, box.y0, box.width * 0.96, box.height])
        axs[-1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()

        # Save plot to file
        file_name = (title_prefix + measure_name + ".png").replace(" ", "")
        plt.savefig(os.path.join(plot_dir, file_name))

    # return N_runs, On_runs, Om_runs


def plot_data(ax, title: str, x_label: str, measure_name: str, data: dict):
    xs = []
    ys = [[] for _ in range(len(algorithm.ALGOS))]
    y_stderr = [[] for _ in range(len(algorithm.ALGOS))]

    data_list = sorted(list(data.items()), key=lambda item: item[0][1])

    prev_x = -1
    # Go through each
    for ((parameter, x), values) in data_list:
        # Add each unique x
        if x != prev_x:
            xs.append(x)
            prev_x = x

        parameter_algo, parameter_measure = parameter.split("_")
        # Not of the current measure
        if parameter_measure != measure_name:
            continue

        index = algorithm.ALGOS.index(parameter_algo)
        y_mean = sum(values) / float(len(values))
        ys[index].append(y_mean)

        y_std = np.std(values, ddof=1)
        y_err = y_std / np.sqrt(len(values))
        y_stderr[index].append(y_err)


    # Set labels
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(measure_name.replace("-", " "))

    if x_label == "N":
        ax.set_xticks(xs[::2])
    else:
        ax.set_xticks(xs)

    # Plot the information
    ax.plot(xs, ys[0], linestyle='solid', marker='o', color='red', label=algorithm.ALGOS[0])
    ax.errorbar(xs, ys[0], yerr=y_stderr[0], fmt=".k")
    ax.plot(xs, ys[1], linestyle='dotted', marker='^', color='orange', label=algorithm.ALGOS[1])
    ax.errorbar(xs, ys[1], yerr=y_stderr[1], fmt=".k")
    ax.plot(xs, ys[2], linestyle='dashdot', marker='s', color='green', label=algorithm.ALGOS[2])
    ax.errorbar(xs, ys[2], yerr=y_stderr[2], fmt=".k")
    # ax.plot(xs, ys[3], linestyle='dashed', marker='v', color='purple', label=algorithm.ALGOS[3], markerfacecolor="None")

    ax.grid(axis='y')

    if len(ys[-1]) != 0:
        ax.plot(xs, ys[-1], linestyle='dashed', marker='*', color='blue', label=algorithm.ALGOS[-1].replace("-", " "))
        ax.errorbar(xs, ys[-1], yerr=y_stderr[-1], fmt=".k")
    else:
        ax.set_yticks(np.arange(0, 1.1, 0.2))
        # plt.ylim([0, 1])

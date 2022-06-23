import os
import re
import utils
import numpy as np
import matplotlib.pyplot as plt

configuration = r'^(U?)W_N(\d+)_Om(\d+)_On(\d+)_(\d+)'


def plot_results(weighted: bool, prefix: str):
    # Skip column names of file since those are column names
    results_file = os.path.join("..", prefix + "_results.dat")
    if not results_file:
        print("There are no results yet, it will first generate them")
        return

    lines = utils.read_file(results_file)[1:]

    N_runs = dict()
    Om_runs = dict()
    On_runs = dict()

    for line in lines:
        # Read the configuration values
        match = re.match(configuration, line)
        uw, n, om, on, nr_run = match[1], int(match[2]), int(match[3]), int(match[4]), int(match[5])

        # Only consider the weighted results when we are trying to plot them
        if uw and weighted:
            continue
        elif not uw and not weighted:
            continue

        # Configuration name as first and all the values after to floats
        name, *csv_values = line.split(",")
        csv_values = [float(value) for value in csv_values]

        on_frac = on / n

        # Put the results in each figure
        if n != 3000:
            N_runs[(name, n, nr_run)] = csv_values
        elif om != 3:
            Om_runs[(name, om, nr_run)] = csv_values
        elif on_frac != 0.3:
            On_runs[(name, on, nr_run)] = csv_values
        # The default values for parameters go in each plot
        else:
            On_runs[(name, on, nr_run)] = csv_values
            Om_runs[(name, om, nr_run)] = csv_values
            N_runs[(name, n, nr_run)] = csv_values

    # Plot title
    if weighted:
        title_prefix = "Weighted network "
    else:
        title_prefix = "Unweighted network "

    for measure in [("NMI", [0, 5, 9]), ("Omega Index", [1, 6, 10]), ("number of communities", [3, 4, 8, 12])]:
        fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 3))
        fig.suptitle(title_prefix + measure[0])

        # Plot information for each variable
        plot(axs[0], "Variable community size", "N", measure[0], measure[1], N_runs)
        plot(axs[1], "Variable number of overlapping nodes", "On", measure[0], measure[1], On_runs)
        plot(axs[2], "Variable number of communities", "Om", measure[0], measure[1], Om_runs)

        # Put legend right of the figure
        box = axs[-1].get_position()
        axs[-1].set_position([box.x0, box.y0, box.width * 0.96, box.height])
        axs[-1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()

        # Save plot to file
        file_name = title_prefix + measure[0] + ".png"
        file_name = file_name.replace(" ", "")
        plt.savefig(os.path.join("..", "plots", file_name))

    return N_runs, On_runs, Om_runs


def plot(ax, title: str, x_label: str, y_label: str, indexes: [int], data: dict):
    xs = []
    ys = (dict(), dict(), dict(), dict())

    data_list = sorted(list(data.items()), key=lambda item: item[0][1])

    for ((_, param, nr_run), values) in data_list:
        for index in range(len(indexes)):
            if not ys[index][param]:
                ys[index][param] = []
            ys[index][param] = ys[index][param].append(values[index])

    ys = [for dic in ys]

    # Add data to y axis for each of the algorithms
    for ((_, param, nr_run), value) in data_list:
        xs.append(param)
        for index in range(len(indexes)):

            ys[index][(param, nr_run)] = value[index]

        # Put them into the 3 or 4 bins
        if len(indexes) == 4:
            for axis_list, index in [(ys1, indexes[0]), (ys2, indexes[2]), (ys3, indexes[3]), (ys4, indexes[1])]:
                axis_list.append(value[index])
        else:
            for axis_list, index in [(ys1, indexes[0]), (ys2, indexes[1]), (ys3, indexes[2])]:
                axis_list.append(value[index])

    # xs = np.array(xs)
    # ys1 = np.array(ys1)
    # ys2 = np.array(ys2)
    # ys3 = np.array(ys3)
    # ys4 = np.array(ys4)

    # Set labels
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Plot the information
    ax.plot(xs, ys1, '--o', color='red', label="Demon", markerfacecolor="None")
    ax.plot(xs, ys2, '-^', color='orange', label="Oslom", markerfacecolor="None")
    ax.plot(xs, ys3, '-.s', color='green', label="O-HAMUHI", markerfacecolor="None")

    ax.grid(axis='y')

    if len(ys4) != 0:
        ax.plot(xs, ys4, ':*', color='blue', label="ground truth", markerfacecolor="None")
        ax.set_ylim(bottom=0)
    else:
        ax.set_yticks(np.arange(0, 1.1, 0.2))
        # plt.ylim([0, 1])

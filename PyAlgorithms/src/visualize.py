import os
import re
import utils
import numpy as np
import matplotlib.pyplot as plt

configuration = r'^(U?)W_N(\d+)_Om(\d+)_On(\d+)'


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
        uw, n, om, on = match[1], int(match[2]), int(match[3]), int(match[4])

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
            N_runs[(name, n)] = csv_values
        elif om != 3:
            Om_runs[(name, om)] = csv_values
        elif on_frac != 0.3:
            On_runs[(name, on)] = csv_values
        # The default values for parameters go in each plot
        else:
            On_runs[(name, on)] = csv_values
            Om_runs[(name, om)] = csv_values
            N_runs[(name, n)] = csv_values

    if weighted:
        title_prefix = "Weighted Network "
    else:
        title_prefix = "Unweighted Network "

    for measure in [("NMI", [0, 5, 9]), ("Omega Index", [1, 6, 10])]:
        fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 3))
        # fig.subplots_adjust(top=0.8)
        fig.suptitle(title_prefix + measure[0])

        plot(axs[0], "Variable community size", "N", measure[0], measure[1], N_runs)
        plot(axs[1], "Variable number of overlapping nodes", "On", measure[0], measure[1], On_runs)
        plot(axs[2], "Variable number of communities", "Om", measure[0], measure[1], Om_runs)
        plt.tight_layout()
        plt.show()

    return N_runs, On_runs, Om_runs


def plot(ax, title: str, x_label: str, y_label: str, indexes: [int], data: dict):
    xs = []
    ys1 = []
    ys2 = []
    ys3 = []

    data = dict(sorted(data.items(), key=lambda item: item[1]))

    # Add data to y axis for each of the algorithms
    for name, value in data:
        xs.append(value)
        ys1.append(data[(name, value)][indexes[0]])
        ys2.append(data[(name, value)][indexes[1]])
        ys3.append(data[(name, value)][indexes[2]])

    xs = np.array(xs)
    ys1 = np.array(ys1)
    ys2 = np.array(ys2)
    ys3 = np.array(ys3)

    # Set labels
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Plot the information
    ax.plot(xs, ys1, '-o', label="Demon")
    ax.plot(xs, ys2, '-o', label="Oslom")
    ax.plot(xs, ys3, '-o', label="O-HAMUHI")

    ax.grid(axis='y')

    ax.set_yticks(np.arange(0, 1.1, 0.2))

    # Visualize the plot
    plt.legend()
    plt.ylim([0, 1])

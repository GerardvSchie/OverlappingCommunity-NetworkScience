import os
import re
import utils
import numpy as np
import matplotlib.pyplot as plt

configuration = r'^(U?)W_N(\d+)_Om(\d+)_On(\d+)'


def plot_results():
    # Skip column names of file since those are column names
    lines = utils.read_file(os.path.join("..", "results.dat"))[1:]

    N_runs = dict()
    Om_runs = dict()
    On_runs = dict()

    for line in lines:
        # Read the configuration values
        match = re.match(configuration, line)
        uw, n, om, on = match[1], int(match[2]), int(match[3]), int(match[4])

        # Configuration name as first and all the values after to floats
        name, *csv_values = line.split(",")
        csv_values = [float(value) for value in csv_values]

        #
        on_frac = on / n

        # Put the configurations
        if n != 3000:
            N_runs[(name, n)] = csv_values
        elif om != 3:
            Om_runs[(name, om)] = csv_values
        elif on_frac != 0.3:
            On_runs[(name, on)] = csv_values
        else:
            On_runs[(name, on)] = csv_values
            Om_runs[(name, om)] = csv_values
            N_runs[(name, n)] = csv_values

    for measure in [("NMI", 0), ("Omega Index", 1)]:
        fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
        fig.suptitle("Measure " + measure[0])

        plot(axs[0], "Variable community size", "N", measure[0], measure[1], N_runs)
        plot(axs[1], "Variable number of overlapping nodes", "On", measure[0], measure[1], On_runs)
        plot(axs[2], "Variable number of communities", "Om", measure[0], measure[1], Om_runs)
        plt.show()

    return N_runs, On_runs, Om_runs


def plot(ax, title: str, x_label: str, y_label: str, index: int, data: dict):
    xs = []
    ys1 = []
    ys2 = []
    ys3 = []

    data = dict(sorted(data.items(), key=lambda item: item[1]))
    print(data)

    for name, value in data:
        print(value, data[(name, value)])
        xs.append(value)
        ys1.append(data[(name, value)][index])
        ys2.append(data[(name, value)][index+3])
        ys3.append(data[(name, value)][index+6])

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

    # Visualize the plot
    plt.legend()
    plt.ylim([0, 1])


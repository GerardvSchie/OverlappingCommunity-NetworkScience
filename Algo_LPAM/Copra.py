#!/usr/bin/env python
# coding: utf-8

# ## COPRA## 

import numpy as np
import random
random.seed = 108

from tqdm import tqdm_notebook as tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import os

params=dict()
params["-v"] = list(range(1,10))
# params["-cp"] = np.arange(0.05, 0.95, 0.05)
# params["-seed"] = random.sample(range(1, 100), 10)

# Commented
# params

def generate_params(params):
    keys = list(params.keys())
    if len(keys) == 1:
        for value in params[keys[0]]:
            yield ( keys[0] + " " + str(value) )        
    if len( keys ) > 1:
        for value in params[keys[0]]:
            for remain_params in generate_params({k:params[k] for k in keys[1:]}):
                yield ( keys[0] + " " + str(value) + " " + remain_params )

def copra_experiment(inputFile, groundTruth, params = {}, vertexNumerationShift=0, verbose=False):
    datasetName = inputFile.split('/')[-2]
    outputDir = "../Results/COPRA_{}".format(datasetName)
    outputFile = outputDir + "/" + "clusters-" + inputFile.split('/')[-1]
    print("Output dir name: {}".format(outputDir) )
    print("Output file name: {}".format(outputFile) )
    
    os.mkdir(outputDir)
    
    all_results = {}
    bestParam = "not found"
    nmi_best = 0
    for param in tqdm(list(generate_params(params))):
        tmp=!(cd {outputDir} && java -cp ../../related_methods/OSLOM2/copra.jar COPRA ../{inputFile} {param} -repeat 100 -mo -nosplit)
    #     !sed -i '' '/^#/d' {outputFile}
        with open(outputFile) as f:
            lines = f.readlines()    
        with open(outputFile, 'w') as the_file:
            for line in lines:
                the_file.write(" ".join([str(int(a) + vertexNumerationShift) for a in line.split()]) + "\n")
        output=!../Overlapping-NMI/onmi {groundTruth} {outputFile}
        if verbose:
            print(output)
        nmi=float(output[0].split()[1])
        all_results[param] = nmi
        if nmi >  nmi_best:
            bestParam = param
            nmi_best = nmi

    print("Best ONMI: {} params: '{}'".format(nmi_best, bestParam) )                   
    return all_results

def plot_graph_for_all_results(all_results, datasetName):
    xdata=[]
    ydata=[]
    df = pd.DataFrame()
    for param, nmi in all_results.items():
        splited = param.split()
        xdata.append(float(splited[1]))
        ydata.append(nmi)
        df = df.append({'x': float(splited[1]), 'y': nmi}, ignore_index=True)

    plt.plot(xdata, ydata, 'C3', zorder=1, lw=3)
    # ax = plt.axes(projection='3d')
    plt.scatter(xdata, ydata,s=70,zorder=2)
    plt.xlabel('v parameter')
    plt.ylabel('nmi value')
    plt.title('onmi values for dataset: {}\nAlgorithm: "COPRA" no option "extrasimplify"'.format(datasetName))
    plt.show()

# # School Friendship #

inputFile = "../datasets/school_friendship/school-2.dat"
groundTruth = "../datasets/school_friendship/truth-school.dat"
all_results = copra_experiment(inputFile, groundTruth, params, vertexNumerationShift=-1)

plot_graph_for_all_results(all_results, "school_friendship")

# ![copra_school](../final_pictures/copra_school.png "COPRA School Friendship")

# # Karate Club #

inputFile = "../datasets/karate/karate.dat"
groundTruth = "../datasets/karate/truth_karate.dat"
all_results = copra_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "Karate club")

# ![copra_karate](../final_pictures/copra_karate.png "COPRA Karate Club")

inputFile = "../datasets/adjnoun/adjnoun.dat"
groundTruth = "../datasets/adjnoun/truth_adjnoun.dat"
all_results = copra_experiment(inputFile, groundTruth, params, vertexNumerationShift=-1)

plot_graph_for_all_results(all_results, "Adj Noun")

# # Football Club #

inputFile = "../datasets/football/footballTSEinput_original.dat"
groundTruth = "../datasets/football/truth_footballTSEinput.dat"
all_results = copra_experiment(inputFile, groundTruth, params, vertexNumerationShift=-1)

plot_graph_for_all_results(all_results, "Football Club")

# ![copra_football](../final_pictures/copra_football.png "COPRA American Football League")

# # Politics Book #

inputFile = "../datasets/polbooks/polbooks.dat"
groundTruth = "../datasets/polbooks/truth_polbooks.dat"
all_results = copra_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "Politics Book")

# ![copra_politic_books](../final_pictures/copra_polbooks.png "COPRA Politic Books")

# # Syntetic Datasets #
# ## bench_30##

inputFile = "../datasets/bench_30/bench_30_network.dat"
groundTruth = "../datasets/bench_30/bench_30_truth.dat"
all_results = copra_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "bench_30")

# ![copra_bench_30](../final_pictures/copra_bench_30.png "COPRA Bench_30")

# ## bench_40##

inputFile = "../datasets/bench_40/bench_40_network.dat"
groundTruth = "../datasets/bench_40/bench_40_truth.dat"
all_results = copra_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "bench_40")

# ![copra_bench_40](../final_pictures/copra_bench_40.png "COPRA Bench_40")

# ## bench_50##

inputFile = "../datasets/bench_50/bench_50_network.dat"
groundTruth = "../datasets/bench_50/bench_50_truth.dat"
all_results = copra_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "bench_50")

# ![copra_bench_50](../final_pictures/copra_bench_50.png "COPRA Bench_50")

# ## bench_60 ##

inputFile = "../datasets/bench_60/bench_60_network.dat"
groundTruth = "../datasets/bench_60/bench_60_truth.dat"
all_results = copra_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "bench_60")

# ![copra_bench_60](../final_pictures/copra_bench_60.png "COPRA Bench_60")

# ## bench_60_dense ##

inputFile = "../datasets/bench_60_dense/bench_60_dense_network.dat"
groundTruth = "../datasets/bench_60_dense/bench_60_dense_truth.dat"
all_results = copra_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "bench_60_dense")

# ![copra_bench_60_dense](../final_pictures/copra_bench_60_dense.png "COPRA Bench_60_dense")

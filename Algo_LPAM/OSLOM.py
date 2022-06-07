#!/usr/bin/env python
# coding: utf-8

# ## OSLOM ## 
# подберём такие параметры, которые бы давали максимальное значение nmi

import numpy as np
import random
import os
import shutil

random.seed = 108
from tqdm import tqdm_notebook as tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import os


def generate_params(params):
    keys = list(params.keys())
    if len(keys) == 1:
        for value in params[keys[0]]:
            yield ( keys[0] + " " + str(value) )        
    if len( keys ) > 1:
        for value in params[keys[0]]:
            for remain_params in generate_params({k:params[k] for k in keys[1:]}):
                yield ( keys[0] + " " + str(value) + " " + remain_params )


def oslom_experiment(inputFileFull, groundTruth, params = {}, vertexNumerationShift=0, verbose=False):
    datasetName = inputFileFull.split('/')[-2]
    outputDir = "../Results/OSLOM2_{}".format(datasetName)
    inputFile =  outputDir + '/' + inputFileFull.split('/')[-1]
    outputFile = outputDir + '/' + inputFileFull.split('/')[-1] + "_oslo_files/tp"
#     outputFile = outputDir + '/' "tp"
    
    os.mkdir(outputDir)
    shutil.copyfile(inputFileFull, os.path.join(outputDir, datasetName))
    
    print("Output dir name: {}".format(outputDir) )
    print("old inputFileName : {}".format(inputFileFull) )
    print("new inputFileName : {}".format(inputFile) )
    print("Output file name: {}".format(outputFile) )
    
    os.mkdir(outputDir)
    
    all_results = {}
    bestParam = "not found"
    onmi_best = 0
    for param in tqdm(list(generate_params(params))):
        tmp=!(cd {outputDir} && ../../related_methods/OSLOM2/oslom_undir -f ../{inputFile} -uw {param})
        if verbose:
            print(tmp)
        !sed -i '/^#/d' {outputFile}
        lines=[]
        with open(outputFile) as f:
            lines = f.readlines()    
        with open(outputFile, 'w') as the_file:
            for line in lines:
                the_file.write(" ".join([str(int(a)+vertexNumerationShift) for a in line.split()]) + "\n")
        output = !../Overlapping-NMI/onmi {groundTruth} {outputFile}
        onmi=float(output[0].split()[1])
        all_results[param] = onmi
        if onmi >  onmi_best:
            bestParam = param
            onmi_best = onmi
            
            
    mean_results = {}
    for line, value in all_results.items():
        key = " ".join(line.split()[:4])
        if key in mean_results:
            mean_results[key].append(value)
        else:
            mean_results[key] = [value]
        
    onmi_best_avg = np.max([np.mean(values) for key, values in mean_results.items() ])
   
            
    print("Best of Max ONMI: {} params: '{}'".format(onmi_best, bestParam) )  
    print("Best of Avarage ONMI: {} params: '{}'".format(onmi_best_avg, bestParam) )                   
    return all_results

def plot_graph_for_all_results(all_results, datasetName, random_choice='max'):
    xdata=[]
    ydata=[]
    zdata=[]
    df = pd.DataFrame()
    for param, onmi in all_results.items():
        splited = param.split()
        xdata.append(float(splited[1]))
        ydata.append(float(splited[3]))
        zdata.append(onmi)
        df = df.append({'x': float(splited[1]), 'y': float(splited[3]) , 'seed': int(splited[5]), 'z': onmi}, ignore_index=True)

    df_ddd = df.groupby(['x','y'], as_index=False)['z'].max()
    if random_choice == 'mean':
        df_ddd = df.groupby(['x','y'], as_index=False)['z'].mean()
    
    #coolwarm  viridis
    fig = plt.figure(figsize=(12, 10), dpi= 80)
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(df_ddd.x.values, df_ddd.y.values, df_ddd.z.values, cmap='plasma', edgecolor='none')
    ax.view_init(30, 55)
    ax.set_xlabel('t parameter')
    ax.set_ylabel('cp paramter')
    ax.set_zlabel('onmi vlue')
    ax.set_title('OSLOM\n Onmi {} values for 10-random seeds\nDataset: {}'.format(random_choice.upper(), datasetName));

# # School Friendship #

params=dict()
params["-t"] = np.arange(0.05, 0.95, 0.1)
params["-cp"] = np.arange(0.05, 0.95, 0.1)
params["-seed"] = random.sample(range(1, 100), 10)

inputFile = "../datasets/school_friendship/school-2.dat"
groundTruth = "../datasets/school_friendship/truth-school.dat"

all_results = oslom_experiment(inputFile, groundTruth, params, vertexNumerationShift=-1)

plot_graph_for_all_results(all_results, "school_friendship", random_choice="mean")

plot_graph_for_all_results(all_results, "school_friendship", random_choice='mean')

# ![oslom_school](../final_pictures/oslom_school_result.png)

# ## Karate Club ##

inputFile = "../datasets/karate/karate.dat"
groundTruth = "../datasets/karate/truth_karate.dat"
all_results = oslom_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "Karate club", random_choice='mean')

# ![oslom_karate](../final_pictures/oslom_karate.png "Oslom Karate Club")

# ## Adj noun##

inputFile = "../datasets/adjnoun/adjnoun.dat"
groundTruth = "../datasets/adjnoun/truth_adjnoun.dat"
all_results = oslom_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "Adj Noun", random_choice='mean')

# ## American Football League ##

inputFile = "../datasets/football/footballTSEinput_original.dat"
groundTruth = "../datasets/football/truth_footballTSEinput.dat"
all_results = oslom_experiment(inputFile, groundTruth, params, vertexNumerationShift=-1)

plot_graph_for_all_results(all_results, "American Fooball League", random_choice='mean')

# ![oslom_football](../final_pictures/oslom_football.png "Oslom Americal Football League")

# ## Politic Books ##

inputFile = "../datasets/polbooks/polbooks.dat"
groundTruth = "../datasets/polbooks/truth_polbooks.dat"
all_results = oslom_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "Politic Books", random_choice='mean')

# ![oslom_polic_books](../final_pictures/oslom_polbooks.png "Oslom Politic Books")

# # Syntetic Datasets #
# ## bench_30##

inputFile = "../datasets/bench_30/bench_30_network.dat"
groundTruth = "../datasets/bench_30/bench_30_truth.dat"
all_results = oslom_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "bench_30", random_choice='mean')

# ![oslom_bench_30](../final_pictures/oslom_bench_30.png "Oslom bench_30")

# ## bench_40##

inputFile = "../datasets/bench_40/bench_40_network.dat"
groundTruth = "../datasets/bench_40/bench_40_truth.dat"
all_results = oslom_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "bench_40", random_choice='mean')

# ![oslom_bench_40](../final_pictures/oslom_bench_40.png "Oslom bench_40")
# ## bench_50##

inputFile = "../datasets/bench_50/bench_50_network.dat"
groundTruth = "../datasets/bench_50/bench_50_truth.dat"
all_results = oslom_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "bench_50", random_choice='mean')

# ![oslom_bench_50](../final_pictures/oslom_bench_50.png "Oslom bench_50")
# ## bench_60##

inputFile = "../datasets/bench_60/bench_60_network.dat"
groundTruth = "../datasets/bench_60/bench_60_truth.dat"
all_results = oslom_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "bench_60", random_choice='mean')

# ![oslom_bench_60](../final_pictures/oslom_bench_60.png "Oslom bench_60")
# ## bench_60_dense ##

inputFile = "../datasets/bench_60_dense/bench_60_dense_network.dat"
groundTruth = "../datasets/bench_60_dense/bench_60_dense_truth.dat"
all_results = oslom_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "bench_60_dense", random_choice='mean')

# ![oslom_bench_60_dense](../final_pictures/oslom_bench_60_dense.png "Oslom bench_60_dense")

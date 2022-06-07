#!/usr/bin/env python
# coding: utf-8

# # Greedy Clique Expansion Community Finder (GCE) # 
# подберём такие параметры, которые бы давали максимальное значение nmi

import numpy as np
import random
random.seed = 108
from tqdm import tqdm_notebook as tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import os

# Commented
# !pwd

# !ls ../related_methods/GCECommunityFinder/build/

# !(cd ../related_methods/GCECommunityFinder/build/ && make)
# Use with either full (if specify all 5) or default (specify just graph file) parameters:
# Full parameters are:
# The name of the file to load
#
# 1) The minimum size of cliques to use as seeds. Recommend 4 as default, unless particularly small communities are required (in which case use 3).
# 2 The minimum value for one seed to overlap with another seed before it is considered sufficiently overlapping to be discarded (eta). 1 is complete overlap. However smaller values may be used to prune seeds more aggressively. A value of 0.6 is recommended.
# 3) The alpha value to use in the fitness function greedily expanding the seeds. 1.0 is recommended default. Values between .8 and 1.5 may be useful. As the density of edges increases, alpha may need to be increased to stop communities expanding to engulf the whole graph. If this occurs, a warning message advising that a higher value of alpha be used, will be printed.
# 4) The proportion of nodes (phi) within a core clique that must have already been covered by other cliques, for the clique to be 'sufficiently covered' in the Clique Coveage Heuristic
#
# Usage: ./GCECommunityFinder graphfilename minimumCliqueSizeK overlapToDiscardEta fitnessExponentAlpha CCHthresholdPhi
#
# The default values of: minimumCliqueSizeK 4, overlapToDiscardEta 0.6, fitnessExponentAlpha 1.0, CCHthresholdPhi .75

def generate_params(params):
    keys = list(params.keys())
    if len(keys) == 1:
        for value in params[keys[0]]:
            yield ( keys[0] + " " + str(value) )        
    if len( keys ) > 1:
        for value in params[keys[0]]:
            for remain_params in generate_params({k:params[k] for k in keys[1:]}):
                yield ( keys[0] + " " + str(value) + " " + remain_params )


def GCE_experiment(inputFile, groundTruth, params = {}, vertexNumerationShift=0, verbose=False):
    datasetName = inputFile.split('/')[-2]
    workingDir = "../Results/GCE_{}".format(datasetName)
    outputFile = workingDir + "/GCE_output.txt"
    print("workingDir: {}".format(workingDir) )
    print("outputFile: {}".format(outputFile) )
    
    os.mkdir(workingDir)
    
    all_results = {}
    bestParam = "not found"
    nmi_best = 0;
    for param in tqdm(list(generate_params(params))):
        out = !../related_methods/GCECommunityFinder/build/GCECommunityFinder {inputFile} 4 0.9 {param} .75
        if verbose:
            print(out)
        with open(outputFile, 'w') as the_file:
            for line in out[out.index('Finished')+1:]:
                the_file.write(" ".join([str(int(a)+vertexNumerationShift) for a in line.split()]) + "\n")

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
        xdata.append(param)
        ydata.append(nmi)
        df = df.append({'x': float(param), 'y': nmi}, ignore_index=True)

    plt.plot(xdata, ydata, 'C3', zorder=1, lw=3)
    plt.scatter(xdata, ydata,s=70,zorder=2)
    plt.xlabel('fitnessExponentAlpha')
    plt.ylabel('onmi value');
    plt.title('Algorithm: "GCE"\nDataset: {}'.format(datasetName));
    plt.show()

# # School_Friendship #

params={}
params[""] = np.arange(0.05, 0.95, 0.05)

inputFile = "../datasets/school_friendship/school-2.dat"
groundTruth = "../datasets/school_friendship/truth-school.dat"
all_results = GCE_experiment(inputFile, groundTruth, params, vertexNumerationShift=-1)

plot_graph_for_all_results(all_results, "school_friendship")

# ![gce_school](../final_pictures/gce_school_result.png "GCE School Friendship")

# # Karate Club#

inputFile = "../datasets/karate/karate.dat"
groundTruth = "../datasets/karate/truth_karate.dat"
all_results = GCE_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "Karate Club")

# ![gce_karate](../final_pictures/gce_karate.png "GCE Karate Club")

# # Adjnoun#

inputFile = "../datasets/adjnoun/adjnoun.dat"
groundTruth = "../datasets/adjnoun/truth_adjnoun.dat"
all_results = GCE_experiment(inputFile, groundTruth, params, vertexNumerationShift=-1)


plot_graph_for_all_results(all_results, "Adj Noun")

# # Football Club #

inputFile = "../datasets/football/footballTSEinput_original.dat"
groundTruth = "../datasets/football/truth_footballTSEinput.dat"
all_results = GCE_experiment(inputFile, groundTruth, params, vertexNumerationShift=-1)

plot_graph_for_all_results(all_results, "Football Club")

# ![gce_football](../final_pictures/gce_football.png "GCE American Football League")

# # Politics Book #

inputFile = "../datasets/polbooks/polbooks.dat"
groundTruth = "../datasets/polbooks/truth_polbooks.dat"
all_results = GCE_experiment(inputFile, groundTruth, params, vertexNumerationShift=0)

plot_graph_for_all_results(all_results, "Politics Book")

# ![gce_politic_books](../final_pictures/gce_polbooks.png "GCE Politic Books")

# # Syntetic Datasets #

# ## bench_30 ##

inputFile = "../datasets/bench_30/bench_30_network.dat"
groundTruth = "../datasets/bench_30/bench_30_truth.dat" 
all_results = GCE_experiment(inputFile, groundTruth, params, vertexNumerationShift=0, verbose=False)

plot_graph_for_all_results(all_results, "bench_30_network")

# ![gce_bench_30](../final_pictures/gce_bench_30.png "GCE bench_30")

# #### bench_40 ##

inputFile = "../datasets/bench_40/bench_40_network.dat"
groundTruth = "../datasets/bench_40/bench_40_truth.dat" 
all_results = GCE_experiment(inputFile, groundTruth, params, vertexNumerationShift=0, verbose=False)

plot_graph_for_all_results(all_results, "bench_30_network")

# ![gce_bench_40](../final_pictures/gce_bench_40.png "GCE bench_40")

# ## bench_50 ##

inputFile = "../datasets/bench_50/bench_50_network.dat"
groundTruth = "../datasets/bench_50/bench_50_truth.dat" 
all_results = GCE_experiment(inputFile, groundTruth, params, vertexNumerationShift=0, verbose=False)

plot_graph_for_all_results(all_results, "bench_50_network")

# ![gce_bench_50](../final_pictures/gce_bench_50.png "GCE bench_50")

# ## bench_60 ##

inputFile = "../datasets/bench_60/bench_60_network.dat"
groundTruth = "../datasets/bench_60/bench_60_truth.dat" 
all_results = GCE_experiment(inputFile, groundTruth, params, vertexNumerationShift=0, verbose=False)

plot_graph_for_all_results(all_results, "bench_60_network")

# ![gce_bench_60](../final_pictures/gce_bench_60.png "GCE bench_60")

# ## bench_60_dense ##

inputFile = "../datasets/bench_60_dense/bench_60_dense_network.dat"
groundTruth = "../datasets/bench_60_dense/bench_60_dense_truth.dat" 
all_results = GCE_experiment(inputFile, groundTruth, params, vertexNumerationShift=0, verbose=False)

plot_graph_for_all_results(all_results, "bench_60_dense_network")

# ![gce_bench_60_dense](../final_pictures/gce_bench_60_dense.png "GCE bench_60_dense")

# In[ ]:




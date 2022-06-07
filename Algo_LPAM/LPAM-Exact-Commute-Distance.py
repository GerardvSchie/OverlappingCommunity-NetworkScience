#!/usr/bin/env python
# coding: utf-8

import numpy as np
import random
import os

random.seed = 108
from tqdm import tqdm_notebook as tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd

# Commented
# !java -jar ../lpam/out/artifacts/Clustering_jar/Clustering.jar


def lp_experiment(clustersNumber, algorithm, distance, inputFile, groundTruth, params = {}, vertexNumerationShift=0, benchmarkFormat=False, verbose=False, lineGraph=False):
    lineGraphParam = ""
    if (lineGraph == True):
        lineGraphParam = " -l"
    datasetName = inputFile.split('/')[-2]
    sufix = inputFile.split('/')[-1].split('.')[0]
    outputDir = "../Results/lp_{}_{}_{}".format(algorithm, distance, datasetName)
    outputFile = outputDir +'/' +"pmp_{3}_{2}_{0}_{1}.dat".format(algorithm, clustersNumber, distance.upper(), sufix)
    print("Output dir name: {}".format(outputDir) )
    print("Output file name: {}".format(outputFile) )
    all_results = {}
    bestParam = "not found"
    nmi_best = 0;
    param_list = list(generate_params(params))
    tmp = None
    for param in tqdm(param_list):
        if benchmarkFormat:
            tmp=!java -jar ../lpam/out/artifacts/Clustering_jar/Clustering.jar -b -a {algorithm} -o {outputDir} -i {inputFile} -k {clustersNumber} -d {distance} -gt {groundTruth} {param}
            tmpFile = outputFile
        else:
            tmp=!java -jar ../lpam/out/artifacts/Clustering_jar/Clustering.jar -a {algorithm} -o {outputDir} -i {inputFile} -k {clustersNumber} -d {distance} -gt {groundTruth} {param}
            lines=[]
            with open(outputFile) as f:
                lines = f.readlines()    
            tmpFile="tmpFile.dat"
            with open(tmpFile, 'w') as the_file:
                for line in lines:
                    the_file.write(" ".join([str(int(a)+vertexNumerationShift) for a in line.split()]) + "\n")

        output=!../Overlapping-NMI/onmi {groundTruth} {tmpFile}
        nmi=float(output[0].split()[1])
        all_results[param] = nmi
        if nmi >  nmi_best:
            bestParam = param
            nmi_best = nmi
    #restorign solution for the best parameters 
    if benchmarkFormat:
        tmp=!java -jar ../lpam/out/artifacts/Clustering_jar/Clustering.jar -b -a {algorithm} -o {outputDir} -i {inputFile} -gt {groundTruth} -k {clustersNumber} -d {distance} -gt {groundTruth} {bestParam} {lineGraphParam}
        tmpFile = outputFile
    else:
        tmp=!java -jar ../lpam/out/artifacts/Clustering_jar/Clustering.jar -a {algorithm} -o {outputDir} -i {inputFile} -gt {groundTruth} -k {clustersNumber} -d {distance} -gt {groundTruth} {bestParam} {lineGraphParam}
        lines=[]
        with open(outputFile) as f:
            lines = f.readlines()    
        tmpFile="tmpFile.dat"
        with open(tmpFile, 'w') as the_file:
            for line in lines:
                the_file.write(" ".join([str(int(a)+vertexNumerationShift) for a in line.split()]) + "\n")

    if verbose:                                                                                                                                             
        print(tmp)
    print("Best ONMI: {} params: '{}'".format(nmi_best, bestParam) )
    return all_results

# In[5]:


def generate_params(params):
    keys = list(params.keys())
    if len(keys) == 1:
        for value in params[keys[0]]:
            yield ( keys[0] + " " + str(value) )        
    if len( keys ) > 1:
        for value in params[keys[0]]:
            for remain_params in generate_params({k:params[k] for k in keys[1:]}):
                yield ( keys[0] + " " + str(value) + " " + remain_params )

# In[6]:


def plot_all_params(algorithm, dataset, all_results ):
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
    plt.xlabel('threshold')
    plt.ylabel('nmi value');
    plt.title('Algorithm: {}\nDataset: {}'.format(algorithm, dataset));
    plt.show()

# # School friendship network #

# In[9]:


params={}
params["-t"] = np.arange(0.05, 1.0, 0.05)

# In[11]:


all_results = lp_experiment(clustersNumber=7, 
              algorithm = "pmp",
              distance = "cm",
              inputFile =  "../datasets/school_friendship/school-2.gml", 
              groundTruth = "../datasets/school_friendship/truth-school.dat", 
              params = params, 
              vertexNumerationShift=-1, 
              benchmarkFormat=False, lineGraph=True) 

# In[13]:


plot_all_params(algorithm = "LPAM-Exact + Commute Distance", dataset = "School Friendship", all_results = all_results)

# ## Clustering results for School Frienship Netwrok with the best parameters ##
# Distance: Commute Distance. Number of Clusters = 7

# ![school-2_ACM_kmd_7_out](../final_pictures/school-2_CM_pmp_7_out.png)
# ## Line Graph ##
# ![school-2_ACM_kmd_7_out_line](../final_pictures/school-2_CM_pmp_7_out_line.png)

# # Karate Club #

# In[20]:


params={}
params["-t"] = np.arange(0.05, 1.0, 0.05)
all_results = lp_experiment(clustersNumber=2, 
              algorithm = "pmp",
              distance = "cm",
              inputFile =  "../datasets/karate/karate.gml", 
              groundTruth = "../datasets/karate/truth_karate.dat", 
              params = params, 
              vertexNumerationShift=0, 
              benchmarkFormat=False, verbose=False, lineGraph=True)

# In[37]:


plot_all_params(algorithm = "LPAM-Exact+Commute-Distance", dataset = "Karate Club ", all_results = all_results)

# ![karate_CM_pmp_2_out](../final_pictures/karate_CM_pmp_2_out.png)
# ## Line Graph ##
# ![karate_CM_pmp_2_out_line](../final_pictures/karate_CM_pmp_2_out_line.png)

# # American Football League c = 12#

# In[38]:


params={}
params["-t"] = np.arange(0.05, 1.0, 0.05)
all_results = lp_experiment(clustersNumber=12, 
              algorithm = "kmd",
              distance = "cm",
              inputFile =  "../datasets/football/footballTSEinput.gml", 
              groundTruth = "../datasets/football/truth_footballTSEinput.dat", 
              params = params, 
              vertexNumerationShift=-1, 
              benchmarkFormat=False)

# In[39]:


plot_all_params(algorithm = "LPAM-Exact + Commute Distance", dataset = "American Foolball League", all_results = all_results)

# ### Americal Football League  [onmi: 0.71194; thresould: 0.5]

# ![American Football Club](../final_pictures/footballTSEinput_CM_kmd_12_out.png)

# # Adj-noun#

# In[40]:


params={}
params["-t"] = np.arange(0.05, 1.0, 0.05)
all_results = lp_experiment(clustersNumber=2, 
              algorithm = "pmp",
              distance = "cm",
              inputFile =  "../datasets/adjnoun/adjnoun.dat", 
              groundTruth = "../datasets/adjnoun/truth_adjnoun.dat", 
              params = params, 
              vertexNumerationShift=0, 
              benchmarkFormat=True, verbose=True, lineGraph=True)

# In[41]:


plot_all_params(algorithm = "LPAM-Exact + acm", dataset = "Adj noun", all_results = all_results)

# ### Adj-noun [ onmi: 0.00490969; thresould: 0.1 ] 

# ![adjnoun_ACM_kmd_2](../final_pictures/adjnoun_CM_pmp_2_out.png)

# # Politics Books #

# In[21]:


params={}
params["-t"] = np.arange(0.05, 1.0, 0.05)
all_results = lp_experiment(clustersNumber=2, 
              algorithm = "pmp",
              distance = "cm",
              inputFile = "../datasets/polbooks/polbooks.dat",
              groundTruth = "../datasets/polbooks/truth_polbooks.dat", 
              params = params, 
              vertexNumerationShift=0, 
              benchmarkFormat=True, verbose=False, lineGraph=True)

# In[22]:


plot_all_params(algorithm = "LPAM-exact + Commute Distance", dataset = "Politics Books", all_results = all_results)

# ![polbooks_ACM_kmd_2_out](../final_pictures/polbooks_CM_pmp_2_out.png)
# ## Line Graph ##
# ![polbooks_cm_pmp_2_out_line](../final_pictures/polbooks_CM_pmp_2_out_line.png)

# # Syntetic Datasets #

# ### bench_30_network ###

# In[147]:


params={}
params["-t"] = np.arange(0.05, 1.0, 0.05)
all_results = lp_experiment(clustersNumber=3, 
              algorithm = "pmp",
              distance = "cm",
              inputFile = "../datasets/bench_30/bench_30_network.dat",
              groundTruth = "../datasets/bench_30/bench_30_truth.dat", 
              params = params, 
              vertexNumerationShift=0, 
              benchmarkFormat=True)

# In[148]:


plot_all_params(algorithm = "LPAM-exact + Commute Distance", dataset = "bench_30", all_results = all_results)

# ![bench_30](../final_pictures/bench_30_network_CM_pmp_3_out.png)

# ### bench_40_network ###

# In[150]:


params={}
params["-t"] = np.arange(0.05, 1.0, 0.05)
all_results = lp_experiment(clustersNumber=3, 
              algorithm = "pmp",
              distance = "cm",
              inputFile = "../datasets/bench_40/bench_40_network.dat",
              groundTruth = "../datasets/bench_40/bench_40_truth.dat", 
              params = params, 
              vertexNumerationShift=0, 
              benchmarkFormat=True)

# In[151]:


plot_all_params(algorithm = "LPAM-exact + Commute Distance", dataset = "bench_40", all_results = all_results)

# ![bench_40](../final_pictures/bench_40_network_CM_pmp_3_out.png)

# ### bench_50 ###

# In[156]:


params={}
params["-t"] = np.arange(0.05, 1.0, 0.05)
all_results = lp_experiment(clustersNumber=4, 
              algorithm = "pmp",
              distance = "cm",
              inputFile = "../datasets/bench_50/bench_50_network.dat",
              groundTruth = "../datasets/bench_50/bench_50_truth.dat", 
              params = params, 
              vertexNumerationShift=0, 
              benchmarkFormat=True)

# In[154]:


plot_all_params(algorithm = "LPAM-exact + Commute Distance", dataset = "bench_50", all_results = all_results)

# ![bench_50](../final_pictures/bench_50_network_CM_pmp_4_out.png)

# ### bench_60 ###

# In[157]:


params={}
params["-t"] = np.arange(0.05, 1.0, 0.05)
all_results = lp_experiment(clustersNumber=6, 
              algorithm = "pmp",
              distance = "cm",
              inputFile = "../datasets/bench_60/bench_60_network.dat",
              groundTruth = "../datasets/bench_60/bench_60_truth.dat", 
              params = params, 
              vertexNumerationShift=0, 
              benchmarkFormat=True)

# In[158]:


plot_all_params(algorithm = "LPAM-exact + Commute Distance", dataset = "bench_60", all_results = all_results)

# ![bench_60](../final_pictures/bench_60_network_CM_pmp_6_out.png)

# ### bench_60_dense ###

# In[160]:


params={}
params["-t"] = np.arange(0.05, 1.0, 0.05)
all_results = lp_experiment(clustersNumber=6, 
              algorithm = "pmp",
              distance = "cm",
              inputFile = "../datasets/bench_60_dense/bench_60_dense_network.dat",
              groundTruth = "../datasets/bench_60_dense/bench_60_dense_truth.dat", 
              params = params, 
              vertexNumerationShift=0, 
              benchmarkFormat=True)

# In[162]:


plot_all_params(algorithm = "LPAM-exact + Commute Distance", dataset = "bench_60_dense", all_results = all_results)

# ![bench_60_dense](../final_pictures/bench_60_dense_network_CM_pmp_6_out.png)

# # Format transformet  Helper Tool #

# In[159]:


#Transform from benchmark community format to onmi-tool community structure format
oldF = "../datasets/bench_60_dense/bench_60_dense_community.dat"
newF = "../datasets/bench_60_dense/bench_60_dense_truth.dat"

v = {}
comm = {}
with open(oldF, "r") as ins:
    array = []
    for line in ins:
        _id = line.split()[0]
        v[_id] = [int(_c) for _c in line.split()[1: ]]
        for _c in line.split()[1: ]:
            if int(_c) in comm:
                comm[int(_c)].append(_id)
            else:
                comm[int(_c)] = [_id]
                
with open(newF, 'w') as the_file:
    for _c in comm:
        the_file.write(" ".join(comm[_c] ) + '\n')
!cat {newF}

# In[123]:




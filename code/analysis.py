#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 18:44:52 2017

@author: davidherrera
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn import preprocessing
import re
from os import listdir
from os.path import isfile, join

#==============================================================================
# PARAMETERS
#==============================================================================
NORMALIZED = False
DATA_FOLDER = "../data/aug2/cpu-times/"
RESULTS_FOLDER="./../results/aug2/"
PLOT_HISTOGRAM = False
PLOT_SCATTER = False
BUILD_TABLE = True
CUTOFF = 50
GROUPS_PER_BENCH = 4

#Definiting linear function
def linear(x, a, b):
    return a* x + b
#Getting files
onlyfiles = [f for f in listdir(DATA_FOLDER) if isfile(join(DATA_FOLDER, f))]
total = []
#Iterating through files and plotting
p = re.compile("bench=.*-impl=")
artHMean = []
artLMean = []
artHStd = []
artLStd = []

for i in range(len(onlyfiles)):
    bechmark = []
    #Reading files    
    name = onlyfiles[i]
    result = pd.read_csv(DATA_FOLDER+name);
    times = result['time'].values
    
    cpuload = result['cpuLoad'].values
    #Normalize graph
    if NORMALIZED:
        times = preprocessing.normalize(times.reshape(1,-1)).T
        times = times.reshape(len(times),)
        cpuload = preprocessing.normalize(cpuload.reshape(1,-1)).T
        cpuload = cpuload.reshape(len(cpuload),)
    
   
    cpuload50 = cpuload[cpuload<CUTOFF]
    
    times50 = times[cpuload<CUTOFF]
    cpuloadH = cpuload[cpuload>=CUTOFF]
    timesH = times[cpuload>=CUTOFF]
    print(name,"LOW",len(cpuload50),"HIGH",len(cpuloadH))
    if PLOT_HISTOGRAM:
#        dicMean = {}
        name = onlyfiles[i-1]
        name = name[:name.rfind(".csv")]
#        dicStd = {}
        meanS = np.mean(times50)
        meanL = np.std(timesH)
        stdS = np.mean(times50)
        stdL = np.std(timesH)
        n_groups = GROUPS_PER_BENCH
    
        if i % GROUPS_PER_BENCH == 0 or i == len(onlyfiles)-1:
            if i ==len(onlyfiles)-1:
                span = p.match(name).span()
                artName.append(name[span[1]:].replace("-comp=",",").replace("-env=",",").replace(".csv",""))
                artHMean.append(meanL)
                artLMean.append(meanS)
                artHStd.append(stdL)
                artLStd.append(stdS)
            
            print(i,name)
            index_name = p.search(name).span()[1]            
            if i>0:
                print(i,name)
                
                index = np.arange(GROUPS_PER_BENCH)
                fig, ax = plt.subplots(figsize=(8,6))
                bar_width = 0.35
                error_config = {'ecolor': '0.3'}
                rects1 = plt.bar(index, tuple(artHMean), bar_width,
                 color='b',
                 alpha = 0.4,
                 yerr=tuple(artHStd),
                 error_kw=error_config,
                 label="CPU<"+str(CUTOFF)+"%")
                rects2 = plt.bar(index + bar_width, tuple(artLMean), bar_width,
                 color='r',
                 alpha = 0.4,
                 yerr=tuple(artLStd),
                 error_kw=error_config,
                 label= "CPU>"+str(CUTOFF)+"%")
               # plt.xlabel(name[:index_name].replace("bench=","").replace("-impl=",""))
                plt.xticks(index + bar_width / 2, artName)
                plt.ylabel("Time(s)")
                #plt.title("Run-time comparison CPU>"+str(CUTOFF)+" vs. CPU<"+str(CUTOFF))
                ax.set_xticklabels( artName, rotation=45 )
                plt.legend()
                plt.title(name[:index_name].replace("bench=","").replace("-impl=",""))
                plt.tight_layout()
                plt.savefig(join(RESULTS_FOLDER,"img","time-comparison",name[:index_name].replace("bench=","").replace("-impl=","")+'-bar-'+str(CUTOFF)+'.png'))                
                plt.show()
                plt.figure()  
            artHMean = [meanL]
            artLMean = [meanS]
            artHStd = [stdL]
            artLStd = [stdS]
            artName = [name[index_name:].replace("-comp=",",").replace("-env=",",").replace(".csv","")]
                
        else: 
            span = p.match(name).span()
            artName.append(name[span[1]:].replace("-comp=",",").replace("-env=",",").replace(".csv",""))
            artHMean.append(meanL)
            artLMean.append(meanS)
            artHStd.append(stdL)
            artLStd.append(stdS)
            
        
        
    elif PLOT_SCATTER:
        name = name[:name.rfind(".csv")]
        plt.figure(figsize=(8,6))
        popt50, pcov50 = curve_fit(linear, cpuload50, times50)
        popt, pcov = curve_fit(linear, cpuload,times)
        print(pcov)
        label50 = 'Fit cpu<50%, m='+str(round(popt50[0],2)) if NORMALIZED else 'Fit cpu<50%'
        plt.plot(cpuload50, linear(cpuload50, *popt50), 'g-', linewidth=2,label=label50)
        
        label = 'Fit all cpu-measurements, m='+str(round(popt[0],2)) if NORMALIZED else 'Fit all'
        plt.plot(cpuload, linear(cpuload, *popt), 'r-', linewidth=2,label=label)
        plt.plot(cpuload,times,'*b',label=name)
        plt.legend()
        plt.ylabel("Time(s)")
        plt.xlabel("CPU Load")
        plt.savefig(join(RESULTS_FOLDER,"img","cpu-vs-time",name+'-cpu-vs-time.png'))
    if BUILD_TABLE:
        cpuloadB50 = cpuload[result['cpuLoad'].values>50]
        timesB50_70 = times[np.bitwise_and(  result['cpuLoad'].values>50, result['cpuLoad'].values<70)]
        timesL70 = times[result['cpuLoad'].values>70]
        print(name.split(".")[0])
        print("MEAN <30:",np.mean(times[result['cpuLoad'].values<50]),"STD:",np.std(times[result['cpuLoad'].values<50]))
        print("MEAN <50:",np.mean(times50),"STD:",np.std(times50))
        print("MEAN >50 and <70:",np.mean(timesB50_70),"STD:",np.std(timesB50_70))
        print("MEAN <70:",np.mean(times[result['cpuLoad'].values<70]),"STD:",np.std(times[result['cpuLoad'].values<70]))
        bechmark = [name, str(np.around(np.mean(times50),3))+"("+str(np.around(np.std(times50),3))+")",  str(np.around(np.mean(timesB50_70),3))+"("+str(np.around(np.std(timesB50_70),3))+")",str(np.around(np.mean(timesL70),3))+"("+str(np.around(np.std(timesL70),3))+")"]
        total.append(bechmark)
##    bechmark.append(temp);
#
if BUILD_TABLE:
    df = pd.DataFrame(columns=['Benchmark','Mean <50','Mean >50 and <70','Mean >70'],data=total)
    print df.to_latex()
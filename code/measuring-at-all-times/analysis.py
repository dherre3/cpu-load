# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:44:52 2017

@author: David Herrera
"""
#==============================================================================
# Imports
#==============================================================================
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import re
import sys

#==============================================================================
# Script Parameters
#==============================================================================
DATA_FOLDER = "../../data/aug2/"
RESULTS_FOLDER="./../../results/aug2"
PLOT_ITER_CPU = False
DELETE_OUTLIERS = False
PRODUCE_TIMES_CPU_CSV = False
GET_MEAN_BENCHMARK_LOAD = True

def getNumberArray(arr):
    '''
        Formats CSV file to appropiately get array of numbers
    '''
    arr = re.sub(r"before-iter:|after-iter:|iter=\d+:","",arr).split(",")
    arr = arr[:len(arr)-1]
    arr = [float(x) for x in arr];
    return arr
def dropIndeces(dt, indeces):
    print(indeces)
    for i in range(len(indeces)):
        dt.drop(dt.index[indeces[i]])
    return dt
def formatData(dt,dt_time, outliers=False,dropLimit=3):
    '''
        PROCEDURE:
            1. Format into numbered array
            2. If outlers is true, eliminate the rows with outliers
    '''
    befSizes = [];
    durSizes = [];
    afterSizes = [];
    print(len(dt),len(dt_time))
    for i in range(len(dt)/3):
        i*=3
        dt["names"][i] = getNumberArray(dt["names"][i])
        dt["names"][i+1] = getNumberArray(dt["names"][i+1])
        dt["names"][i+2] = getNumberArray(dt["names"][i+2])
        befSizes.append(len(dt["names"][i]))
        durSizes.append(len(dt["names"][i+1]))
        afterSizes.append(len(dt["names"][i+2]))
    meanBef = np.mean(befSizes)
    mean = np.mean(durSizes)
    meanAft = np.mean(afterSizes)
    stdBef = np.std(befSizes)
    std = np.std(durSizes)
    stdAft = np.std(afterSizes)
    #Clean data to only keep normal data
    if outliers:
        drop_indeces = []
        drop_time_indeces = []
        for i in range(len(dt)/3):
            i*=3
            t = i/3
            bef = len(dt["names"][i])>(meanBef+dropLimit*stdBef) or len(dt["names"][i])<(meanBef-dropLimit*stdBef)
            dur = len(dt["names"][i+1])>(mean+dropLimit*std) or len(dt["names"][i+1])<(mean-dropLimit*std)
            aft = len(dt["names"][i+2])>(meanAft+dropLimit*stdAft) or len(dt["names"][i+2])<(meanAft-dropLimit*stdAft)
            if bef or dur or aft:
#               print("Run",bef,dur,aft)
#               print("Bef",len(dt["names"][i]),(meanBef+dropLimit*stdBef),meanBef,  (meanBef-dropLimit*stdBef))
#               print("Dur",len(dt["names"][i+1]),(mean+dropLimit*std),mean,  (mean-dropLimit*std))
#               print("Aft",len(dt["names"][i+2]),(meanAft+dropLimit*stdAft),meanAft,  (meanAft-dropLimit*stdAft))
               drop_indeces.append(i)
               drop_indeces.append(i+1)
               drop_indeces.append(i+2)
               drop_time_indeces.append(t)
        if len(drop_time_indeces)>0:
            dt = dt.drop(dt.index[drop_indeces])
            dt_time = dt_time.drop(dt_time.index[drop_time_indeces])
            dt = dt.reindex(range(len(dt)),method='backfill')
            dt_time = dt_time.reindex(range(len(dt_time)),method='backfill')
    return (dt,dt_time)
def meanIter(before,after):
    ext = before[len(before):]=after
    iterMean = np.mean(ext)
    return iterMean
if __name__ == "__main__":
    '''
     - PLOT_ITERS will plot all the iterations
    '''
    DATA_FOLDER_CPU = DATA_FOLDER+"cpu/";
    DATA_FOLDER_TIMES = DATA_FOLDER+"times/";
    total_mean_cpu = []
    onlyfiles = [f for f in listdir(DATA_FOLDER_CPU) if isfile(join(DATA_FOLDER_CPU, f))]
    for j in range(len(onlyfiles)):
        bechmark = []
        #Reading files    
        name = onlyfiles[j]
        dt_cpu = pd.read_table(DATA_FOLDER_CPU+name,names=["names"], header=None)
        dt_times = pd.read_table(DATA_FOLDER_TIMES+name[:name.rfind(".csv")]+"-times.csv")
        [dt_cpu,dt_times] = formatData(dt_cpu,dt_times, DELETE_OUTLIERS,8)
        if PLOT_ITER_CPU:
            plt.figure()
            for i in range(len(dt_cpu)/3):
                i*=3
                plt.plot(np.arange(0,len(dt_cpu["names"][i])),dt_cpu["names"][i],"-b");
                plt.plot(np.arange(len(dt_cpu["names"][i]),len(dt_cpu["names"][i])+len(dt_cpu["names"][i+1])),dt_cpu["names"][i+1],"-g");
                plt.plot(np.arange(len(dt_cpu["names"][i])+len(dt_cpu["names"][i+1]),len(dt_cpu["names"][i])+len(dt_cpu["names"][i+1])+len(dt_cpu["names"][i+2])),dt_cpu["names"][i+2],"-r");
            plt.title(name)
            plt.xlabel("Time CPU-Collector(s)")
            plt.ylabel("CPU Load %")
            plt.savefig(join(RESULTS_FOLDER,"img","cpu-trace",name[:name.rfind(".csv")]+'-cpu-trace.png'))
        if PRODUCE_TIMES_CPU_CSV:
            if not isfile(DATA_FOLDER+"/cpu-times/"+name):
                with open(DATA_FOLDER+"/cpu-times/"+name,'ab') as f:
                   f.write("time,cpuLoad\n")
                   for i in range((len(dt_cpu)/3)-1):
                        i*=3
                        iterMean = meanIter(dt_cpu["names"][i],dt_cpu["names"][i+2])
                        time = dt_times["times"][i/3]
                        f.write(str(float(time[:len(time)-1]))+","+str(iterMean)+ "\n")
        if GET_MEAN_BENCHMARK_LOAD:
            cpu_avg_bench = []
            for i in range(len(dt_cpu)/3):
                i*=3
                meanBefAft = meanIter(dt_cpu["names"][i],dt_cpu["names"][i+2])
                meanDur = np.mean(dt_cpu["names"][i+1])
                cpu_avg_bench.append(meanDur-meanBefAft)
            mean = np.mean(cpu_avg_bench)
            std = np.std(cpu_avg_bench)
            total_mean_cpu.append([name.replace(".csv",""),mean,std])
            print("RESULT:",name,mean,std)
    if len(total_mean_cpu)>0:
        df = pd.DataFrame(columns=['Benchmark','Mean$(%)$','Std$(%)$'],data=total_mean_cpu)
        print df.to_latex()
        
            
             


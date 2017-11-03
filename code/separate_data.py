# -*- coding: utf-8 -*-
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
DATA_FOLDER = "../data/aug31/"
def meanIter(before,after):
    ext = before[len(before):]=after
    iterMean = np.mean(ext)
    return iterMean

def getNumberArray(arr):
    '''
        Formats CSV file to appropiately get array of numbers
    '''
    arr = re.sub(r"before-iter:|after-iter:|iter=\d+:|time-iter:","",arr).split(",")
    arr = arr[:len(arr)-1]
    arr = [float(x) for x in arr];
    return arr
if __name__ == "__main__":
    '''
     - PLOT_ITERS will plot all the iterations
    '''
    DATA_FOLDER_CPU = DATA_FOLDER;
    total_mean_cpu = []
    onlyfiles = [f for f in listdir(DATA_FOLDER_CPU) if isfile(join(DATA_FOLDER_CPU, f))]
    for j in range(len(onlyfiles)):
        bechmark = []
        #Reading files    
        name = onlyfiles[j]
        dt = pd.read_table(DATA_FOLDER_CPU+name,names=["names"], header=None)
        if not isfile(DATA_FOLDER+"cpu-times/"+name):
                with open(DATA_FOLDER+"cpu-times/"+name,'ab') as f:
                   f.write("time,cpuLoad\n")
                   for i in range(len(dt)/4):
                    i*=4
                    dt["names"][i] = getNumberArray(dt["names"][i])
                    dt["names"][i+1] = getNumberArray(dt["names"][i+1])
                    dt["names"][i+2] = getNumberArray(dt["names"][i+2])
                    if len(dt["names"][i+2])>1: 
                        dt["names"][i+2] = dt["names"][i+2][:1]
                    dt["names"][i+3] = getNumberArray(dt["names"][i+3])
                    print(dt["names"][i+2])
                    iterMean = meanIter(dt["names"][i],dt["names"][i+3])
                    time = dt["names"][i+2]
                    f.write(str(float(time[0]))+","+str(iterMean)+ "\n")


            
#        dt_times = pd.read_table(DATA_FOLDER_TIMES+name[:name.rfind(".csv")]+"-times.csv")
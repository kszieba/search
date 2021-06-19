# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 18:40:36 2021


"""

import matplotlib.pyplot as plt
import numpy as np
#import math
#import time
import argparse

xvalues=[]
for i in range(1, 101):
    xvalues.append(i)

def plotMathFunction(yvalues, title):
    plt.plot(yvalues)
    plt.yscale('linear')
    plt.title(title)
    plt.show()
    
def plot(yvalues, title):
    plt.plot(yvalues)
    plt.yscale('linear')
    plt.xlabel("Number of Elements in Sequence(n)")
    plt.title(title)
    plt.show()    
    
def plot2(yvalues, title, yvalues2):
    plt.plot(yvalues)
    plt.plot(yvalues2)
    plt.title(title)
    plt.show()   
"""
#2^10=O(1)   
f1Yvalues=[]
for i in range(1, 101):
    f1Yvalues.append(pow(2,10)+0*i)
plotMathFunction(f1Yvalues, "Plot of 2 Raised to the 10th Power") 


#2log2n=O(n)
f2Yvalues=[]
for i in range(1, 101):
    f2Yvalues.append((math.log2(i))*2)
plotMathFunction(f2Yvalues, "Plot of 2 Times the Log of n") 
"""

#create sequence of length s for inputting
def makeSequence(length):
    sequence=[]
    for i in range(0, length*3, 2):
        sequence.append(1)
    return sequence 


def plot_expandcount(inputfile, domain):
    ibs_list = []
    ibs_fcl_list = []
    ibs_k_list = []
    ibs_k_fcl_list = []
    linecount = 0
    rfile = open(inputfile, "r")
    for line in rfile:
        linecount += 1
        pieces = line.split(",")
        if pieces[4] == domain:
            if pieces[3] == "ibs":
                ibs_list.append(pieces[12])
            elif pieces[3] == "ibs_full_closed_list_variant":
                ibs_fcl_list.append(pieces[12])
            elif pieces[3] == "ibs_katrina":
                ibs_k_list.append(pieces[12])
            elif pieces[3] == "ibs_katrina_full_closed_list":
                ibs_k_fcl_list.append(pieces[12])
    count = [0 for i in range(linecount//4)]
    for i in range(linecount//4):
        count[i] = i
    count_array = np.array(count)
    ibs_array = np.array(ibs_list)
    ibs_fcl_array = np.array(ibs_fcl_list)
    ibs_k_array = np.array(ibs_k_list)
    ibs_k_fcl_array = np.array(ibs_k_fcl_list)
    plt.plot(count_array, ibs_array)
    print(ibs_list)
    plt.plot(count_array, ibs_fcl_array)
    plt.plot(count_array, ibs_k_array)
    plt.plot(count_array, ibs_k_fcl_array)
    plt.ylim(0, 70000)
    plt.title("Plot of Nodes Expanded")
    plt.show()

def plot_data(inputfile, plot_type, domain):
    if plot_type == "expandcount":
        plot_expandcount (inputfile, domain)


if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    PARSE.add_argument("-i", help='input file path (shortened)', type=str)
    #PARSE.add_argument("-o", help='output file path (shortened)', type=str)
    PARSE.add_argument("-t", help='plot type', type=str)
    PARSE.add_argument("-d", help='domain', type=str)
    arguments = PARSE.parse_args()
    if not arguments.i:
        inputfile = "ibs_results1.csv"
        plot_type = "expandcount"
        domain = "sliding_tiles"
    plot_data (inputfile, plot_type, domain)
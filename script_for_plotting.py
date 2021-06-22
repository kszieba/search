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


def plot_variable(inputfile, domain, plot_type):
    ibs_list = []
    ibs_fcl_list = []
    ibs_k_list = []
    ibs_k_fcl_list = []
    linecount = 0
    if domain == "sliding_tiles":
        domainname = "Sliding Tiles"
    else:
        domainname = "Blocksworld"
    plot_types = ["" for j in range(18)]
    plot_types[12] = "expandcount"
    plot_types[13] = "gencount"
    plot_types[14] = "time"
    plot_types[15] = "memory"
    for i in range(len(plot_types)):
        if plot_types[i] == plot_type:
            break
    rfile = open(inputfile, "r")
    for line in rfile:
        pieces = line.split(",")
        if pieces[16] != "Yes":
            if pieces[4] == domain:
                if i in (12, 13, 15):
                    if pieces[3] == "ibs":
                        ibs_list.append(int(pieces[i]))
                    elif pieces[3] == "ibs_full_closed_list_variant":
                        ibs_fcl_list.append(int(pieces[i]))
                    elif pieces[3] == "ibs_katrina":
                        ibs_k_list.append(int(pieces[i]))
                    elif pieces[3] == "ibs_katrina_full_closed_list":
                        ibs_k_fcl_list.append(int(pieces[i]))
                elif i in (14,):
                    if pieces[3] == "ibs":
                        ibs_list.append(float(pieces[i]))
                    elif pieces[3] == "ibs_full_closed_list_variant":
                        ibs_fcl_list.append(float(pieces[i]))
                    elif pieces[3] == "ibs_katrina":
                        ibs_k_list.append(float(pieces[i]))
                    elif pieces[3] == "ibs_katrina_full_closed_list":
                        ibs_k_fcl_list.append(float(pieces[i]))
                linecount += 1
    count = [0 for j in range(linecount//4)]
    for j in range(linecount//4):
        count[j] = j
    plt.plot(count, ibs_list)
    plt.plot(count, ibs_fcl_list)
    plt.plot(count, ibs_k_list)
    plt.plot(count, ibs_k_fcl_list)
    titlelist = plot_types = ["" for j in range(18)]
    titlelist[12] = "Nodes Expanded"
    titlelist[13] = "Nodes Generated"
    titlelist[14] = "Cumulative Time (sec)"
    titlelist[15] = "Cumulative Memory (bytes)"
    plt.title("Plot of "+ titlelist[i] + " for " + domainname)
    plt.show()

def plot_data(inputfile, plot_type, domain):
    plot_variable (inputfile, domain, plot_type)


if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    PARSE.add_argument("-i", help='input file path (shortened)', type=str)
    #PARSE.add_argument("-o", help='output file path (shortened)', type=str)
    PARSE.add_argument("-t", help='plot type', type=str)
    PARSE.add_argument("-d", help='domain', type=str)
    arguments = PARSE.parse_args()
    if not arguments.i:
        inputfile = "ibs_results2.csv"
        plot_type = "time"
        domain = "blocksworld"
    plot_data (inputfile, plot_type, domain)
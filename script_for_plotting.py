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



def plot_variable(inputfile, domain, c_type, plot_type, algor1=None, algor2=None):
    algorithms = ("ibs", "ibs_full_closed_list_variant", "ibs_katrina", "ibs_katrina_full_closed_list")
    if c_type == "all":
        algorlists = ([] for i in range(4))
    elif c_type == "two":
        algorlists = ([] for i in range(2))
        two = []
        algors = ("ibs", "ibs_fcl", "ibs_k", "ibs_kfcl")
        for j in (4):
            if algor1 == algors[j]:
                two.append(algorithms[j])
            if algor2 == algors[j]:
                two.append(algorithms[j])
            
    linecount = 0
    if domain == "sliding_tiles":
        domainname = "Sliding Tiles"
    else:
        domainname = "Blocksworld"
    plot_types = ("g_value", "expanded", "generated", "duplicates", 
                  "reexpansions","max_open", "max_wait", "max_closed")
    for i in range(len(plot_types)):
        if plot_types[i] == plot_type:
            break
    rfile = open(inputfile, "r")
    for line in rfile:
        pieces = line.split(",")
        if pieces[16] != "Yes":
            if pieces[4] == domain:
                if c_type == "all":
                    if pieces[3] == "ibs":
                        algorlists[0].append(int(pieces[i+8]))
                    elif pieces[3] == "ibs_full_closed_list_variant":
                        algorlists[1].append(int(pieces[i+8]))
                    elif pieces[3] == "ibs_katrina":
                        algorlists[2].append(int(pieces[i+8]))
                    elif pieces[3] == "ibs_katrina_full_closed_list":
                        algorlists[3].append(int(pieces[i+8]))
                elif c_type == "two":
                    if pieces[3] == two[0]:
                        algorlists[0].append(int(pieces[i+8]))
                    elif pieces[3] == two[1]:
                        algorlists[1].append(int(pieces[i+8]))
                linecount += 1
    count = [0 for j in range(linecount//4)]
    beams = (10, 20, 40, 60, 80, 100)
    for j in len(beams):
        count[j] = j
    for algorithm in algorlists:
        plt.plot(count, algorithm)
    titlelist = plot_types = ["G-Value of Solution", "Nodes Expanded", 
            "Nodes Generated", "Duplicates Pruned", "Re-expansions", 
            "Maximum Size of Open List", "Maximum Size of Wait List"
            "Maximum Size of Closed List"]
    plt.title("Plot of "+ titlelist[i] + " for " + domainname)
    plt.show()

def plot_data(inputfile, plot_type, domain):
    plot_variable (inputfile, domain, plot_type)


if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    PARSE.add_argument("-i", help='input file path (shortened)', type=str)
    PARSE.add_argument("-c", help='comparison type', type=str)
    PARSE.add_argument("-t", help='plot type', type=str)
    PARSE.add_argument("-d", help='domain', type=str)
    PARSE.add_argument("-f", help='first algorithm', type=str, required=False)
    PARSE.add_argument("-s", help='second algorithm', type=str, required=False)
    arguments = PARSE.parse_args()
    if not arguments.i:
        inputfile = "ibs_results2.csv"
        plot_type = "time"
        domain = "blocksworld"
        c_type = "all"
        plot_data (inputfile, c_type, plot_type, domain)
    else:
        inputfile = arguments.i
        c_type = arguments.c
        plot_type = arguments.t
        domain = arguments.d
        if c_type == "two":
            algor1 = arguments.f
            algor2 = arguments.s
            plot_data (inputfile, c_type, plot_type, domain, algor1, algor2)
        else:
            plot_data (inputfile, c_type, plot_type, domain)
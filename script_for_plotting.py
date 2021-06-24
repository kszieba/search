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



def plot_variable(input1, input2, plot_type):
    inputf1 = input1.split("_")
    inputf2 = input2.split("_")
    algorithms = ("ibs", "ibs_full_closed_list_variant", "ibs_katrina", "ibs_katrina_full_closed_list")
    plot_types = ("g_value", "goals_found", "expanded", "generated", "duplicates", 
                  "reexpansions","max_open", "max_wait", "max_closed")
    inputs = [input1, input2]
    for i in range(len(plot_types)):
        if plot_types[i] == plot_type:
            break
    beams = (10, 20, 40, 60, 80, 100)
    twolists =[[], []]
    for j in range(2):
        twolists[j] = [[] for i in range(len(beams))]
        rfile = open(inputs[j], "r")
        for line in rfile:
            pieces = line.split(",")
            if pieces[8] != "":
                for k in range(len(beams)):
                    if pieces[5] == str(beams[k]):
                        twolists[j][k].append(int(pieces[i+8]))
                        break
        rfile.close()
    count = [0 for j in range(len(beams))]
    averagelist1 = [0 for j in range(len(beams))]
    averagelist2 = [0 for j in range(len(beams))]
    for j in range(len(beams)):
        count[j] = j
        averagelist1[j] = sum(twolists[0][j]) / len(twolists[0][j])
        averagelist2[j] = sum(twolists[1][j]) / len(twolists[1][j])
    if inputf1[-3] == "ibs":
        label1 = "_".join(inputf1[-3:-1])
    else:
        label1 = inputf1[-2]
    if inputf2[-3] == "ibs":
        label2 = "_".join(inputf2[-3:-1])
    else:
        label2 = inputf2[-2]
    plt.plot(beams, averagelist1, label=label1)
    plt.plot(beams, averagelist2, label=label2)
    titlelist = ["G-Value of Solution", "Number of Goals Found", "Nodes Expanded", 
            "Nodes Generated", "Duplicates Pruned", "Re-expansions", 
            "Maximum Size of Open List", "Maximum Size of Wait List"
            "Maximum Size of Closed List"]
    print(averagelist1)
    print(averagelist2)
    plt.title("Plot of "+ titlelist[i])
    plt.legend()
    plt.show()

def plot_data(inputfile, plot_type, domain):
    plot_variable (inputfile, domain, plot_type)


if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    PARSE.add_argument("-f", help='first file', type=str, required=False)
    PARSE.add_argument("-s", help='second file', type=str, required=False)
    PARSE.add_argument("-t", help='plot type', type=str, required=False)
    arguments = PARSE.parse_args()
    first_file = "New_Results/korf100_1_3_ibs_k_660.csv"
    second_file = "New_Results/korf100_1_3_ibs_660.csv"
    plot_type = "expanded"
    plot_variable (first_file, second_file, plot_type)
    #plot_variable (arguments.f, arguments.s, arguments.t)